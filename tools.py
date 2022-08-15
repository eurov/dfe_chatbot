import random
import re
from colorama import Fore, init

from df_engine.core import Context, Actor
from text import HELP_, WANDS, FACULTIES, NAVIGATOR, HAGRID_SPEECH


init(autoreset=True)


def choose_hagrid_greeting(ctx: Context) -> str:
    """Returns greeting depends on user grade"""
    if ctx.misc:
        return HAGRID_SPEECH[1]
    return HAGRID_SPEECH[0]


def get_grade(ctx: Context, actor: Actor, *args, **kwargs) -> tuple:
    """Returns transition route depends on user grade"""
    if ctx.misc:
        return "second_year", "kings_cross"
    return "first_year", "ollivander_shop"


def overwrite_response(ctx: Context, current_response: str, nav_commands: list) -> Context:
    """Overwrites response with nav hints"""
    hint = "\n".join(nav_commands)
    ctx.current_node.response = f"{Fore.GREEN}{current_response}\n{Fore.YELLOW}{hint}"
    ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_help(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Returns help hint"""
    if re.search(r"(?i)(help)", ctx.last_request):
        ctx.current_node.response = f"{ctx.last_response} \n{Fore.CYAN}{HELP_}"
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def pickup_wand(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Puts the wand into ctx.misc"""
    if re.search(r"[1-3]", ctx.last_request):
        ctx.misc["wand"] = WANDS[int(ctx.last_request)]
    return ctx


def sorting_hat(ctx: Context) -> str:
    """Declares a faculty and save into ctx.misc"""
    faculty = FACULTIES[random.randint(1, len(FACULTIES))]
    ctx.misc["faculty"] = faculty
    return f"Congrats! The hat chose the {faculty}!\n\t An unforgettable year awaits you!"


navi_hints = {
    "start_node": ["start", "help"],
    "ollivander_shop": WANDS,
    "fallback_node": ["back", "help"],
    "hogwarts_school": ["hat", "back", "help"],
    "sorting_hat": ["next", "back", "help"],
}


def format_selected_nav_commands(source, required_commands=None) -> list:
    """Returns selected nav commands"""
    if not required_commands:
        required_commands = source
    return [f"\t[{key}] > {value}" for key, value in source.items() if key in required_commands]


def get_navi_hint(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    if not ctx.last_request == "help":
        current_response = ctx.current_node.response
        if ctx.last_label[1] == "start_node":
            current_response = choose_hagrid_greeting(ctx)
        elif ctx.last_label[1] == "sorting_hat":
            current_response = sorting_hat(ctx)
        if ctx.last_label[1] == "ollivander_shop":
            nav_commands = format_selected_nav_commands(WANDS)
        else:
            nav_commands = format_selected_nav_commands(NAVIGATOR, navi_hints[ctx.last_label[1]])
        overwrite_response(ctx, current_response, nav_commands)
    return ctx
