import random

class QAgent:
  def __init__(self, environment, alpha, gamma, epsilon, iterationLife):
    self.environment = environment # Environment instance
    self.alpha = alpha # learning rate
    self.gamma = gamma # Importance of future actions
    self.epsilon = epsilon # ration of random actions over existing ones
    self.iterationLife = iterationLife # for training, how many actions allowed max
    self.qMap = {}

  def train(self, iterations):
    for i in range(iterations):
      state = self.environment.getStartingState()
      for j in range(self.iterationLife):
        nextAction = self.selectAction(state)
        state = self.updateQValue(state, action)

  def generate(self):
    state = self.environment.getStartingState()
    for j in range(self.iterationLife):
      nextAction = self.getBestAction(state)
      state = self.environment.updateState(state, action)
    return state

  def selectAction(self, state):
    curatedActions = self.environment.curatedActions(state)
    randomAction = self.epsilon > random.uniform(0,1)
    if randomAction: return random.choice(curatedActions)
    return self.getBestAction(state)

  def getQValue(self, state, action):
    return self.getQState(state).get(action)

  def getQState(self, state):
    qDict = self.qMap.get(state)
    if not qDict:
      qDict = {}
      for action in self.environment.curatedActions(state):
        qDict[action] = 0
      self.qMap[state] = qDict
    return qDict

  def updateQValue(self, state, action):
    currentQValue = self.getQValue(state, action)
    reward = self.environment.reward(state, action)

    nextState = self.environment.updateState(state, action)
    bestNextAction = self.getBestAction(nextState)

    # Basic qValue formula
    newQvalue = currentQValue + self.alpha * (reward + self.gamma * (self.getQValue(nextState, bestNextAction) - currentQValue))
    # Alternative qValue formula
    # newQvalue = (1 - self.alpha) * currentQValue + self.alpha * (reward + self.gamma * (self.getQSValue(nextState, bestNextAction) - currentQValue))

    self.qMap[state][action] = newQvalue
    return nextState

  def getBestAction(self, state):
    actions = self.getQState(state)
    return max(actions, key=actions.get)