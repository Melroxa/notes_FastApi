import logging

logging.basicConfig(
    filename="actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_action(action: str):
    logging.info(action)
