from typing import Dict
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented
inf=1e30
# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[str, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {str(state):0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()
        if(self.mdp.is_terminal(state)):
            return 0
        actions = self.mdp.get_actions(state)
        max_u=-inf
        for action in actions:
            new_states_dic = self.mdp.get_successor(state, action)
            new_u=0
            for new_state in new_states_dic:
                #new_u+=P(s'| s, a) * (r(s,a,s') + discount_factor * U(s'))

                reward = self.mdp.get_reward(state, action, new_state) 

                utility_discounted = self.discount_factor * self.utilities[str(new_state)]
                new_u += (new_states_dic[new_state] *  (reward+ utility_discounted))

            if new_u > max_u:
                max_u= new_u
        return max_u
    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: int = 1):
        #TODO: Complete this function to apply value iteration for the given number of iterations
        for _ in range(iterations):
            new_utilities = self.utilities.copy()
            for state in self.mdp.get_states():
                new_utilities[str(state)] = self.compute_bellman(state)
            self.utilities=new_utilities
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # if more than one action has the maximum expected utility, return the one that appears first in the "actions" list
        
        # return the action that maximizes the expected utility Q(s,a)
        if self.mdp.is_terminal(state):
            return None
        
        actions = env.actions()
        best_action = None
        max_u=-inf
        for action in actions:
            new_states_dic = self.mdp.get_successor(state, action)
            new_u=0
            for new_state in new_states_dic:
                #new_u+=P(s'| s, a) * (r(s,a,s') * discount_factor * U(s'))

                reward = self.mdp.get_reward(state, action, new_state) 
                utility_discounted = self.discount_factor * self.utilities[str(new_state)]
                new_u += (new_states_dic[new_state] *  (reward+ utility_discounted))

            if new_u > max_u:
                max_u= new_u
                best_action= action
        return best_action            

    # Save the utilities to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.utilities = json.load(f)
