from typing import Any, Callable

import requests
from config import config
from loguru import logger


class Api:

    _token: str

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

    @error_wrapper
    def get_balance(self) -> int:
        response = self.session.get(config.urls.game_balance)
        if not response.ok:
            raise Exception(
                "Can not get balance "
                f"with status code {response.status_code}: {response.text}"
            )
        return 0
