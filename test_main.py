import unittest
import random
from collections import OrderedDict

from main import turn_handler, ACTOR, db


new_user_requests = {
    "first_scenario": {
        "path": ["hi"],
        "expected_response": "Hello, Muggle!",
        "expected_node": "start_node",
    },
    "second_scenario": {
        "path": ["hi", "help"],
        "expected_response": "course of the dialogue",
        "expected_node": "start_node",
    },
    "third_scenario": {
        "path": ["hi", "start"],
        "expected_response": "Mr.Ollivander has prepared",
        "expected_node": "ollivander_shop",
    },
    "forth_scenario": {
        "path": ["hi", "start", "help"],
        "expected_response": "You are not a wizard without a wand!",
        "expected_node": "ollivander_shop",
    },
    "fifth_scenario": {
        "path": ["hi", "start", "1"],
        "expected_response": "I see you've got the stuff.",
        "expected_node": "hogwarts_school",
    },
    "sixth_scenario": {
        "path": ["hi", "start", "1", "hat"],
        "expected_response": "Congrats!",
        "expected_node": "sorting_hat",
    },
    "seventh_scenario": {
        "path": ["hi", "start", "1", "hat", "next"],
        "expected_response": "Yo, buddy!",
        "expected_node": "platform 9¾",
    },
    "eighth_scenario": {
        "path": ["hi", "start", "1", "hat", "next", "blabla"],
        "expected_response": "Avada Kedavra!",
        "expected_node": "fallback_node",
    },
    "ninth_scenario": {
        "path": ["hi", "start", "1", "hat", "next", "back"],
        "expected_response": "Congrats",
        "expected_node": "sorting_hat",
    },
}

known_user_requests = OrderedDict(
    [
        (
            "fill_misc",
            {
                "path": ["hi", "start", "1", "hat", "next"],
                "expected_response": "Yo, buddy!",
                "expected_node": "platform 9¾",
            },
        ),
        (
            "first_scenario",
            {
                "path": ["hi"],
                "expected_response": "Glad to see you again!",
                "expected_node": "start_node",
            },
        ),
        (
            "second_scenario",
            {
                "path": ["hi", "start"],
                "expected_response": "Yo, buddy!",
                "expected_node": "platform 9¾",
            },
        ),
    ]
)


class TestHandler(unittest.TestCase):
    def test_new_user(self) -> None:
        for name, scenario in new_user_requests.items():
            user_id = str(random.randint(0, 100))
            with self.subTest(name=name):
                out_response = None
                for request in scenario["path"]:
                    out_response, ctx = turn_handler(request, user_id, ACTOR)
                if "expected_response" in scenario:
                    self.assertTrue(scenario["expected_response"] in out_response, name)
                self.assertEqual(ctx.last_label[1], scenario["expected_node"], name)
                db.clear()

    def test_known_user(self) -> None:
        for name, scenario in known_user_requests.items():
            user_id = "1000"
            with self.subTest(name=name):
                out_response = None
                for request in scenario["path"]:
                    out_response, ctx = turn_handler(request, user_id, ACTOR)
                if "expected_response" in scenario:
                    self.assertTrue(scenario["expected_response"] in out_response, name)
                self.assertEqual(ctx.last_label[1], scenario["expected_node"], name)


if __name__ == "__main__":
    unittest.main()
