from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards, estimate_hole_card_win_rate
import random


class AIPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    def get_past_action(self, round_state):
        return round_state['action_histories'][round_state['street']][-1]

    def declare_action(self, valid_actions, hole_card, round_state):
        
        # get evaluation score of hand
        print("================================================")
        print("Cards: " + str(hole_card))
        win_rate = estimate_hole_card_win_rate(nb_simulation=1000, nb_player=2, hole_card=gen_cards(hole_card), community_card=gen_cards(round_state['community_card']))
        print("Win rate: " + str(win_rate))
        print(self.uuid)

        try:
            opponent_action_dict = round_state['action_histories'][round_state['street']][-1]
            print(round_state['street'])
        except:
            if round_state['street'] == 'turn':
                opponent_action_dict = round_state['action_histories']['flop'][-1]
            else:
                opponent_action_dict = round_state['action_histories']['preflop'][-1]

        print(round_state['action_histories'])
        print(opponent_action_dict['action'])


        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        amount = None

        # If the win rate is large enough, then raise
        if win_rate > 0.5:
            raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
            if win_rate > 0.85:
                # If it is extremely likely to win, then raise as much as possible
                action = 'raise'
                amount = raise_amount_options['max']
            elif win_rate > 0.75:
                # If it is likely to win, then raise by the minimum amount possible
                action = 'raise'
                amount = raise_amount_options['min']

            else:
                # If there is a chance to win, then call
                action = 'call'

        elif round_state['street'] == 'preflop' and win_rate >= 0.4:
            action = 'call'

        else:
            if opponent_action_dict['action'] == 'raise':
                win_rate*= 2/3

            randnum = random.uniform(0,1)
            if randnum > win_rate:
                action = 'fold'
            elif randnum < win_rate/2
                if can_call:
                    action = 'call'
            else:
                action = 'raise'
                amount = raise_amount_options['min']
                print(round_state['pot']['main']['amount'])
            #action = 'call' if can_call and call_amount == 0 else 'fold'

        # Set the amount
        if amount is None:
            items = [item for item in valid_actions if item['action'] == action]
            amount = items[0]['amount']

        '''
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"] '''
        return action, amount  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        self.n_players = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        '''
        is_winner = self.uuid in [item['uuid'] for item in winners]
        self.wins += int(is_winner)
        self.losses += int(not is_winner)
        '''
        pass


def setup_ai():
    return AIPlayer()