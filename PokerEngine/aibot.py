from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards, estimate_hole_card_win_rate
import random



class AIPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"
    bluffing = False
    initial_stack = 100
    turn = 0
    prev_round = 0

    def declare_action(self, valid_actions, hole_card, round_state):
        # Useful variables
        win_rate = estimate_hole_card_win_rate(nb_simulation=1000, nb_player=2, hole_card=gen_cards(hole_card),
                                               community_card=gen_cards(round_state['community_card']))
        try:
            opponent_action_dict = round_state['action_histories'][round_state['street']][-1]
            print(round_state['street'])
        except:
            if round_state['street'] == 'turn':
                opponent_action_dict = round_state['action_histories']['flop'][-1]
            else:
                opponent_action_dict = round_state['action_histories']['preflop'][-1]

        pot_amount = round_state['pot']['main']['amount']
        ai_stack = [player['stack'] for player in round_state['seats'] if player['uuid'] == self.uuid][0]
        raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
        opponent_action = opponent_action_dict['action']

        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        amount = None

        if 'round_count' not in round_state.keys() and self.turn == 0:
            self.bluffing = False
        if 'round_count' in round_state.keys():
            if round_state['round_count'] != self.prev_round:
                self.prev_round = round_state['round_count']
                self.bluffing = False
                self.turn = 0
                print("Turn reset")


        print(round_state)
        print("Initial stack: " + str(self.initial_stack))

        # get evaluation score of hand
        print(round_state['street'])
        print("================================================")
        print("Turn: " + str(self.turn))
        if 'round_count' in round_state.keys():
            print("Round: " + str(round_state['round_count']))
        print("Prev Round: " + str(self.prev_round))
        print("Cards: " + str(hole_card))
        print("Win rate: " + str(win_rate))

        if opponent_action == "raise":
            print("Opponent raised.")
            if win_rate > .85:
                action = 'raise'
                amount = raise_amount_options['max']
            elif win_rate > .75:
                action = 'raise'
                amount = int(2 * (self.initial_stack / (ai_stack)) * (raise_amount_options['max'] - raise_amount_options['min']) + raise_amount_options['min'])
            elif win_rate > .45:
                action = 'call'
            else:
                if not self.bluffing:
                    randnum = random.uniform(0, 1)

                    if randnum > win_rate / 2:
                        action = 'fold'
                    elif can_call:
                        action = 'call'
                else:
                    print("AI bot: bluffing")
                    action = 'call'

        else:
            # raise less if opponent calls
            if win_rate > .85:
                action = 'raise'
                amount = int(2*(self.initial_stack/(ai_stack))*(raise_amount_options['max'] - raise_amount_options['min']) + raise_amount_options['min'])
            elif win_rate > .75:
                action = 'raise'
                amount = int(1.7*(self.initial_stack/(ai_stack))*(raise_amount_options['max'] - raise_amount_options['min']) + raise_amount_options['min'])
            elif win_rate > .45:
                action = 'call'
            else:
                if not self.bluffing:
                    randnum = random.uniform(0, 1)

                    if randnum > win_rate / 2:
                        action = 'fold'
                    elif randnum > win_rate / 4 and can_call:
                        action = 'call'
                    else:
                        print("AI bot: bluffing")

                        action = 'raise'
                        #small bluff
                        amount = int((ai_stack / self.initial_stack) / 4 * (raise_amount_options['max'] - raise_amount_options['min']))
                        amount += raise_amount_options['min']
                        self.bluffing = True
                else:
                    print("AI bot: bluffing")
                    action = 'raise'
                    amount = int((ai_stack / self.initial_stack) / 4 * (raise_amount_options['max'] - raise_amount_options['min']))
                    amount += raise_amount_options['min']

            print("Opponent called.")

        if amount is None:
            items = [item for item in valid_actions if item['action'] == action]
            amount = items[0]['amount']

        if amount < 0 or self.turn == 0:
            action = 'call'
            items = [item for item in valid_actions if item['action'] == action]
            amount = items[0]['amount']

            if win_rate < .25:
                action = 'fold'

        if action == "raise" and amount > raise_amount_options['max']:
            amount = raise_amount_options['max']
        if action == "raise" and amount < raise_amount_options['min']:
            amount = raise_amount_options['min']

        self.turn += 1
        print("AI bot: " + action)
        return action, amount

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