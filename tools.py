import random
import re
from colorama import Fore

from df_engine.core import Context, Actor

from text import HELP_, WANDS, FACULTIES, NAVIGATOR, HAGRID_SPEECH


def choose_hagrid_greeting(ctx: Context):
    if ctx.misc:
        return HAGRID_SPEECH[1]
    return HAGRID_SPEECH[0]


def overwrite_response(ctx: Context, current_response: str, nav_commands: list):

    hint = "\n".join(nav_commands)
    ctx.current_node.response = f"{current_response} \n{Fore.YELLOW}{hint}"
    ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_hagrid_greeting(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds navigation hint to response"""
    if not ctx.last_request == "help":
        current_response = choose_hagrid_greeting(ctx)
        nav_commands = [
            f"\t[{key}] > {value}"
            for key, value in NAVIGATOR.items()
            if key in ["start", "help"]
        ]
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def get_grade(ctx: Context, actor: Actor, *args, **kwargs):
    if ctx.misc:
        return "second_year", "platform 9¾"
    return "first_year", "ollivander_shop"


def get_help(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns help hint"""
    if re.search(r"(?i)(help)", ctx.last_request):
        ctx.current_node.response = f"{ctx.last_response} \n{Fore.CYAN}{HELP_}"
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_fallback_navi_hint(ctx: Context, actor: Actor, *args, **kwargs):
    if not ctx.last_request == "help":
        current_response = f"{Fore.CYAN}{ctx.current_node.response}\n"
        nav_commands = [
            f"\t[{key}] > {value}"
            for key, value in NAVIGATOR.items()
            if key in ["back", "help"]
        ]
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def get_ollivander_offer(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds Ollivander's offer to response"""
    if not ctx.last_request == "help":
        current_response = ctx.current_node.response
        nav_commands = [f"\t[{key}] > {value}" for key, value in WANDS.items()]
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def pickup_wand(ctx: Context, actor: Actor, *args, **kwargs):
    """Puts the wand in ctx.misc"""
    if re.search(r"[1-3]", ctx.last_request):
        ctx.misc["wand"] = WANDS[int(ctx.last_request)]
    return ctx


def get_hogwarts_navi_hint(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds navigation hint to response"""
    if not ctx.last_request == "help":
        current_response = ctx.current_node.response
        nav_commands = [
            f"\t[{key}] > {value}"
            for key, value in NAVIGATOR.items()
            if key in ["hat", "back", "help"]
        ]
        overwrite_response(ctx, current_response, nav_commands)
    return ctx


def sorting_hat(ctx: Context):
    """Declares a faculty and save in ctx.misc"""
    faculty = FACULTIES[random.randint(1, len(FACULTIES))]
    ctx.misc["faculty"] = faculty
    return (
        f"Congrats! The hat chose the {faculty}!\n\t An unforgettable year awaits you!"
    )


def get_hat_navi_hint(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds navigation hint to response"""
    if not ctx.last_request == "help":
        current_response = sorting_hat(ctx)
        nav_commands = [
            f"\t[{key}] > {value}"
            for key, value in NAVIGATOR.items()
            if key in ["next", "back", "help"]
        ]
        overwrite_response(ctx, current_response, nav_commands)
    return ctx
