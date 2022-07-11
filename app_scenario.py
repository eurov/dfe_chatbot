import re

import df_engine.conditions as cnd
import df_engine.labels as lbl
from app_tools import show_help, save_session_history, get_session_history, home_page
from df_engine.core.keywords import TRANSITIONS, RESPONSE, GLOBAL, PRE_RESPONSE_PROCESSING


script = {
    "root": {
        "start_node": {
            RESPONSE: home_page,
            TRANSITIONS: {
                ("operator_flow", "node1"): cnd.exact_match("1"),
                ("models_flow", "node1"): cnd.exact_match("2"),
            }
        },
        "fallback_node": {  # We get to this node if an error occurred while the agent was running
            RESPONSE: "\033[31m YOU FUCKED UP",
        },
    },
    GLOBAL: {
        PRE_RESPONSE_PROCESSING: {
            # "service_label": add_label(),
            "logbook": save_session_history,
        },
        TRANSITIONS: {
            # determine_next_label: cnd.true(),
            lbl.to_start(): cnd.regexp(r"home", re.I),
            lbl.previous(): cnd.regexp(r"back", re.I),
            ("help_flow", "help_node"): cnd.regexp(r"help", re.I),
            ("help_flow", "history_node"): cnd.regexp(r"history", re.I),
        },
    },
    "help_flow": {
        "help_node": {
            RESPONSE: show_help,
        },
        "history_node": {
            RESPONSE: get_session_history,
        },
    },
    "operator_flow": {
        "node1": {
            RESPONSE: "Hi! How can I help you?",
            TRANSITIONS: {
                # determine_next_label: cnd.true(),  # to init handler
            },
        },
        # "node2": {
        #     RESPONSE: "Is this what you're looking for? [y / n]",
        #     TRANSITIONS: {
        #         ("some_flow", "some_node"): cnd.regexp(r"y", re.I),
        #         lbl.previous(): cnd.regexp(r"n", re.I),
        #     },
        # }
    },
    "models_flow": {
        "node1": {
            RESPONSE: 'Choose a model: .....',  # returns a list of models
            # TRANSITIONS: {
            #     "model_node": cnd.regexp(r"some model", re.IGNORECASE),
            # },
        },
        # "node2": {
        #     RESPONSE: 'Model .....',  # returns info about model #1
        #     TRANSITIONS: {
        #         "model_node": cnd.regexp(r"some model", re.IGNORECASE),
        #     },
        # },
    },
}
