import numpy as np

class BlackjackEnv:
    def __init__(self):
        self.action_space = [0, 1]  # 0: Stand, 1: Hit
        self.reset()

    def reset(self, player_cards=None, dealer_card=None):
        if player_cards is not None and dealer_card is not None:
            self.player_hand = list(player_cards)
            self.dealer_hand = [dealer_card, self.draw_card()]
        else:
            self.player_hand = [self.draw_card(), self.draw_card()]
            self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.done = False
        return self.get_state()

    def draw_card(self):
        return min(np.random.randint(1, 14), 10)

    def get_state(self):
        player_total = self.calculate_hand(self.player_hand)
        dealer_show = self.dealer_hand[0]
        usable_ace = int(1 in self.player_hand and player_total <= 11)
        return (player_total, dealer_show, usable_ace)

    def calculate_hand(self, hand):
        total = sum(hand)
        if 1 in hand and total <= 11:
            total += 10
        return total

    def step(self, action):
        if action == 1:  # Hit
            self.player_hand.append(self.draw_card())
            if self.calculate_hand(self.player_hand) > 21:
                self.done = True
                return self.get_state(), -1, self.done
            return self.get_state(), 0, self.done

        # Dealer's turn
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())

        player_total = self.calculate_hand(self.player_hand)
        dealer_total = self.calculate_hand(self.dealer_hand)
        self.done = True

        if dealer_total > 21:
            return self.get_state(), 1, self.done
        elif player_total > dealer_total:
            return self.get_state(), 1, self.done
        elif player_total < dealer_total:
            return self.get_state(), -1, self.done
        else:
            return self.get_state(), 0, self.done


def simulate_single_scenario(env, p1, p2, dealer_card, n_sim=1000):
    results = []
    player_hand = [p1, p2]
    has_ace = 1 in player_hand
    ace_scenarios = [(False, player_hand)]
    if has_ace:
        # Two scenarios: Ace as 1 and Ace as 11
        ace_scenarios = [(False, player_hand)]
        hand_11 = [11 if c == 1 else c for c in player_hand]
        ace_scenarios.append((True, hand_11))

    for ace_as_11, hand in ace_scenarios:
        for action in [0, 1]:  # 0: Stand, 1: Hit
            win = 0
            lose = 0
            draw = 0
            for _ in range(n_sim):
                # Reset with a copy of the hand
                if ace_as_11:
                    # For Ace as 11: convert 11s back to 1 for reset, then manually set one Ace to 11
                    reset_hand = [1 if c == 11 else c for c in hand]
                    env.reset(tuple(reset_hand), dealer_card)
                    for i in range(len(env.player_hand)):
                        if env.player_hand[i] == 1:
                            env.player_hand[i] = 11
                            break
                else:
                    env.reset(tuple(hand), dealer_card)
                if action == 0:
                    env.done = False
                    while env.calculate_hand(env.dealer_hand) < 17:
                        env.dealer_hand.append(env.draw_card())
                    player_total = sum(env.player_hand)
                    if has_ace and ace_as_11:
                        if player_total > 21 and 11 in env.player_hand:
                            idx = env.player_hand.index(11)
                            env.player_hand[idx] = 1
                            player_total = sum(env.player_hand)
                    dealer_total = env.calculate_hand(env.dealer_hand)
                    if dealer_total > 21:
                        win += 1
                    elif player_total > dealer_total:
                        win += 1
                    elif player_total < dealer_total:
                        lose += 1
                    else:
                        draw += 1
                else:
                    env.player_hand.append(env.draw_card())
                    player_total = sum(env.player_hand)
                    if has_ace and ace_as_11:
                        if player_total > 21 and 11 in env.player_hand:
                            idx = env.player_hand.index(11)
                            env.player_hand[idx] = 1
                            player_total = sum(env.player_hand)
                    if player_total > 21:
                        lose += 1
                        continue
                    while env.calculate_hand(env.dealer_hand) < 17:
                        env.dealer_hand.append(env.draw_card())
                    dealer_total = env.calculate_hand(env.dealer_hand)
                    if dealer_total > 21:
                        win += 1
                    elif player_total > dealer_total:
                        win += 1
                    elif player_total < dealer_total:
                        lose += 1
                    else:
                        draw += 1
            results.append({
                'action': 'stand' if action == 0 else 'hit',
                'win_rate': win / n_sim,
                'lose_rate': lose / n_sim,
                'draw_rate': draw / n_sim,
                'win': win,
                'lose': lose,
                'draw': draw,
                'ace_as_11': ace_as_11,
                'has_ace': has_ace
            })
    return results



if __name__ == "__main__":
    env = BlackjackEnv()
    print("Enter your first card (1-10, Ace as 1): ", end="")
    p1 = int(input())
    print("Enter your second card (1-10, Ace as 1): ", end="")
    p2 = int(input())
    print("Enter the dealer's visible card (1-10, Ace as 1): ", end="")
    dealer_card = int(input())
    print(f"\nSimulating 1000 games for Player [{p1}, {p2}] vs Dealer [{dealer_card}, ?]...\n")
    results = simulate_single_scenario(env, p1, p2, dealer_card, n_sim=1000)

    # Find the best win rate and best (lowest) lose rate
    max_win = max(r['win_rate'] for r in results)
    min_lose = min(r['lose_rate'] for r in results)

    print("Action  |  Win %  |  Lose %  |  Draw %  |  Ace Usage   |  Note")
    print("---------------------------------------------------------------")
    for r in results:
        if r.get('has_ace', False):
            ace_str = 'Ace as 11' if r.get('ace_as_11', False) else 'Ace as 1'
        else:
            ace_str = '-'
        note = ""
        if abs(r['win_rate'] - max_win) < 1e-8:
            note += " [33m★[0m"  # Gold star
        if abs(r['lose_rate'] - min_lose) < 1e-8:
            note += " [37m☆[0m"  # Silver star
        print(f"{r['action']:6}  |  {r['win_rate']*100:6.1f}  |  {r['lose_rate']*100:7.1f}  |  {r['draw_rate']*100:7.1f}  |  {ace_str:10} |{note}")