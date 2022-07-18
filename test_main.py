import unittest

from app_vocabulary import home_page_description
from main import turn_handler, actor

testing_dialog = [
    ("start", home_page_description),
    ("1", "How can I help you?"),
    ("is it raining?", "Please rephrase your question.."),
    ("home", home_page_description),
    ("2", "Choose a model: ....."),
    ("I heard a lot about Lada Kalina", "Let me present you LADA KALINA....."),
    ("back", "Choose a model: ....."),
    ("ferrari", "\033[31mSorry, I couldn't find anything for this query\033[0m"),
]


# TODO: upgrade test scenario -> process a series of requests and check only final result
class TestHandler(unittest.TestCase):
    def test_turn_handler(self):
        ctx = {}
        for in_request, true_out_response in testing_dialog:
            out_response, ctx = turn_handler(in_request, ctx, actor)
            self.assertEqual(out_response.strip(), true_out_response.strip())


if __name__ == "__main":
    unittest.main()
