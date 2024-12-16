import os
from dataclasses import dataclass

from dotenv import load_dotenv
from fake_headers import Headers
from loguru import logger

logger.debug("Init config file...")

load_dotenv()


@dataclass
class Urls:
    auth: str = (
        "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    )
    user_me: str = "https://user-domain.blum.codes/api/v1/user/me"
    game_balance: str = "https://game-domain.blum.codes/api/v1/user/balance"
    farming_start: str = "https://game-domain.blum.codes/api/v1/farming/start"
    farming_claim: str = "https://game-domain.blum.codes/api/v1/farming/claim"
    daily_reward: str = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-420"
    game_play: str = "https://game-domain.blum.codes/api/v2/game/play"
    game_claim: str = "https://game-domain.blum.codes/api/v2/game/claim"
    tasks: str = "https://earn-domain.blum.codes/api/v1/tasks"
    payload: str = "http://localhost:9876"


@dataclass
class SessionKeys:
    query_id: str = os.getenv("QUERY_ID", "")
    user: str = os.getenv("USER", "")
    auth_date: str = os.getenv("AUTH_DATE", "")
    signature: str = os.getenv("SIGNATURE", "")
    hash: str = os.getenv("HASH", "")

    def to_dict(self) -> dict:
        return {
            "query": f"query_id={self.query_id}&"
            f"user={self.user}&"
            f"auth_date={self.auth_date}&"
            f"signature={self.signature}&"
            f"hash={self.hash}",
            "referralToken": "vTHusRz4j0",
        }


class Config:
    urls: Urls = Urls()
    headers: dict = Headers(headers=False).generate()
    session_keys: dict = SessionKeys().to_dict()


config = Config()
