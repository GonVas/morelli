import datetime
from random import choice
from math import log, sqrt
from copy import deepcopy, copy

import pprint

class DecisionNode:

    def __init__(self, node, depth, dad):
        self.node = init_node
        self.depth = depth
        self.dad = dad
        self.wins = 0
        self.plays = 0
        self.children = None

    def get_root(self):
        node_dad = self.dad
        while(node_dad is not None):
            node_dad = self.dad
        return node_dad

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
            (self.wins.get((player, id(S)), 0) /
             self.plays.get((player, id(S)), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, id(S)), 0) /
              self.plays.get((player, id(S)), 1),
              self.wins.get((player, id(S)), 0),
              self.plays.get((player, id(S)), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return move

    def selection(self, decision_tree):


        moved_states = []
        for legal_play in state.avaiable_moves(self.me_player, flat=True):
            moved_states.append( (legal_play, MonteCarlo.next_state(state, legal_play)))

        decision_node.children


        have_all_plays = True
        for moved_state in moved_states:
            if ( (player, id(moved_state)) not in plays) or plays[(player, id(moved_state))] == 0:
                have_all_plays = False

        if(have_all_plays):
            log_total = sum(
                plays[(player, id(S))] for p, S in moved_states)

            v_m_s = max(
                ((wins[(player, id(S))] / plays[(player, id(S))] + 1) +
                 self.ucb_C * sqrt(log_total / plays[(player, id(S))]), p, S)
                for p, S in moved_states
            )
            value, move, state = v_m_s
        else:
            # Otherwise, just make an arbitrary decision.
            move, state = choice(moved_states)

        return node

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.

        decision_tree = DecisionNode('root', 0, None)






        visited_states = set()
        states_copy = self.states[:]
        board = states_copy[-1]
        player = str(state.current_player())

        expand = True
        for t in range(1, self.max_moves + 1):

            legal = state.avaiable_moves(self.me_player, flat=True)

            node = self.select_node(decision_tree)














            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, id(state)) not in plays:
                expand = False
                plays[(player, id(state))] = 0
                wins[(player, id(state))] = 0
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
            if (player, id(state)) not in plays:
                continue
            plays[(player, id(state))] += 1
            if player == winner:
                wins[(player, id(state))] += 1

    @staticmethod
    def next_state(board, move):
  #      print("before board: BBBBBBBBB\n")
  #      board.print()
  #      print("BEFOR BOARD PRINTED\n")

        next_board = board.move(move[0], move[1], destructive=False ) 
  #      next_board.print()
        return next_board




'''
            if all(plays.get((player, S)) for p, S in moved_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moved_states))


                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.ucb_C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moved_states
                )
'''