import logging
import os
import datetime
from datetime import datetime, timezone
import Datalake2Sentinel.config as config
import azure.functions as func
import json
from Datalake2Sentinel.Datalake2Sentinel import Datalake2Sentinel


def _build_logger():
    logger = logging.getLogger("datalake2sentinel")
    logger.setLevel(logging.INFO)
    if config.verbose_log:
        logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.getenv("log_file"), mode="a")
    handler.setLevel(logging.INFO)
    if config.verbose_log:
        handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def pmain(logger):
    tenant = json.loads(os.getenv("tenant"))
    datalake = json.loads(os.getenv("datalake"))

    datalake2Sentinel = Datalake2Sentinel(logger, tenant, datalake)
    datalake2Sentinel.uploadIndicatorsToSentinel()


def main(mytimer: func.TimerRequest):
    utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info("The timer is past due!")

    logger = _build_logger()

    logger.info("Start Datalake2Sentinel")
    pmain(logger)
    logger.info("End Datalake2Sentinel")
    logger.info("Python timer trigger function ran at %s", utc_timestamp)
