import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
import os

LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=3
            ),
            RichHandler(
                rich_tracebacks=True,
                markup=True
            )
        ]
    )
    # Silence noisy libraries
    for name in [
        "watchfiles",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "asyncio",
    ]:
        logging.getLogger(name).setLevel(logging.WARNING)
