import unittest
from main import turn_handler, actor


testing_dialog = [  # collect a scenario

]


def run_test():  # origin approach
    ctx = {}
    for in_request, true_out_response in testing_dialog:
        _, ctx = turn_handler(in_request, ctx, actor, true_out_response=true_out_response)


class TestHandler(unittest.TestCase):
    def test_turn_handler(self):
        ctx = {}
        for in_request, true_out_response in testing_dialog:
            self.assertEqual(turn_handler(in_request, ctx, actor), true_out_response)


if __name__ == '__main':
    unittest.main()
    # run_test()
