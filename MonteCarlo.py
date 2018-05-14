import datetime
from random import choice
from math import log, sqrt
from copy import deepcopy, copy

import pprint

class MonteCarlo:
    def __init__(self, board, player, max_time, ucb_C=1.4, max_moves=500):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.max_moves = max_moves
        self.ucb_C = ucb_C
        self.board = board
        self.me_player = player
        #self.other_player = other
        #self.players = [player, other
        self.calculation_time = datetime.timedelta(seconds=max_time)
        self.states = [board]
        self.wins = {}
        self.plays = {}

    def update(self, state):
        # Takes a game state, and appends it to the history.
         self.states.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.states[-1]
        legal = state.avaiable_moves(self.me_player, flat=True) #self.curr_player.aval_moves(self.board[:])

        # Bail out early if there is no real choice to be made.
        if len(legal) == 0:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(p, MonteCarlo.next_state(state, p)) for p in legal]

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        print(games, datetime.datetime.utcnow() - begin)

        # Pick the move with the highest percentage of wins.
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return move
        
    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = state.current_player()
 
        expand = True
        for t in range(1, self.max_moves + 1):
            legal = state.avaiable_moves(self.me_player, flat=True)

            #moves_states = [(p, MonteCarlo.next_state(state, p)) for p in legal]

            moves_states = []
            for legal_play in legal:
                moves_states.append( (legal_play, MonteCarlo.next_state(state, legal_play)))


            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.ucb_C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = choice(moves_states)

            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            player = state.current_player()
            
            winner = None
            for possible_state in states_copy:
                temp = possible_state.check_winning()
                if( temp != None):
                    winner = temp

            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] += 1

    @staticmethod
    def next_state(board, move):
  #      print("before board: BBBBBBBBB\n")
  #      board.print()
  #      print("BEFOR BOARD PRINTED\n")

        next_board = board.move(move[0], move[1], destructive=False ) 
  #      next_board.print()
        return next_board
