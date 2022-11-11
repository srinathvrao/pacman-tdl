from learningAgents import ReinforcementAgent
import util


class TrueOnlineSarsaLambdaAgent(ReinforcementAgent):
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        """
        Define feature vectors, q values, etc here
        """

    def getQValue(self, state, action):
        """
        Using weights, calculate q value according to linear function approximation
        """
        return util.raiseNotDefined()

    def getValue(self, state):
        """
        Using self.getQValue(), calculate the value of a current state
        May not be used ¯\_(ツ)_/¯
        """
        return util.raiseNotDefined()

    def getAction(self, state):
        """
        Using self.getQValue() calculate the action to take at a given state
        """
        return util.raiseNotDefined()

    def getPolicy(self, state):
        """
        Using self.getAction(), calculate the epsilon greedy policy for the state
        """
        return util.raiseNotDefined()

    def getFeatureVector(self, state, action):
        """
        Return the feature vector given a state, action pair
        """
        return util.raiseNotDefined()

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
        return util.raiseNotDefined()
