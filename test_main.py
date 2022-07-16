import unittest
from main import turn_handler, actor

testing_dialog = [
    (
        "home",
        """
    ----------------------------------------------------
    You are welcomed by the online assistant of AVTOVAZ
    ----------------------------------------------------

    Choose an option:

    [1] > Contact the operator 
    [2] > Our models
    [3] > Sign up for a test drive
    [4] > Find a dealer
    [5] > Assistance service
    [help] > Chat navigation

    """,
    ),
    ("1", "How can I help you?")
    # ("i'm fine, how are you?", "Good. What do you want to talk about?"),
    # ("talk about music.", "I love `System of a Down` group, would you like to tell about it? "),
    # ("yes", "System of a Downis an Armenian-American heavy metal band formed in in 1994."),
    # ("next", "The band achieved commercial success with the release of five studio albums."),
    # ("back", "System of a Downis an Armenian-American heavy metal band formed in in 1994."),
    # ("repeat", "System of a Downis an Armenian-American heavy metal band formed in in 1994."),
    # ("next", "The band achieved commercial success with the release of five studio albums."),
]


class TestHandler(unittest.TestCase):
    def test_turn_handler(self):
        ctx = {}
        for in_request, true_out_response in testing_dialog:
            out_response, ctx = turn_handler(in_request, ctx, actor)
            self.assertEqual(out_response.strip(), true_out_response.strip())


if __name__ == "__main":
    unittest.main()
