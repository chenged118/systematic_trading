# src/utils/logger.py

import logging

def setup_logger():
    logger = logging.getLogger("quant-bot")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("logs/app.log")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(handler)
    return logger