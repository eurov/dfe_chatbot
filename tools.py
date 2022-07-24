import random
import re
from colorama import Fore

from df_engine.core import Context, Actor

from text import HELP_, WANDS, FACULTIES, NAVIGATOR, HAGRID_SPEECH


def choose_hagrid_greeting(ctx: Context) -> str:
    """Returns greeting depends on user grade"""
    if ctx.misc:
        return HAGRID_SPEECH[1]
    return HAGRID_SPEECH[0]


def get_grade(ctx: Context, actor: Actor, *args, **kwargs) -> tuple:
    """Returns transition route depends on user grade"""
    if ctx.misc:
        return "second_year", "platform 9¾"
    return "first_year", "ollivander_shop"


def overwrite_response(
    ctx: Context, current_response: str, nav_commands: list
) -> Context:
    """Overwrites response with nav hints"""
    hint = "\n".join(nav_commands)
    ctx.current_node.response = f"{current_response} \n{Fore.YELLOW}{hint}"
    ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_selected_nav_commands(source, required_commands=None) -> list:
    """Returns selected nav commands"""
    if not required_commands:
        required_commands = source
    return [
        f"\t[{key}] > {value}"
        for key, value in source.items()
        if key in required_commands
    ]


def get_help(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns help hint"""
    if re.search(r"(?i)(help)", ctx.last_request):
        ctx.current_node.response = f"{ctx.last_response} \n{Fore.CYAN}{HELP_}"
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_hagrid_greeting(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns Hagrid's greeting"""
    if not ctx.last_request == "help":
        current_response = choose_hagrid_greeting(ctx)
        nav_commands = get_selected_nav_commands(NAVIGATOR, ["start", "help"])
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def get_fallback_navi_hint(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns fallback alert"""
    if not ctx.last_request == "help":
        current_response = f"{Fore.CYAN}{ctx.current_node.response}\n"
        nav_commands = get_selected_nav_commands(NAVIGATOR, ["back", "help"])
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def get_ollivander_offer(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns Ollivander's offer"""
    if not ctx.last_request == "help":
        current_response = ctx.current_node.response
        nav_commands = get_selected_nav_commands(WANDS)
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def pickup_wand(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Puts the wand into ctx.misc"""
    if re.search(r"[1-3]", ctx.last_request):
        ctx.misc["wand"] = WANDS[int(ctx.last_request)]
    return ctx


def get_hogwarts_navi_hint(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns Dunbledor's greeting"""
    if not ctx.last_request == "help":
        current_response = ctx.current_node.response
        nav_commands = get_selected_nav_commands(NAVIGATOR, ["hat", "back", "help"])
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def sorting_hat(ctx: Context) -> str:
    """Declares a faculty and save into ctx.misc"""
    faculty = FACULTIES[random.randint(1, len(FACULTIES))]
    ctx.misc["faculty"] = faculty
    return (
        f"Congrats! The hat chose the {faculty}!\n\t An unforgettable year awaits you!"
    )


def get_hat_navi_hint(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns Dumbledor's response"""
    if not ctx.last_request == "help":
        current_response = sorting_hat(ctx)
        nav_commands = get_selected_nav_commands(NAVIGATOR, ["hat", "back", "help"])
        overwrite_response(ctx, current_response, nav_commands)
    return ctx
