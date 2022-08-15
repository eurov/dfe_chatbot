import re

import df_engine.conditions as cnd
import df_engine.labels as lbl
from tools import (
    get_help,
    pickup_wand,
    get_grade,
    get_navi_hint,
)
from df_engine.core.keywords import (
    TRANSITIONS,
    RESPONSE,
    GLOBAL,
    PRE_RESPONSE_PROCESSING,
    PRE_TRANSITIONS_PROCESSING,
)

from text import (
    OLLIVANDER_SPEECH,
    DUMBLEDORE_SPEECH,
    HARRY_SPEECH,
)

script = {
    "root": {
        "start_node": {
            PRE_RESPONSE_PROCESSING: {"hagrid_greeting": get_navi_hint},
            RESPONSE: "",
            TRANSITIONS: {
                get_grade: cnd.exact_match("start"),
            },
        },
        "fallback_node": {
            PRE_RESPONSE_PROCESSING: {"navi": get_navi_hint},
            RESPONSE: "Avada Kedavra!",
        },
    },
    GLOBAL: {
        PRE_RESPONSE_PROCESSING: {
            "help": get_help,
        },
        TRANSITIONS: {
            lbl.to_start(): cnd.regexp(r"home|hello|hi", re.I),
            lbl.repeat(): cnd.exact_match(r"help", re.I),
            lbl.previous(): cnd.exact_match(r"back", re.I),
        },
    },
    "first_year": {
        "ollivander_shop": {
            PRE_RESPONSE_PROCESSING: {"navi": get_navi_hint},
            RESPONSE: OLLIVANDER_SPEECH,
            PRE_TRANSITIONS_PROCESSING: {
                "pickup_wand": pickup_wand,
            },
            TRANSITIONS: {lbl.forward(): cnd.regexp(r"1|2|3")},
        },
        "hogwarts_school": {
            PRE_RESPONSE_PROCESSING: {
                "navi": get_navi_hint,
            },
            RESPONSE: DUMBLEDORE_SPEECH,
            TRANSITIONS: {
                lbl.forward(): cnd.exact_match(r"hat", re.I),
            },
        },
        "sorting_hat": {
            PRE_RESPONSE_PROCESSING: {
                "navi": get_navi_hint,
            },
            RESPONSE: "",
            TRANSITIONS: {
                ("second_year", "kings_cross"): cnd.exact_match(r"next", re.I),
            },
        },
    },
    "second_year": {
        "kings_cross": {
            RESPONSE: HARRY_SPEECH,
        },
    },
}
