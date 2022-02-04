import os
from dotenv import load_dotenv
import logging

def initialize():
    load_dotenv()

    global API_TOKEN, LOG_CHANNEL
    API_TOKEN = os.getenv("API_TOKEN")
    LOG_CHANNEL = os.getenv("LOG_CHANNEL")

    global logger
    # Enable logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='myapp.log',
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)

    global alphabet
    alphabet = "abcdefghijklmnopqrstuvwxyzäöüßABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ"+"Åå"

    # crete necessary folders
    if not os.path.exists("data"):
        logger.info("Creating data directory...")
        os.makedirs("data")
    if not os.path.exists("img"):
        logger.info("Creating img directory...")
        os.makedirs("img")
