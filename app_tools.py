from datetime import datetime
import json
import re

from df_engine.core import Context, Actor
from app_vocabulary import home_page_description, help_description


def home_page(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns the description of home page"""
    return home_page_description


def get_help(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns help hint"""
    if re.search(r'(?i)(help)', ctx.last_request):
        ctx.current_node.response = f"{ctx.last_response} \033[36m{help_description}\033[32m"
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_history(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns current session history"""
    if re.search(r'(?i)(history)', ctx.last_request):
        history = json.dumps(ctx.misc, indent=4)
        ctx.current_node.response = f"{ctx.last_response}\n\t\033[36m<Current session history>\n{history}\033[32m"
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def save_session_history(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Stores current chat history in ctx.misc"""
    dt = datetime.now()
    dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    ctx.misc[f'{dt_string} :> Me'] = ctx.last_request  # saving a last user request
    processed_node = ctx.current_node
    if hasattr(processed_node.response, '__call__'):
        value = processed_node.response.__name__
    else:
        value = processed_node.response
    ctx.misc[f'{dt_string} :> Bot'] = value  # saving a last bot response
    return ctx






