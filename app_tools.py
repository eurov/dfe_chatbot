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
    if re.search(r"(?i)(help)", ctx.last_request):
        ctx.current_node.response = (
            f"{ctx.last_response} \033[36m{help_description}\033[32m"
        )
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def get_history(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns current session history"""
    if re.search(r"(?i)(history)", ctx.last_request):
        history = json.dumps(ctx.misc, indent=4)
        ctx.current_node.response = f"{ctx.last_response}\n\t\033[36m<Current session history>\n{history}\033[32m"
        ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def save_session_history(ctx: Context, actor: Actor, *args, **kwargs) -> Context:
    """Stores current chat history in ctx.misc"""
    dt = datetime.now()
    dt_string = dt.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
    ctx.misc[f"{dt_string} :> Me"] = ctx.last_request  # saving a last user request
    processed_node = ctx.current_node
    if hasattr(processed_node.response, "__call__"):
        value = processed_node.response.__name__
    else:
        value = processed_node.response
    ctx.misc[f"{dt_string} :> Bot"] = value  # saving a last bot response
    return ctx


def operator_custom_response(ctx: Context, actor: Actor, *args, **kwargs):
    """Configuring an operator's response"""
    if re.search(r"(?i)(model)", ctx.last_request):
        section = "Our models"
    elif re.search(r"(?i)(drive)", ctx.last_request):
        section = "Sign up for a test drive"
    elif re.search(r"(?i)(dealer)", ctx.last_request):
        section = "Find a dealer"
    elif re.search(r"(?i)(service)", ctx.last_request):
        section = "Assistance service"
    else:
        return ctx
    ctx.current_node.response = (
        f"Would you like me to transfer you to \033[36m<{section}>\033[32m section?"
        f"\n\t[Y] > confirm transfer"
        f"\n\t[n] > go back to reception"
    )
    ctx.overwrite_current_node_in_processing(ctx.current_node)
    return ctx


def operator_custom_transfer(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns the NodeLabel2Type depending on request"""

    if re.search("y", ctx.last_request):
        pre_request = ctx.requests[max(ctx.requests) - 1]
        if re.search("help|history", pre_request):
            pre_request = ctx.requests[max(ctx.requests) - 2]
        if re.search("model", pre_request):
            return "models_flow", "node1", 1.1
        elif re.search("drive", pre_request):
            return "test_drive_flow", "node1", 1.1
        elif re.search("dealer", pre_request):
            return "dealer_flow", "node1", 1.1
        elif re.search("service", pre_request):
            return "service_flow", "node1", 1.1
    if re.search("n", ctx.last_request):
        return "operator_flow", "reception_node"
    return "root", "fallback_node", 1.1
