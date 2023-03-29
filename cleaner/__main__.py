from sys import stdout

from loguru import logger
from pyuac import isUserAdmin, runAsAdmin

from cleaner.interface import start

logger.remove()
logger.add(stdout, level="INFO", format="[{time:HH:mm:ss}] [{level}] [<level>{message}</level>]")

if __name__ == "__main__":
    if not isUserAdmin():
        logger.warning("Programa reiniciado como administrador")
        runAsAdmin()
        quit()

    start()
