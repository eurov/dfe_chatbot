import unittest
import uuid
from collections import OrderedDict

from main import db
from df_runner import Pipeline

from scenario import script

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
        "expected_node": "kings_cross",
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
                "expected_node": "kings_cross",
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
                "expected_node": "kings_cross",
            },
        ),
    ]
)


pipeline = Pipeline.from_script(
    script=script,
    start_label=("root", "start_node"),
    fallback_label=("root", "fallback_node"),
    context_db=db,
)


class TestRunner(unittest.TestCase):
    def execute_scenario(self, pipeline, name, scenario, ctx_id=None):
        ctx = None
        if not ctx_id:
            ctx_id = uuid.uuid4()
        out_response = None
        for request in scenario["path"]:
            ctx = pipeline(request, ctx_id)
            out_response = ctx.last_response
        if "expected_response" in scenario:
            self.assertIn(scenario["expected_response"], out_response, name)
        self.assertEqual(ctx.last_label[1], scenario["expected_node"], name)

    def test_run_for_new_user(self):
        for name, scenario in new_user_requests.items():
            with self.subTest(name):
                self.execute_scenario(pipeline, name, scenario)

    def test_run_for_known_user(self):
        ctx_id = uuid.uuid4()
        for name, scenario in known_user_requests.items():
            with self.subTest(name):
                self.execute_scenario(pipeline, name, scenario, ctx_id)


if __name__ == "__main__":
    unittest.main()
