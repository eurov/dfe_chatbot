import unittest
import random

from main import turn_handler, actor, db


requests = {
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
}


class TestHandler(unittest.TestCase):
    def test_dialog_paths(self):
        for name, scenario in requests.items():
            user_id = str(random.randint(0, 100))
            with self.subTest(name=name):
                out_response = None
                for request in scenario["path"]:
                    out_response, ctx = turn_handler(request, user_id, actor)
                if "expected_response" in scenario:
                    self.assertTrue(scenario["expected_response"] in out_response, name)
                self.assertEqual(ctx.last_label[1], scenario["expected_node"], name)
                db.clear()


if __name__ == "__main":
    unittest.main()
