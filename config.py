from pathlib import Path


PROJECT_DIR = Path(__file__).parent

RESULTS_DATABASE_NAME = "results_database_name"
RESULTS_DATABASE_PATH = PROJECT_DIR / RESULTS_DATABASE_NAME

MYSQL_HOST = "0.0.0.0"
MYSQL_PORT = 3307
MYSQL_USER = "root"
MYSQL_PASSWORD = "root_password"
MYSQL_PARSED_ITEMS_DATABASE = "youtube_parsed_items_database"
MYSQL_PARSED_ITEMS_TABLE = "youtube_parsed_items_table"
MYSQL_PARSED_ITEMS_ID_COLUMN = "video_id"
