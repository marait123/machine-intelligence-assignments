from os import stat
from typing import Callable, DefaultDict, Dict, Generic, List, Optional, Union
from agents import Agent
from environment import Environment, S, A
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented

import json
from collections import defaultdict
inf=1e30
# The base class for all Reinforcement Learning Agents required for this problem set
class RLAgent(Agent[S, A]):
    rng: RandomGenerator # A random number generator used for exploration
    actions: List[A] # A list of all actions that the environment accepts
    discount_factor: float # The discount factor "gamma"
    epsilon: float # The exploration probability for epsilon-greedy
    learning_rate: float # The learning rate "alpha"

    def __init__(self,
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01, 
            seed: Optional[int] = None) -> None:
        super().__init__()
        self.rng = RandomGenerator(seed) # initialize the random generator with a seed for reproducability
        self.actions = actions
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    # A virtual function that returns the Q-value for a specific state and action
    # This should be overriden by the derived RL agents
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return 0
    
    # Returns true if we should explore (rather than exploit)
    def should_explore(self) -> bool:
        return self.rng.float() < self.epsilon

    def act(self, env: Environment[S, A], observation: S, training: bool = False) -> A:
        actions = env.actions()
        if training and self.should_explore():
            #TODO: Return a random action whose index is "self.rng.int(0, len(actions)-1)"
            return actions[self.rng.int(0, len(actions)-1)]
        else:
            #TODO: return the action with the maximum q-value as calculated by "compute_q" above
            # if more than one action has the maximum q-value, return the one that appears first in the "actions" list
            max_q= -inf
            max_action = None
            for action in actions:
                new_q = self.compute_q(env,observation, action)
                if new_q > max_q:
                    max_q = new_q
                    max_action=action
            return max_action

#############################
#######     SARSA      ######
#############################

# This is a class for a generic SARSA agent
class SARSALearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]] # The table of the Q values
                                                 # The first key is the string representation of the state
                                                 # The second key is the string representation of the action
                                                 # The value is the Q-value of the given state and action
    
    def __init__(self, 
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01, 
            seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda:defaultdict(lambda:0)) # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return self.Q[str(state)][str(action)] # Return the Q-value of the given state and action
        # NOTE: we cast the state and the action to a string before querying the dictionaries
    
    # Update the value of Q(state, action) using this transition via the SARSA update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, next_action: Optional[A]):
        #TODO: Complete this function to update Q-table using the SARSA update rule
        # If next_action is None, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        if next_state is None:
            return
        # just applying the sarse update rule here
        q_s_a = self.Q[str(state)][str(action)]
        q_s_abar = self.Q[str(next_state)][str(next_action)] 
        self.Q[str(state)][str(action)] = q_s_a  + self.learning_rate * (reward + self.discount_factor * q_s_abar- q_s_a) 

    # Save the Q-table to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.Q, f, indent=2, sort_keys=True)
    
    # load the Q-table from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.Q = json.load(f)

#############################
#####   Q-Learning     ######
#############################

# This is a class for a generic Q-learning agent
class QLearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]] # The table of the Q values
                                                 # The first key is the string representation of the state
                                                 # The second key is the string representation of the action
                                                 # The value is the Q-value of the given state and action
    
    def __init__(self, 
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01, 
            seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda:defaultdict(lambda:0)) # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return self.Q[str(state)][str(action)] # Return the Q-value of the given state and action
        # NOTE: we cast the state and the action to a string before querying the dictionaries
    
    # Given a state, compute and return the utility of the state using the function "compute_q"
    def compute_utility(self, env: Environment[S, A], state: S) -> float:
        #TODO: Complete this function..
        # utility value = argmax(a) Q(s,a)
        actions = env.actions()
        max_q = -inf
        for action in actions:
            max_q = max(max_q, self.compute_q(env, state,action))
        return max_q

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        #TODO: Complete this function to update Q-table using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        
        # update the entry Q[state][action] in the Q table based on the equetion of Q-Learning
        # current_state_utility
        q_s_a = self.Q[str(state)][str(action)]
        # next state utility
        q_s_abar = self.compute_utility(env, next_state)
        self.Q[str(state)][str(action)] = q_s_a + self.learning_rate *(reward + self.discount_factor * q_s_abar - q_s_a)
    
    # Save the Q-table to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.Q, f, indent=2, sort_keys=True)
    
    # load the Q-table from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.Q = json.load(f)

#########################################
#####   Approximate Q-Learning     ######
#########################################

# The type definition for a set of features representing a state
# The key is the feature name and the value is the feature value
Features = Dict[str, float]

# This class takes a state and returns the a set of features
class FeatureExtractor(Generic[S, A]):

    # Returns a list of feature names.
    # This will be used by the Approximate Q-Learning agent to initialize its weights dictionary.
    @property
    def feature_names(self) -> List[str]:
        return []
    
    # Given an enviroment and an observation (a state), return a set of features that represent the given state
    def extract_features(self, env: Environment[S, A], state: S) -> Features:
        return {}

# This is a class for a generic Q-learning agent
class ApproximateQLearningAgent(RLAgent[S, A]):
    weights: Dict[str, Features]    # The weights dictionary for this agent.
                                    # The first key is action and the second key is the feature name
                                    # The value is the weight 
    feature_extractor: FeatureExtractor[S, A]   # The feature extractor used to extract the features corresponding to a state

    def __init__(self, 
            feature_extractor: FeatureExtractor[S, A],
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01,
            seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        feature_names = feature_extractor.feature_names
        self.weights = {str(action):{feature: 0 for feature in feature_names} for action in actions} # we initialize the weights to 0
        self.feature_extractor = feature_extractor

    # Given the features of state and an action, compute and return the Q value
    def __compute_q_from_features(self, features: Dict[str, float], action: A) -> float:
        #TODO: Complete this function
        # NOTE: Remember to cast the action to string before quering self.weights
        # q value is the dot product between weights and input features
        q_val=0
        weightsDic = self.weights[str(action)]
        for feature in weightsDic:
            q_val += (weightsDic[feature] * features[feature])        
        return q_val
    
    # Given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
    def __compute_utility_from_features(self, features: Dict[str, float]) -> float:
        #TODO: Complete this function
        # utility is the max q over all actions
        utility= -inf
        for action in self.actions:
            utility = max(utility, self.__compute_q_from_features(features, action))
        return utility
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        features = self.feature_extractor.extract_features(env, state)
        return self.__compute_q_from_features(features, action)

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        #TODO: Complete this function to update weights using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        # extract the features for the current state
        features = self.feature_extractor.extract_features(env,state)
        q_s_a = self.compute_q(env, state, action)
        features_bar = self.feature_extractor.extract_features(env, next_state)
        
        q_s_abar = 0 if done else self.__compute_utility_from_features(features_bar)
        
        # update the weights for each feature in the weights dictionary for the current action
        # based on the weights update equation
        for weight_feature in self.weights[str(action)]:
            w_i_a = self.weights[str(action)][weight_feature]
            wi = features[weight_feature]
            self.weights[str(action)][weight_feature] =  w_i_a + self.learning_rate * (reward + self.discount_factor * q_s_abar - q_s_a)*wi
        
    
    # Save the weights to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.weights, f, indent=2, sort_keys=True)
    
    # load the weights from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.weights = json.load(f)