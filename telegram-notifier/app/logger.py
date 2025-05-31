import logging

logger = logging.getLogger("notifier")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("notifier.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)