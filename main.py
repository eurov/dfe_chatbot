import logging
import time
from typing import Union
from df_engine.core import Context, Actor

from app_scenario import script


logger = logging.getLogger(__name__)

actor = Actor(
    script,
    start_label=("root", "start_node"),
    fallback_label=("root", "fallback_node"),
)


def turn_handler(
    in_request: str,
    ctx: Union[Context, str, dict],
    _actor: Actor,
):
    ctx = Context.cast(ctx)
    ctx.add_request(in_request)
    ctx = actor(ctx)
    out_response = ctx.last_response
    logging.info(
        "\033[37mBot: \033[3m\033[32m{}\033[37m\n<<hint>> I'm here: {}\033[0m".format(
            out_response, ctx.last_label
        )
    )
    return out_response, ctx


def run_interactive_mode(_actor):
    ctx = {}
    while True:
        time.sleep(0.1)
        in_request = input("Me: ")
        _, ctx = turn_handler(in_request, ctx, actor)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )
    run_interactive_mode(actor)
