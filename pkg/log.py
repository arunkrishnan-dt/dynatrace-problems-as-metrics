import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from configparser import ConfigParser

# Read Config File
# Read config
config_obj = ConfigParser()
config_file = Path(__file__).parents[1] / "problems.config"
config_obj.read(config_file)

# Create logger
logger = logging.getLogger()

# Create handler for logging data to file
log_file = Path(__file__).parents[1] / Path("logs") / "problems.log"
logger_handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)

#Create the Handler for logging data to console.
console_handler = StreamHandler()

# Set Logging mode
if config_obj["LOGGING"]["LOG_MODE"] == "INFO":
    logger.setLevel(logging.INFO)
    logger_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
if config_obj["LOGGING"]["LOG_MODE"] == "DEBUG":
    logger.setLevel(logging.DEBUG)
    logger_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s : %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)
console_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.addHandler(console_handler)