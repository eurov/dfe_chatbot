import os

from df_db_connector import connector_factory
from df_runner import ScriptRunner
from df_telegram_connector.connector import TelegramConnector
from df_telegram_connector.request_provider import PollingRequestProvider

from scenario import script
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


YDB_NAME = os.getenv("YDB_NAME")
YDB_HOST = os.getenv("YDB_HOST")
YDB_PORT = os.getenv("YDB_PORT")

db = connector_factory(f"grpc://{YDB_HOST}:{YDB_PORT}/{YDB_NAME}")


bot = TelegramConnector(os.getenv("BOT_TOKEN"))
provider = PollingRequestProvider(bot=bot)


runner = ScriptRunner(
    script,
    start_label=("root", "start_node"),
    fallback_label=("root", "fallback_node"),
    db=db,
    request_provider=provider,
)

if __name__ == "__main__":
    runner.start()
