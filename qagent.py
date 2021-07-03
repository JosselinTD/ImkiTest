import random, sys, json

class QAgent:
  def __init__(self, environment, alpha, gamma, epsilon):
    self.environment = environment # Environment instance
    self.alpha = alpha # learning rate
    self.gamma = gamma # Importance of future actions
    self.epsilon = epsilon # ration of random actions over existing ones
    self.qMap = {}

  def train(self, iterations):
    # Print loading bar, from https://stackoverflow.com/a/3002100/2332573
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('='*0, 0))
    sys.stdout.flush()

    for i in range(iterations):
      state = self.environment.getStartingState()
      while not self.environment.isRoomsConnected(state):
        nextAction = self.selectAction(state)
        state = self.updateQValue(state, nextAction)
      self.cleanQMap()
      # Update loading bar
      sys.stdout.write('\r')
      percent = int(i * 100 / iterations)
      sys.stdout.write("[%-100s] %d%%" % ('=' * percent, percent))
      sys.stdout.flush()
    print()

  def generate(self):
    state = self.environment.getStartingState()
    while not self.environment.isRoomsConnected(state):
      nextAction = self.selectAction(state)
      state = self.environment.updateState(state, nextAction)
    return state

  def save(self):
    with open(f"{self.environment.mapSize}-{self.alpha}-{self.gamma}-{self.epsilon}.json", "w") as write_file:
      json.dump(self.qMap, write_file, indent=2)

  def load(self):
    try:
      with open(f"{self.environment.mapSize}-{self.alpha}-{self.gamma}-{self.epsilon}.json") as json_file:
        self.qMap = json.load(json_file)
    except:
      print('Model not loadable, qMap set to default')

  def selectAction(self, state):
    curatedActions = self.environment.curatedActions(state)
    randomAction = self.epsilon > random.uniform(0,1)

    if randomAction: return random.choice(curatedActions)
    return self.getBestAction(state)

  def getQValue(self, state, action):
    return self.getQState(state).get(action) or 0

  def getQState(self, state):
    qDict = self.qMap.get(state)
    if not qDict:
      qDict = {}
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

    if newQvalue > 0: self.qMap[state][action] = newQvalue
    elif self.qMap[state].get(action): del self.qMap[state][action]
    
    # if newQvalue > 0: print(state, action, newQvalue)
    return nextState

  def getBestAction(self, state):
    actionsDict = self.getQState(state)

    values = list(actionsDict.values())
    actions = list(actionsDict.keys())
    if len(actions) == 0: return random.choice(self.environment.curatedActions(state))
    
    maxValue = max(values)

    actionsIndexesWithMaxValues = [i for i in range(len(values)) if values[i] == maxValue]

    return actions[random.choice(actionsIndexesWithMaxValues)]

  def cleanQMap(self):
    self.qMap = {k:v for k,v in self.qMap.items() if bool(v)}