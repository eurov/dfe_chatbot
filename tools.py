import random
import re
from colorama import Fore

from df_engine.core import Context, Actor

from text import HELP_, WANDS, FACULTIES, NAVIGATOR, HAGRID_SPEECH


def choose_hagrid_greeting(ctx: Context, actor: Actor, *args, **kwargs):
    if ctx.misc:
        return HAGRID_SPEECH[1]
    return HAGRID_SPEECH[0]


def get_hagrid_greeting(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds navigation hint to response"""
    if not ctx.last_request == "help":
        commands = [f"\t[{key}] > {value}" for key, value in NAVIGATOR.items()]
        navi_hint = "\n".join(commands[:2])
        ctx.current_node.response = (
            f"{choose_hagrid_greeting(ctx, actor)} \n{Fore.YELLOW}{navi_hint}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
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
        commands = [f"\t[{key}] > {value}" for key, value in NAVIGATOR.items()]
        navi_hint = "\n".join(commands[1:3])
        ctx.current_node.response = (
            f"{ctx.current_node.response}\n\n{Fore.YELLOW}{navi_hint}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_ollivander_offer(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds Ollivander's offer to response"""
    if not ctx.last_request == "help":
        goods = [f"\t[{key}] > {value}" for key, value in WANDS.items()]
        offer = "\n".join(goods)
        ctx.current_node.response = (
            f"{ctx.current_node.response} \n{Fore.YELLOW}{offer}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def pickup_wand(ctx: Context, actor: Actor, *args, **kwargs):
    """Puts the wand in ctx.misc"""
    if re.search(r"[1-3]", ctx.last_request):
        ctx.misc["wand"] = WANDS[int(ctx.last_request)]
    return ctx


def get_hogwarts_navi_hint(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds navigation hint to response"""
    if not ctx.last_request == "help":
        commands = [f"\t[{key}] > {value}" for key, value in NAVIGATOR.items()]
        navi_hint = "\n".join(commands[-2:-5:-1])
        ctx.current_node.response = (
            f"{ctx.current_node.response}\n{Fore.YELLOW}{navi_hint}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def sorting_hat(ctx: Context, actor: Actor, *args, **kwargs):
    """Declares a faculty and save in ctx.misc"""
    faculty = FACULTIES[random.randint(1, len(FACULTIES))]
    ctx.misc["faculty"] = faculty
    return (
        f"Congrats! The hat chose the {faculty}!\n\t An unforgettable year awaits you!"
    )


def get_hat_navi_hint(ctx: Context, actor: Actor, *args, **kwargs):
    """Adds navigation hint to response"""
    if not ctx.last_request == "help":
        commands = [f"\t[{key}] > {value}" for key, value in NAVIGATOR.items()]
        navi_hint = "\n".join([commands[-1], commands[2], commands[1]])
        ctx.current_node.response = (
            f"{sorting_hat(ctx, actor)}\n\n{Fore.YELLOW}{navi_hint}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx
