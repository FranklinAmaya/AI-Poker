from pypokerengine.api.game import start_poker, setup_config
from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.engine.card import Card

import numpy as np


if __name__ == '__main__':

    community = [

        Card(Card.HEART, 12),

        Card(Card.DIAMOND, 11),

        Card(Card.HEART, 6),

        Card(Card.CLUB, 4),

        Card(Card.CLUB, 5)

        ]

    hole = [

        Card(Card.CLUB, 2),

        Card(Card.CLUB, 3)

        ]

    bit = HandEvaluator.eval_hand(hole, community)
    info = HandEvaluator.gen_hand_rank_info(hole, community)
    print(bit)
    print(info)



