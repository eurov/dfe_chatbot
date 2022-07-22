import random
import re
from colorama import Fore

from df_engine.core import Context, Actor

from vocabulary import help_, wands, faculties, navigator


def get_help(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns help hint"""
    if re.search(r"(?i)(help)", ctx.last_request):
        ctx.current_node.response = (
            f"{ctx.last_response} \n{Fore.CYAN}{help_}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_start_navi_hint(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns navigation hint"""
    if not ctx.last_request == "help":
        commands = [f"\t[{key}] > {value}" for key, value in navigator.items()]
        navi_hint = '\n'.join(commands[:2])
        ctx.current_node.response = (
            f"{ctx.current_node.response} \n{Fore.YELLOW}{navi_hint}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_ollivanders_offer(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns Ollivander's offer"""
    if not ctx.last_request == "help":
        goods = [f"\t[{key}] > {value}" for key, value in wands.items()]
        offer = '\n'.join(goods)
        ctx.current_node.response = (
            f"{ctx.current_node.response} \n{Fore.YELLOW}{offer}"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def pickup_wand(ctx: Context, actor: Actor, *args, **kwargs):
    """Puts the wand in ctx.misc"""
    if re.search(r'[1-3]', ctx.last_request):
        ctx.misc["wand"] = wands[int(ctx.last_request)]
    return ctx


def sorting_hat(ctx: Context, actor: Actor, *args, **kwargs):
    """Declares a faculty and save in ctx.misc"""
    if ctx.last_request == "hat":
        faculty = faculties[random.randint(1, 4)]
        ctx.current_node.response = f"Congrats! The hat chose the {faculty}!"
        ctx.misc["faculty"] = faculty
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx