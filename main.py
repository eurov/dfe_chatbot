import os

from df_db_connector import connector_factory
from df_runner import ScriptRunner

from scenario import script
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


DB_NAME = os.getenv("PG_NAME")
DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_LOGIN = os.getenv("PG_USERNAME")
DB_PASSWORD = os.getenv("PG_PASSWORD")

db = connector_factory(f"postgresql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")  # try except?


runner = ScriptRunner(
    script,
    start_label=("root", "start_node"),
    fallback_label=("root", "fallback_node"),
    db=db,
)

if __name__ == "__main__":
    runner.start()
