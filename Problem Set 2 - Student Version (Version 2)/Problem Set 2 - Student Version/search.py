from argparse import ArgumentDefaultsHelpFormatter
from os import stat
from threading import active_count
from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import math
# set inf as the 10^14
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


def myminimax(initialAgent, game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1):
    # get the player whose turn is now
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    # if reached a terminal node return the
    # the value of the terminal state
    if terminal:
        return values[initialAgent], None

    # if you reached the maximum depth you can get to
    # then we must return a heuristic at the nodes of this level
    if max_depth == 0:
        return heuristic(game, state, initialAgent), None
    if agent == 0:
        # max node calculations
        v = -inf
        maxAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            new_val, _ = myminimax(initialAgent, game, game.get_successor(
                state, action), heuristic, max(-1, max_depth-1))
            if new_val > v:
                v = new_val
                maxAct = action
        return v, maxAct
    else:
        # min node calculations
        v = inf
        minAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            # the max(-1, max_depth-1) insures that max depth isn't below -1
            # so that I know when it reached zero
            new_val, _ = myminimax(initialAgent, game, game.get_successor(
                state, action), heuristic,  max(-1, max_depth-1))
            if new_val < v:
                v = new_val
                minAct = action
        return v, minAct
# 'C:\Python39\python.exe' .\autograder.py -q 1


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    agent = game.get_turn(state)
    return myminimax(agent, game, state, heuristic, max_depth)

# Apply Alpha Beta pruning and return the tree value and the best action


def myalphabeta(iagent, alpha, beta, game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1):
    # get the player whose turn is now
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)

    if terminal:
        # return the value for the inital agent
        # as if it was a monster's turn it will try to minimze the player's reward
        # if it was a player it will try to maximize it's reward
        return values[iagent], None

    if max_depth == 0:
        return heuristic(game, state, iagent), None
    if agent == 0:
        # max
        v = -inf
        maxAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            new_val, _ = myalphabeta(iagent, alpha, beta, game, game.get_successor(
                state, action), heuristic, max(-1, max_depth-1))
            if new_val > v:
                v = new_val
                maxAct = action
            if v >= beta:
                break
            alpha = max(alpha, v)
        return v, maxAct
    else:
        # min
        v = inf
        minAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            new_val, _ = myalphabeta(iagent, alpha, beta, game, game.get_successor(
                state, action), heuristic,  max(-1, max_depth-1))
            if new_val < v:
                v = new_val
                minAct = action
            if v <= alpha:
                break
            beta = min(beta, v)
        return v, minAct


def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    agent = game.get_turn(state)
    return myalphabeta(agent, -inf, inf,  game, state, heuristic, max_depth)

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action


def myalphabeta_ordering(iagent, alpha, beta, game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1):
    # the code for alpha beta ordering is the same as minimax
    # with the extra checks on alpha and beta
    # get the player whose turn is now
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)

    if terminal:
        # return the value for the inital agent
        # as if it was a monster's turn it will try to minimze the player's reward
        # if it was a player it will try to maximize it's reward
        return values[iagent], None

    if max_depth == 0:
        return heuristic(game, state, iagent), None
    if agent == 0:
        # max
        v = -inf
        maxAct = None
        allActions = game.get_actions(state)
        # sort all actions descending based on heuristic
        # always go for the action that maximizes your reward
        allActions.sort(reverse=True, key=lambda action: heuristic(game, game.get_successor(
            state, action), iagent))
        for action in allActions:
            new_val, _ = myalphabeta_ordering(iagent, alpha, beta, game, game.get_successor(
                state, action), heuristic, max(-1, max_depth-1))
            if new_val > v:
                v = new_val
                maxAct = action
            if v >= beta:
                break  # prune
            alpha = max(alpha, v)
        return v, maxAct
    else:
        # min
        v = inf
        minAct = None
        allActions = game.get_actions(state)
        # sort all actions descending based on heuristic
        # always go for the action that maximizes your reward
        allActions.sort(reverse=True, key=lambda action: heuristic(game, game.get_successor(
            state, action), agent))
        for action in allActions:
            new_val, _ = myalphabeta_ordering(iagent, alpha, beta, game, game.get_successor(
                state, action), heuristic,  max(-1, max_depth-1))
            if new_val < v:
                v = new_val
                minAct = action
            if v <= alpha:
                break  # prune
            beta = min(beta, v)
        return v, minAct


def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    agent = game.get_turn(state)
    return myalphabeta_ordering(agent, -inf, inf,  game, state, heuristic, max_depth)

# Apply Expectimax search and return the tree value and the best action


def myexpectimax(iagent, alpha, beta, game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1):
    # get the player whose turn is now
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)

    if terminal:
        # return the value for the inital agent
        # as if it was a monster's turn it will try to minimze the player's reward
        # if it was a player it will try to maximize it's reward
        return values[iagent], None

    if max_depth == 0:
        return heuristic(game, state, iagent), None
    if agent == 0:
        # max node
        v = -inf
        maxAct = None
        allActions = game.get_actions(state)
        for action in allActions:
            new_val, _ = myexpectimax(iagent, alpha, beta, game, game.get_successor(
                state, action), heuristic, max(-1, max_depth-1))
            if new_val > v:
                v = new_val
                maxAct = action
            if v >= beta:
                break
            alpha = max(alpha, v)
        return v, maxAct
    else:
        # chance node
        v = 0
        allActions = game.get_actions(state)
        for action in allActions:
            new_val, _ = myexpectimax(iagent, alpha, beta, game, game.get_successor(
                state, action), heuristic,  max(-1, max_depth-1))
            v += new_val
        # return the mean value of all children
        return v/len(allActions), None


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    agent = game.get_turn(state)
    return myexpectimax(agent, -inf, inf,  game, state, heuristic, max_depth)
