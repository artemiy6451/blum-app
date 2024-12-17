import sys

from api import Api
from loguru import logger

CHOOSE_TEXT = """1. Get balance
2. Start daily farm
3. Claim daily farm
4. Claim daily reward
5. Complete tasks
6. Play all awaliable games
Type `q` to quit
-> """


def main() -> None:
    logger.info("Start app!")
    api = Api()
    api.get_username()
    while True:
        match input(f"Coose what you want to do:\n{CHOOSE_TEXT}"):
            case "1":
                api.get_balance()
            case "2":
                api.start_farming()
            case "3":
                api.claim_farming()
            case "4":
                api.claim_daily_reward()
            case "5":
                api.process_tasks()
            case "6":
                api.play_game()
            case "q":
                sys.exit(0)
            case _:
                logger.info("Do you choose right number?")


if __name__ == "__main__":
    main()
