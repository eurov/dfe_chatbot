import re
from colorama import Fore

import df_engine.conditions as cnd
import df_engine.labels as lbl
from tools import sorting_hat, get_help, pickup_wand, get_start_navi_hint, get_ollivanders_offer
from df_engine.core.keywords import (
    TRANSITIONS,
    RESPONSE,
    GLOBAL,
    PRE_RESPONSE_PROCESSING, PRE_TRANSITIONS_PROCESSING,
)

from vocabulary import hagrids_greeting, ollivanders_speech

script = {
    "root": {
        "start_node": {
            PRE_RESPONSE_PROCESSING: {
                "navi": get_start_navi_hint
            },
            RESPONSE: hagrids_greeting,
            TRANSITIONS: {
                ("first_year", "ollivanders_shop"): cnd.exact_match("start"),
            },
        },
        "fallback_node": {RESPONSE: f"{Fore.MAGENTA} Avada Kedavra!"},
    },
    GLOBAL: {
        PRE_RESPONSE_PROCESSING: {
            "help": get_help,
        },
        TRANSITIONS: {
            lbl.to_start(): cnd.regexp(r"home|start|hello|hi", re.I),
            lbl.repeat(): cnd.exact_match(r"help", re.I),
            lbl.previous(): cnd.exact_match(r"back", re.I),
        },
    },
    "first_year": {
        "ollivanders_shop": {
            PRE_RESPONSE_PROCESSING: {
                "navi": get_ollivanders_offer
            },
            RESPONSE: ollivanders_speech,
            PRE_TRANSITIONS_PROCESSING: {
                "pickup_wand": pickup_wand,
            },
            TRANSITIONS: {
                lbl.forward(): cnd.regexp(r'1|2|3')
            },
        },
        "sorting_hat": {
            PRE_RESPONSE_PROCESSING: {
                "sorting": sorting_hat,
            },
            RESPONSE: "Let the Sorting Hat decide where you will study!",
            TRANSITIONS: {
                lbl.forward(): cnd.exact_match(r"fwd", re.I),
                lbl.repeat(): cnd.exact_match(r"hat", re.I),
            },
        },
    },
}
