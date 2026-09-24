
##
# Mastermind Solver
# Klasse: Knuth
# Methoden: get_next_guess, update_possible_codes
# Usage Example:
#
# from mastermind_solver import Knuth
# solver = Knuth()
#
# next_guess = solver.get_next_guess()
#
# # next_guess (rateversuch) an den Server senden
# # solver aktuallisieren..
# solver.update_possible_codes(next_guess, b, w)
# 
# # widerholen (get_next_guess, update_possible_codes...) bis die Lösung gefunden ist

from collections import defaultdict

# Implementation of Donald Knuth solver algorithm according to https://en.wikipedia.org/wiki/Mastermind_(board_game)

# internal helper which reports correct position and color for a guess compared to an assumption.
# used to update (remove) codes from whole set
def checker(guess, assumption):
    # correct position and color
    correct_position = 0
    for i in range(4):
        if (guess[i] == assumption[i]):
            correct_position = correct_position + 1
    
    # correct color
    correct_color = 0
    for i in range(1, 7):
        assumption_count = assumption.count(i)
        guess_count = guess.count(i)
        correct_color = correct_color + min(assumption_count, guess_count)
    
    correct_color = correct_color - correct_position
    return [correct_position, correct_color]


class Knuth:

    # initialize the solver algorithm
    # 1. create the set of possible codes (1111, 1112, ... 6666)
    def __init__(self):
        self.S = []
        for a in range(1, 7):
            for b in range(1, 7):
                for c in range(1, 7):
                    for d in range(1, 7):
                        self.S.append([a, b, c, d])
        self.next_guess = [1, 1, 2, 2]

    # get the next guess which should be sent to the Server
    def get_next_guess(self):
        return self.next_guess
    
    # update the internal list of possible codes
    # guess: played guess
    # b: black (correct position and color)
    # w: white (correct color)
    def update_possible_codes(self, guess, b, w):
        next_S = []
        for s in self.S:
            assumption_b, assumption_w = checker(guess, s)
            if (assumption_b == b) and (assumption_w == w):
                # keep this value
                next_S.append(s)    
        self.S = next_S
        print(f"S has {len(self.S)} items")
        self._calculate_next_guess()

    # internal: calculate the next guess
    #
    # loop over the set (S) and guess each code,
    # compare them with each value in the set (S) (assume that it is the true value)
    def _calculate_next_guess(self):
        guesses_worst_score = []
        for guess in self.S:
            scores = dict()
            for assume in self.S:
                b, w = checker(guess, assume)
                key = f"{b}{w}"
                # count the number of same b,w for this guess (score)
                if (key in scores):
                    scores[key] += 1
                else:
                    scores[key] = 1

            guesses_worst_score.append([guess, max(scores.values())])
        # minimum is the best score...
        self.next_guess = min(guesses_worst_score, key=lambda p:p[1])[0]

