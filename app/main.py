from api import Api
from loguru import logger


def main() -> None:
    logger.info("Start app!")
    api = Api()
    api.get_username()


if __name__ == "__main__":
    main()
