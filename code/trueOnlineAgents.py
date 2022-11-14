import math
import random
from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
import util
# import numpy as np


class TrueOnlineSarsaLambdaAgent(ReinforcementAgent):
    def __init__(self, trace_decay=0.8, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, extractor='IdentityExtractor',  **args):
        self.index = 0  # This is always Pacman
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        ReinforcementAgent.__init__(self, **args)
        """
        Define feature vectors, q values, etc here
        """
        self.getFeaturesRaw = util.lookup(extractor, globals())().getFeatures
        self.weights = util.Counter()
        self.oldQ = 0
        self.trace = util.Counter()
        self.trace_decay = trace_decay
        self.next_action = None

    def featureDotProduct(self, counter, state, action):
        return sum([counter[feature] * featureVal for (feature,
                                                       featureVal) in self.getFeatureCounter(state, action).items()])

    def getQValue(self, state, action):
        """
        Using weights, calculate q value according to linear function approximation
        """
        qValue = self.featureDotProduct(self.weights, state, action)

        return qValue

    def getValue(self, state):
        """
        Using self.getQValue(), calculate the value of a current state
        May not be used ¯\_(ツ)_/¯
        """
        legalActions = self.getLegalActions(state)

        if len(legalActions) == 0:
            return 0

        value = -math.inf
        for action in legalActions:
            value = max(value, self.getQValue(state, action))

        return value

    def getAction(self, state):
        """
        Using self.getQValue() calculate the action to take at a given state (epsilon greedy)
        """
        if self.next_action is not None:
            res = self.next_action
            self.next_action = None
            return res

        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None
        shouldDoRandom = util.flipCoin(self.epsilon)

        action = random.choice(
            legalActions) if shouldDoRandom else self.getPolicy(state)
        self.doAction(state, action)
        return action

    def getPolicy(self, state):
        """
        Using self.getAction(), calculate the optimal policy for the state
        """
        legalActions = self.getLegalActions(state)

        if len(legalActions) == 0:
            return None

        actionValuePair = (-math.inf, -1, None)
        for (i, action) in enumerate(legalActions):
            actionValuePair = max(
                actionValuePair, (self.getQValue(state, action), i, action))

        return actionValuePair[2]

    def getFeatureCounter(self, state, action):
        """
        Return the feature vector given a state, action pair
        """
        return self.getFeaturesRaw(state, action)

    def startEpisode(self):
        self.trace = util.Counter()
        self.oldQ = 0
        return super().startEpisode()

    def update(self, state, action, nextState, reward):
        """
        (THIS MAY NOT BE COMPLETELY ACCURATE)
        (GREEK LETTERS, DO NOT COPY PASTE INTO REAL CODE)
        (Numpy would help here tremendously)

        Given S, A, R, S'
            A'     = self.getPolicy(nextState)
            x      = IF NULL self.getFeatureVector(state, action) ELSE dont change
            x'     = self.getFeatureVector(nextState, A')
            Q      = self.getQValue(state, action)
            Q'     = self.getQValue(nextState, A')
            δ      = R + γQ' - Q
            z      = γλz + (1-αγλzᵀx)x                       <-- Not sure if we can abstract this away or what this represents and should be 0 at start of episode
            w      = w + α(δ + Q - Qₚᵣᵢₒᵣ)z - α(Q - Qₚᵣᵢₒᵣ)x
            Qₚᵣᵢₒᵣ = Q'                                      <-- Should be initialized to 0 at begining of episode
            x      = x'

        Keep in mind these are my best guesses. Need to discuss for this to make more sense
        """
        self.updateTrace(state, action)
        self.updateWeights(state, action, nextState, reward)

    def updateTrace(self, state, action):
        discount_coefficient = self.discount * self.trace_decay
        feature_coefficient = 1-self.alpha*discount_coefficient * \
            self.featureDotProduct(self.trace, state, action)
        new_trace = util.Counter()
        for feature, value in self.trace.items():
            new_trace[feature] = value * discount_coefficient
        for feature, value in self.getFeatureCounter(state, action).items():
            new_trace[feature] += feature_coefficient * value

        self.trace = new_trace

    def updateWeights(self, state, action, nextState, reward):
        self.next_action = self.getAction(nextState)

        if self.next_action is None:
            return

        current_features = self.getFeatureCounter(state, action)

        current_q = self.getQValue(state, action)
        next_q = self.getQValue(nextState, self.next_action)

        difference = reward + self.discount * next_q - current_q

        # update weights
        next_weights = self.weights.copy()

        for feature, value in self.trace.items():
            next_weights[feature] += self.alpha * \
                (difference + current_q - self.oldQ)*value

        for feature, value in current_features.items():
            next_weights[feature] -= self.alpha*(current_q-self.oldQ)*value

        self.weights = next_weights.copy()
        self.oldQ = next_q