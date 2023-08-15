
'''
Module for configurations
'''
import logging
import tomllib

from constants import BASE_DIR

logger = logging.getLogger(__name__)


def get_config_file():
    """Get the config file path"""
    config = BASE_DIR.joinpath("config.toml")
    if config.exists():
        return config
    config = BASE_DIR.joinpath("config.toml.example").rename(config)
    return config


def load():
    """Load the settings from the config file"""

    config_file = get_config_file()
    with open(str(config_file), "rb") as file:
        setting = tomllib.load(file)
        logger.debug("Settings loaded successfuly")
    return setting


# This is to have only one instance of the settings
SETTINGS = load()
