import os

from df_db_connector import connector_factory
from df_runner import ScriptRunner

from scenario import script
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

db = connector_factory(f"grpc://{DB_HOST}:{DB_PORT}/{DB_NAME}")


runner = ScriptRunner(
    script,
    start_label=("root", "start_node"),
    fallback_label=("root", "fallback_node"),
    db=db,
)

if __name__ == "__main__":
    runner.start()
