import os
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Load database configuration
def load_db_config(env="default"):
    with open("config/db_config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config.get(env, config["default"])

DB_CONFIG = load_db_config(os.getenv("APP_ENV", "default"))