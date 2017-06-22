from ask_amy.tests.utility import TestCaseASKAmy
from ask_amy.core.reply import Reply, Card


class TestReply(TestCaseASKAmy):
    def setUp(self):
        pass

    def test_card_simple(self):
        card = Card.simple('title','some content')
        print(card)

    def test_build_w_card(self):
        pass