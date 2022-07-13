import re

from df_engine.core import Context, Actor
from app_vocabulary import home_page_description, help_description


def home_page(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns the description of home page"""
    return home_page_description


def show_help(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns a hint with useful information"""
    if re.search(r'(?i)(help)', ctx.last_request):
        processed_node = ctx.current_node
        processed_node.response = f"{ctx.last_response} \033[36m{help_description}\033[32m"
        ctx.overwrite_current_node_in_processing(processed_node)
    return ctx

