import re

import df_engine.conditions as cnd
import df_engine.labels as lbl
from app_tools import (
    get_help,
    save_session_history,
    home_page,
    operator_custom_transfer,
    operator_transfer_confirmation,
    get_history,
    operator_clarifying_question,
)
from df_engine.core.keywords import (
    TRANSITIONS,
    RESPONSE,
    GLOBAL,
    PRE_RESPONSE_PROCESSING,
)


script = {
    "root": {
        "start_node": {
            RESPONSE: home_page,
            TRANSITIONS: {
                ("operator_flow", "reception_node"): cnd.exact_match("1"),
                ("models_flow", "node1"): cnd.exact_match("2"),
                ("test_drive_flow", "node1"): cnd.exact_match("3"),
                ("dealer_flow", "node1"): cnd.exact_match("4"),
                ("service_flow", "node1"): cnd.exact_match("5"),
            },
        },
        "fallback_node": {
            RESPONSE: "\033[31mSorry, I couldn't find anything for this query\033[0m"
        },
    },
    GLOBAL: {
        PRE_RESPONSE_PROCESSING: {
            "logbook": save_session_history,
            "help": get_help,
            "history": get_history,
        },
        TRANSITIONS: {
            lbl.to_start(): cnd.regexp(r"home|start|hello|hi", re.I),
            lbl.repeat(1.1): cnd.regexp(r"help|history", re.I),
            lbl.previous(): cnd.regexp(r"back", re.I),
        },
    },
    "operator_flow": {
        "reception_node": {
            PRE_RESPONSE_PROCESSING: {
                "clarifying_question": operator_clarifying_question,
            },
            RESPONSE: "How can I help you?",
            TRANSITIONS: {
                lbl.forward(): cnd.regexp(r"model|drive|dealer|service", re.I),
                lbl.repeat(0.9): cnd.true(),
            },
        },
        "request_confirmation_node": {
            PRE_RESPONSE_PROCESSING: {
                "transfer_confirmation": operator_transfer_confirmation,
            },
            RESPONSE: "",
            TRANSITIONS: {
                operator_custom_transfer: cnd.regexp(r"y|n", re.I),
            },
        },
    },
    "models_flow": {
        "node1": {
            RESPONSE: "Choose a model: .....",  # TODO: add a list of models
            TRANSITIONS: {
                "node2": cnd.regexp(r"granta", re.I),
                "node3": cnd.regexp(r"kalina", re.I),
            },
        },
        "node2": {
            RESPONSE: "Let me present you LADA GRANTA....",  # TODO: add info about models
            TRANSITIONS: {lbl.forward(): cnd.regexp(r"next", re.I)},
        },
        "node3": {
            RESPONSE: "Let me present you LADA KALINA....."
        },  # returns info about model #2
    },
    "test_drive_flow": {
        "node1": {
            RESPONSE: "Let's find the nearest available date for a test drive!",  # TODO: add sign up form
            TRANSITIONS: {},
        },
    },
    "dealer_flow": {
        "node1": {
            RESPONSE: "Here is the list of dealer addresses .....",  # TODO: add info
        },
    },
    "service_flow": {
        "node1": {
            RESPONSE: "Tell us ",  # hot-line
        },
    },
}
