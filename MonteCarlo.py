import datetime
from random import choice
from math import log, sqrt
from copy import deepcopy, copy
import time
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
    def __init__(self, board, player, max_time, ucb_C=1.4, max_moves=120):
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
        self.states = []
        self.wins = {}
        self.plays = {}

    def update(self, state):
        # Takes a game state, and appends it to the history.
         self.states.append(state)

    def clean_records(self, visited_states):

        new_wins = {}
        for key, item in self.wins.items():
            new_key = (key[0], key[1][0:-1])
            new_wins[new_key] = item
        self.wins = new_wins

        new_plays = {}
        for key, item in self.plays.items():
            new_key = (key[0], key[1][0:-1])
            new_plays[new_key] = item
        self.plays = new_plays

        new_visited_states = []
        for key, item in visited_states:
            new_item = item[0:-1]
            new_visited_states.append([key, new_item])
        visited_states = new_visited_states

        return new_visited_states


    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = deepcopy(self.states[-1])
        player = str(state.current_player())
        legal = state.avaiable_moves(state.current_player(), flat=True) #self.curr_player.aval_moves(self.board[:])

        # Bail out early if there is no real choice to be made.
        if len(legal) == 0:
            print('Legal is None')
            return
        if len(legal) == 1:
            print('Legal is 1')
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while games < 3:
            self.run_simulation()
            games += 1
            print('Ran a game simulation')

        #moves_states = [(p, MonteCarlo.next_state(state, p).get_state()) for p in legal]

        moves_states = []
        copy_old_state = deepcopy(state)
        for play in state.avaiable_moves(state.current_player(), flat=True):
            state.move(play[0], play[1], destructive=True) 
            #print('Moved (%d, %d) to (%d, %d) state : %s' % (play[0].pos[0], play[0].pos[1], play[1].pos[0], play[1].pos[1], state.get_state()  ))
            moves_states.append( [play, state.get_state()])
            state = deepcopy(copy_old_state)


        print(games, datetime.datetime.utcnow() - begin)

        moves_states = self.clean_records(moves_states)
        
        record = [-1, None]
        for play, sta in moves_states:
            if((player, sta) in self.wins):
                per_win = self.wins[(player, sta)]/self.plays[(player, sta)]
                if(per_win > record[0]):
                    record = [per_win, play]

        if(record[0] == None):
            print('Not found in records')
            return legal[0]

        # Display the stats for each possible play.
      #  for x in sorted(
       #     ((100 * self.wins.get((player, S), 0) /
        #      self.plays.get((player, S), 1),
         #     self.wins.get((player, S), 0),
          #    self.plays.get((player, S), 0), p)
           #  for p, S in moves_states),
            #reverse=True
        #):
         #   print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        #print("Maximum depth searched:", self.max_depth)

        return record[1]

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
        visited_states = set()
        states_copy = [deepcopy(s) for s in self.states]

        state = states_copy[-1]
        player = str(state.current_player())

        expand = True
        first_time = True

        for t in range(self.max_moves):
            legal = state.avaiable_moves(state.current_player(), flat = True)

            #print('Length of legal %d' % (len(legal)))
            
            winner = state.check_winning()
            if winner:
                winner = str(winner)
                print('Got a Winner: ' + winner)
                break

            play = choice(legal)
            
            #old_state = state.get_state()
            #state = self.next_state(state, play)
            #print('Is equal? ' + str(old_state==state.get_state()))
            state.move(play[0], play[1], destructive=True) 

            states_copy.append(state.get_state())

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state.get_state()) not in self.plays:
                expand = False
                self.plays[(player, state.get_state())] = 0
                self.wins[(player, state.get_state())] = 0

            visited_states.add((player, state.get_state()))

            player = str(state.current_player())

        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] += 1
            elif winner == 'tie':
                self.wins[(player, state)] -= 1


    @staticmethod
    def next_state(board, move):
        next_board = board.move(move[0], move[1], destructive=False ) 
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



"""
    def run_simulation(self):
            legal = self.board.legal_plays(states_copy)

            play = choice(legal)
            state = self.board.next_state(state, play)
            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

            visited_states.add((player, state))

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            if winner:
                break

            for player, state in visited_states:
                if (player, state) not in self.plays:
                    continue
                self.plays[(player, state)] += 1
                if player == winner:
                    self.wins[(player, state)] += 1
"""