import os

from df_db_connector import connector_factory
from df_runner import Pipeline

from scenario import script
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


YDB_NAME = os.getenv("YDB_NAME")
YDB_HOST = os.getenv("YDB_HOST")
YDB_PORT = os.getenv("YDB_PORT")

db = connector_factory(f"grpc://{YDB_HOST}:{YDB_PORT}/{YDB_NAME}")


pipeline = Pipeline.from_script(
    script,
    start_label=("root", "start_node"),
    fallback_label=("root", "fallback_node"),
    context_db=db,
)

if __name__ == "__main__":
    pipeline.start_sync()
