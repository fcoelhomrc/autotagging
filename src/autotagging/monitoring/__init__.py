import logging
import logging.config
import yaml
import os

config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
