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
    daily_reward: str = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-180"
    farming_start: str = "https://game-domain.blum.codes/api/v1/farming/start"
    farming_claim: str = "https://game-domain.blum.codes/api/v1/farming/claim"
    tasks: str = "https://earn-domain.blum.codes/api/v1/tasks/"
    game_play: str = "https://game-domain.blum.codes/api/v2/game/play"
    game_claim: str = "https://game-domain.blum.codes/api/v2/game/claim"
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
    keywords: dict = {
        "6af85c01-f68d-4311-b78a-9cf33ba5b151": "GO GET",
        "38f6dd88-57bd-4b42-8712-286a06dac0a0": "VALUE",
        "d95d3299-e035-4bf6-a7ca-0f71578e9197": "BEST PROJECT EVER",
        "53044aaf-a51f-4dfc-851a-ae2699a5f729": "HEYBLUM",
        "835d4d8a-f9af-4ff5-835e-a15d48e465e6": "CRYPTOBLUM",
        "3c048e58-6bb5-4cba-96cb-e564c046de58": "SUPERBLUM",
        "350501e9-4fe4-4612-b899-b2daa11071fb": "CRYPTOSMART",
        "b611352b-0d8c-44ec-8e0f-cd71b5922ca5": "BLUMERSSS",
        "92373c2b-2bf3-44c0-90f7-a7fd146c05c5": "HAPPYDOGS",
        "d2715289-b487-43bc-bc21-18224f8f6bc3": "NODOXXING",
        "7067a3db-d9c5-4268-ac19-c393743e8491": "WOWBLUM",
        "c60919cd-0282-46fe-854a-1da0a01db9b2": "Blum - Big City Life",
        "1572a605-d714-4f2c-8045-9c5f874d9c7e": "MEMEBLUM",
        "30d9f351-614e-4565-a1bb-e7e94fc3dc3c": "ONFIRE",
        "d2a972a1-12ab-4c7b-a411-da056609f2bd": "SOBLUM",
        "56d210c1-446b-473b-b7c4-cba856b4476c": "BLUMEXPLORER",
        "25928ae7-c3c2-40ba-bb78-975ed68e4a5a": "CRYPTOFAN",
        "dc627a62-f747-4cbb-981f-62cf82a85458": "BLUMTASTIC",
        "71ad89ea-f11f-4825-af9c-408fba7dfd8e": "BLUMFORCE",
        "a669a160-45fd-4935-9eda-58079e19aad5": "ULTRABLUM",
        "7491c933-e49d-4a60-89cd-53d9fe690dca": "BLUMSTORM",
        "900bc6e5-d73e-49fe-adf5-1f8111f1b431": "BLUMEXTRA",
        "6fb7499f-8b38-4132-8255-c3184cc2712c": "PUMPIT",
        "98d390d1-95da-475f-8df9-53a335842c3a": "BLUMHELPS",
        "92bc4338-85ca-4bf9-a0a5-320e677116fd": "FOMOOO",
        "bb84e765-31aa-4f0d-8430-b3f75d88c1aa": "CRYPTOZONE",
        "7a3502e2-cdc7-4842-8879-bbeb2ebec594": "BLUMIFY",
        "4477c434-f8df-4432-a3d7-b47a6e44c1d7": "DEXXX",
    }


config = Config()
