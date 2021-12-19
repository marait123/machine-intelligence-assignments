from argparse import ArgumentDefaultsHelpFormatter
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
    # game.get_turn()
    # side note to me : look at the greedy to understand how it all works
    def max_val(myState: S, level):
        # print("max_val now state is ", myState)
        agent = game.get_turn(myState)
        if max_depth != -1 and level == max_depth:
            # print(level , " level == max_depth heuristic is ",heuristic(game,myState, 1) )
            return heuristic(game,myState, agent)
        terminal, values = game.is_terminal(myState)
        if terminal:
            return values[agent]
        v = -inf
        for action in game.get_actions(myState):
            v = max(v, min_val(game.get_successor(myState, action),level+1))
        return 0

    def min_val(myState: S, level):
        # print(level," min_val  now  state is ", myState)
        
        agent = game.get_turn(myState)
        if max_depth != -1 and level == max_depth:
            # print(level, " level == max_depth heuristic is ",heuristic(game,myState, 0) )
            return heuristic(game,myState,agent )

        terminal, values = game.is_terminal(myState)
        if terminal:
            # print(level , " terminal heuristic is ",heuristic(game,myState, 1) )
            # return myState.value
            return values[agent]
        v = inf
        for action in game.get_actions(myState):
            # print("about to cal max_val")
            v = min(v, max_val(game.get_successor(myState, action),level+1))
        return v
    actions = game.get_actions(state)
    max_action = 0
    max_util = -inf
    for action in actions:
        util = min_val(game.get_successor(state, action),1)
        print("util is ", util)
        if util > max_util:
            max_util = util
            max_action = action

    # get the action that returns the maximum utilit
    return max_util, max_action

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
