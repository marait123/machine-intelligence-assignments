from argparse import ArgumentDefaultsHelpFormatter
from os import stat
from threading import active_count
from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import math

inf = 1e14
# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state)

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.


def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[agent], None

    actionsmyStates = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action)
                           for index, (action, state) in enumerate(actionsmyStates))
    return value, action

# Apply Minimax search and return the tree value and the best action

# 'C:\Python39\python.exe' .\autograder.py -q 1
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE

    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[agent], None

    if max_depth == 0:
        heuristic(game,state, agent)
    if agent == 0:
        # max
        v = -inf
        maxAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            new_val,_ = minimax(game, game.get_successor(state, action),heuristic, max(-1,max_depth-1))
            if new_val > v:
                v=new_val
                maxAct = action
        return v, maxAct
    else:
        #min
        v = inf
        minAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            new_val,_ = minimax(game, game.get_successor(state, action),heuristic,  max(-1,max_depth-1))
            if new_val < v:
                v=new_val
                minAct = action
        return v, minAct

# Apply Alpha Beta pruning and return the tree value and the best action


def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action


def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()

# Apply Expectimax search and return the tree value and the best action


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()
