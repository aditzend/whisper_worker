"""
WHISPER_WORKER
"""

import logging
import coloredlogs
from dotenv import load_dotenv
import transcribe
import os

load_dotenv()


FORMAT = (
    "[WHISPER_WORKER] %(process)d  -  %(asctime)s %(levelname)s [%(module)s]"
    " %(message)s"
)


# logging.Formatter(FORMAT, "%m/%d/%Y, %H:%M:%S ")
logging.basicConfig(level=logging.INFO, format=FORMAT)
coloredlogs.install(level="INFO", fmt=FORMAT)
logger = logging.getLogger("main")


logger.info(f"Starting Whisper Worker {os.getenv('RABBITMQ_HOST')}")


transcribe.consume()
