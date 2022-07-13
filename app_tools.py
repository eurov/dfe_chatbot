from df_engine.core import Context, Actor
from app_vocabulary import home_page_description, help_description


def home_page(ctx: Context, actor: Actor, *args, **kwargs):
    """Returns the description of home page"""
    return home_page_description


