import time
from http import HTTPStatus
from typing import Any, Callable

import requests
from config import config
from loguru import logger


class Api:

    balance: int
    count_tikets: int
    username: str

    def __init__(self) -> None:
        logger.debug("Init api class")
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://telegram.blum.codes",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0)"
            "Gecko/20100101 Firefox/132.0",
        }
        if not self._get_token():
            raise Exception("Can not get token")

    @staticmethod
    def error_wrapper(method: Callable[..., object]) -> Callable[..., object]:
        def wrapper(self: object, *arg: Any, **kwargs: Any) -> Any:
            try:
                logger.debug(f"Start {method.__name__} method")
                result = method(self, *arg, **kwargs)
                logger.debug(f"{method.__name__} done")
                return result
            except Exception as e:
                logger.error(f"Error in function {method.__name__}: {e}")

        return wrapper

    @error_wrapper
    def _get_token(self) -> bool:
        response = self.session.post(
            config.urls.auth, json=config.session_keys, timeout=5
        )
        if not response.ok:
            raise Exception(
                "Can not auth "
                f"with status_code {response.status_code}: {response.text}"
            )
        token = response.json().get("token").get("access")
        if token is None:
            raise Exception("Can not parse token")

        self.session.headers["Authorization"] = f"Bearer {token}"
        return True

    @error_wrapper
    def get_username(self) -> None:
        response = self.session.get(config.urls.user_me)
        if not response.ok:
            raise Exception(
                "Can not get username "
                f"with status code {response.status_code}: {response.text}"
            )
        username = response.json().get("username")
        if username is None:
            raise Exception("Can not parse username")

        logger.info(f"Logged in as: {username}")
        self.username = username

    @error_wrapper
    def get_balance(self) -> None:
        response = self.session.get(config.urls.game_balance)
        if not response.ok:
            raise Exception(
                "Can not get balance "
                f"with status code {response.status_code}: {response.text}"
            )
        self.count_tikets = response.json().get("playPasses")
        self.balance = response.json().get("availableBalance")
        if any(value is None for value in (self.count_tikets, self.balance)):
            raise Exception("Can not parse balance or count ticket")
        logger.info(f"Balance: {self.balance} ------ Tikets: {self.count_tikets}")

    @error_wrapper
    def claim_daily_reward(self) -> None:
        response = self.session.post(config.urls.daily_reward)
        if response.json().get("message") == "Not Found":
            return
        if response.json().get("message") == "same day":
            logger.info("Can not claim daily reward today, try tomorrow")
            return
        if not response.ok:
            raise Exception(
                "Can not claim daily reward "
                f"with status code {response.status_code}: {response.text}"
            )
        logger.info("Daily reward claimed")

    @error_wrapper
    def start_farming(self) -> None:
        response = self.session.post(config.urls.farming_start)
        if not response.ok:
            raise Exception(
                "Can not start farming "
                f"with status code {response.status_code}: {response.text}"
            )
        logger.info("Start farming")

    @error_wrapper
    def claim_farming(self) -> None:
        response = self.session.post(config.urls.farming_claim)
        if response.status_code == HTTPStatus.TOO_EARLY:
            logger.info(f"{response.json().get('message')}")
            return

        if not response.ok:
            raise Exception(
                "Can not claim farm "
                f"with status code {response.status_code}: {response.text}"
            )
        logger.info("Claim farming")

    @error_wrapper
    def _get_tasks(self) -> list:
        response = self.session.get(config.urls.tasks)
        if not response.ok:
            raise Exception(
                "Can not get tasks "
                f"with status code {response.status_code}: {response.text}"
            )

        tasks: list | None = response.json()
        if tasks is None:
            raise Exception("Can not parse tasks")
        return tasks

    @error_wrapper
    def parse_all_tasks(self, tasks: list) -> list:
        all_tasks = []
        collected_tasks = []

        for section in tasks:
            collected_tasks.extend(section.get("tasks", []))
            for sub_section in section.get("subSections"):
                collected_tasks.extend(sub_section.get("tasks", []))

        for task in collected_tasks:
            if task.get("subTasks"):
                all_tasks.extend(task.get("subTasks"))

        all_tasks.extend(collected_tasks)
        return all_tasks

    @error_wrapper
    def sort_tasks(self, all_tasks: list) -> dict:
        unique_tasks = {}
        task_types = ("SOCIAL_SUBSCRIPTION", "INTERNAL", "SOCIAL_MEDIA_CHECK")
        for task in all_tasks:
            if task.get("validationType") == "MEMEPAD":
                continue
            elif task.get("type") == "PROGRESS_TARGET":
                continue
            elif task.get("title") == "Join or create tribe":
                continue

            if (
                task["status"] == "NOT_STARTED"
                and task["type"] in task_types
                or task["status"] == "READY_FOR_CLAIM"
                or task["status"] == "READY_FOR_VERIFY"
                and task["validationType"] == "KEYWORD"
            ):
                unique_tasks.update({task.get("id"): task})
        return unique_tasks

    @error_wrapper
    def process_tasks(self) -> None:
        tasks = self._get_tasks()
        parsed_tasks = self.parse_all_tasks(tasks)
        sorted_tasks = self.sort_tasks(parsed_tasks)

        for task_id in sorted_tasks:  # type: ignore
            logger.debug(f"Process task with id: {task_id}")
            self.start_task(task_id)
            time.sleep(2)
            if sorted_tasks.get(task_id).get("validationType") == "KEYWORD":  # type: ignore
                keyword = config.keywords.get(task_id)
                self.validate_task(task_id, keyword=keyword)
            else:
                self.validate_task(task_id)
            self.claim_task(task_id)
            time.sleep(2)

    @error_wrapper
    def start_task(self, task: str) -> None:
        url = config.urls.tasks + task + "/start"
        response = self.session.post(url)
        if response.status_code == HTTPStatus.BAD_REQUEST:
            logger.debug(f"Task already started: {task}")
            return
        if not response.ok:
            raise Exception(
                "Can not get tasks "
                f"with status code {response.status_code}: {response.text}"
            )
        logger.debug(f"Started task with id: {task}")

    @error_wrapper
    def validate_task(self, task: str, keyword: str | None = None) -> None:
        url = config.urls.tasks + task + "/validate"
        if keyword is None:
            response = self.session.post(url, json={})
        else:
            print(keyword)
            response = self.session.post(url, json={"keywoard": keyword})

        if response.status_code == HTTPStatus.BAD_REQUEST:
            logger.debug(f"Incorrect task keyword: {task}")
            return
        if response.status_code == HTTPStatus.PRECONDITION_FAILED:
            logger.debug(f"Task do not validete: {task}")
            return

        if not response.ok:
            raise Exception(
                "Can not get tasks "
                f"with status code {response.status_code}: {response.text}"
            )
        logger.debug(f"Verifyed task with id: {task}")

    @error_wrapper
    def claim_task(self, task: str) -> None:
        url = config.urls.tasks + task + "/claim"
        response = self.session.post(url)
        if response.status_code == HTTPStatus.PRECONDITION_FAILED:
            logger.debug(f"Task is not done: {task}")
            return
        if response.status_code == HTTPStatus.BAD_REQUEST:
            logger.debug(f"Task already claimed: {task}")
            return

        if not response.ok:
            raise Exception(
                "Can not get tasks "
                f"with status code {response.status_code}: {response.text}"
            )
        logger.debug(
            f"Task `{response.json().get('title')}` "
            f"claimed with reward: {response.json().get('reward')}"
        )
