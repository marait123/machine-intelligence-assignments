# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    # seeting the noise to 0.0 will make it go besite -10 row and making the discount factor small will make
    # it go for the nearest reward
    return {
        "noise": 0.0,
        "discount_factor": 0.01,
        "living_reward": -1
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    # we need to go to the +1 but avoiding being neer the -10 row
    #  so we make discount factor small (medium)
    # and we make noise big like .4 to make it avoid getting near the -10 row
    return {
        "noise": 0.4,   # .4
        "discount_factor": 0.5,    # .1
        "living_reward": -3         #-3
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    #  setting the discount factor to 1 and the noise to 0 will cause the agent to 
    # go to the biggest reward via the short safe path but this has to set the noise to 0.0
    return {
        "noise": 0.0,
        "discount_factor": 1,
        "living_reward": -1
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
    # we want to go through the long safe path
    # we need living reward to be small for it to prefer the long path
    # big discount factor 1 means go for the +10
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -.01
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    # giving postitive reward and setting noise to 0 will cause the game to last for ever
    # since
    return {
        "noise": 0.0,
        "discount_factor": 0.99,
        "living_reward":10
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    # making the living reward very big causes the agent to try to terminate as soon as possible
    return {
        "noise": 0.0,
        "discount_factor": 0.99,
        "living_reward": -100
    }