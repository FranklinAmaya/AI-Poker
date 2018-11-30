from pypokerengine.api.game import start_poker, setup_config

from aibot import AIPlayer
import numpy as np

if __name__ == '__main__':
    ai_bot = AIPlayer()

    # The stack log contains the stacks of the Data Blogger bot after each game (the initial stack is 100)
    stack_log = []
    for round in range(1000):
        p1 = ai_bot

        config = setup_config(max_round=5, initial_stack=100, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == ai_bot.uuid])
        print('Avg. stack:', '%d' % (int(np.mean(stack_log))))