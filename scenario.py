import re
from colorama import Fore

import df_engine.conditions as cnd
import df_engine.labels as lbl
from tools import sorting_hat, get_help, pickup_wand, get_response
from df_engine.core.keywords import (
    TRANSITIONS,
    RESPONSE,
    GLOBAL,
    PRE_RESPONSE_PROCESSING, PRE_TRANSITIONS_PROCESSING,
)

from vocabulary import greeting, ollivander

script = {
    "root": {
        "start_node": {
            RESPONSE: greeting,
            TRANSITIONS: {
                ("quest", "ollivanders"): cnd.exact_match("fwd"),
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
            lbl.repeat(1.1): cnd.regexp(r"help", re.I),
            lbl.previous(): cnd.regexp(r"back", re.I),
        },
    },
    "quest": {
        "ollivanders": {
            RESPONSE: ollivander,
            PRE_TRANSITIONS_PROCESSING: {
                "pickup_wand": pickup_wand,
            },
            TRANSITIONS: {
                lbl.forward(): cnd.true()
            },
        },
        "sorting_hat": {
            PRE_RESPONSE_PROCESSING: {
                "sorting": sorting_hat,
            },
            RESPONSE: "Let the Sorting Hat decide where you will study!",
            TRANSITIONS: {
                lbl.forward(): cnd.regexp(r"fwd", re.I),
                lbl.repeat(): cnd.regexp(r"hat", re.I),
            },
        },
    },
}
