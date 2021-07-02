import math

def Environment:
  mapSize = 4
  
  def __init__(self):
    self.allActions = []
    for i in range(self.mapSize * self.mapSize):
      self.allActions.append('SP' + str(i))
      self.allActions.append('TP' + str(i))
      self.allActions.append('EP' + str(i))

    for i in range((self.mapSize - 1) * self.mapSize * 2):
      self.allActions.append('W' + str(i))

  def reward(self, state, action):
    if not self.isActionLegal(state, action):
      raise AttributeError(f"Action {action} not allowed in state {state}")
    
    index = extractIndex(action, 'W' in action)
    reward = 0
    if 'W' not in action:
      if 'SP' in action or 'TP' in action or 'EP' in action: reward += 1 # 1 point when adding a room
      if '1' in state:
        spColumn = state.index('1') % self.mapSize
        spRow = int(math.ceil(float(state.index('1')) / self.mapSize))
        actionColumn = index % self.mapSize
        actionRow = int(math.ceil(float(index) / self.mapSize))
        reward += abs(spColumn - actionColumn) + abs(spRow - actionRow) # +1 point for each case between starting room and other room
    else:
      if '1' in state and ('2' in state or '3' in state):
        previouslyAdjacentSpaces = self.listAllAdjacentSpaces(state, state.index('1'))
        newState = self.updateState(state, action)
        newlyAdjacentSpaces = self.listAllAdjacentSpaces(newState, newStatestate.index('1'))
        if ('2' in state and state.index('2') not in previouslyAdjacentSpaces and state.index('2') in newlyAdjacentSpaces) or
           ('3' in state and state.index('3') not in previouslyAdjacentSpaces and state.index('3') in newlyAdjacentSpaces): reward += 5 # +5 point when connecting starting room to another room
    return reward

  def curatedActions(self, state):
    return [action for action in self.allActions if self.isActionLegal(state, action)]

  def updateState(self, state, action):
    if not self.isActionLegal(state, action):
      raise AttributeError(f"Action {action} not allowed in state {state}")

    index = extractIndex(action, 'W' in action)
    newValue = '0'
    if 'SP' in action: newValue = '1'
    if 'TP' in action: newValue = '2'
    if 'EP' in action: newValue = '3'
    
    state = state[:index] + newValue + state[index + 1:]

    return state

  def isActionLegal(self, state, action):
    index = extractIndex(action, 'W' in action):

    # Index issues
    if index < 0: return False
    if 'W' not in action and index > self.mapSize * self.mapSize: return False
    if 'W' in action and index > (self.mapSize - 1) * self.mapSize * 2: return False

    # Already existing rooms
    if '1' in state and 'SP' in action: return False
    if '2' in state and 'TP' in action: return False
    if '3' in state and 'EP' in action: return False

    # Already filled room
    if 'W' not in action and state[index] != 0: return False

    # All non wall illegal action have been filtered when we are here
    if 'W' not in action: return True

    # Already breaked walls
    if state[index] == 0: return False

    # 2x2 empty room
    wallNumber = index - self.mapSize * self.mapSize
    isAVerticalWall = self.isAVerticalWall(wallNumber)

    if isAVerticalWall:
      upperWallsToCheck = [
        # Upper wall
        index - (self.mapSize * 2 - 1),
        # Diagonal upper left
        index - self.mapSize
        # Diagonal upper right
        index - self.mapSize - 1
      ]
      lowerWallsToCheck = [
        # Lower wall
        index + (self.mapSize * 2 - 1),
        # Diagonal lower right
        index + self.mapSize,
        # Diagonal lower left
        index + self.mapSize +1
      ]
      if wallNumber > self.mapSize: # Check upper walls only if map exist there
        allDestroyed = True
        for i in upperWallsToCheck:
          if state[i] == 1:
            allDestroyed = False
            break
        if allDestroyed: return False

      if wallNumber < ((self.mapSize - 1) * self.mapSize * 2) - (self.mapSize - 1): # Check lower walls only if map exist there
        allDestroyed = True
        for i in lowerWallsToCheck:
          if state[i] == 1:
            allDestroyed = False
            break
        if allDestroyed: return False
    else:
      leftWallsToCheck = [
        # Upper wall
        index - self.mapSize,
        # Left wall
        index - 1
        # Lower wall
        index + self.mapSize - 1
      ]
      rightWallsToCheck = [
        # Upper wall
        index - self.mapSize - 1,
        # Right wall
        index + 1
        # Lower wall
        index + self.mapSize
      ]
      if wallNumber % (self.mapSize * 2 - 1) != self.mapSize: # Check left walls only if map exist there
        allDestroyed = True
        for i in leftWallsToCheck:
          if state[i] == 1:
            allDestroyed = False
            break
        if allDestroyed: return False

      if wallNumber % (self.mapSize * 2 - 1) != 0: # Check right walls only if map exist there
        allDestroyed = True
        for i in rightWallsToCheck:
          if state[i] == 1:
            allDestroyed = False
            break
        if allDestroyed: return False

    return True

  def extractIndex(self, action, isWall):
    shift = -1
    if isWall : shift = self.mapSize * self.mapSize
    return re.search(r'\d+', action).group() + shift

  def listAllAdjacentSpaces(self, state, spaceIndex):
    spacesToAnalyze = [spaceIndex]
    adjacentSpaces = []
    while len(spacesToAnalyze) > 0:
      spaceToAnalyze = spacesToAnalyze.pop()
      adjacentSpaces.append(spaceToAnalyze)
      walls = self.getSpaceWalls(spaceToAnalyze)
      for wall in walls:
        if state[wall] == 0:
          spacesToAnalyze.extend(self.getWallSpaces(wall))
      spacesToAnalyze = [space for space in spacesToAnalyze if space not in adjacentSpaces]
    return adjacentSpaces

  def getSpaceWalls(self, spaceIndex):
    spaceRow = int(math.ceil(float(spaceIndex) / self.mapSize))
    upperWallNumber = spaceIndex + ((spaceRow - 1) * (self.mapSize - 1) - self.mapSize)
    upperWallIndex = upperWallNumber + self.mapSize * self.mapSize
    leftWallIndex = upperWallIndex + (self.mapSize - 1)
    rightWallIndex = leftWallIndex + 1
    lowerWallIndex = upperWallIndex + (self.mapSize * 2 - 1)

    walls = []
    if spaceIndex > self.mapSize : walls.append(upperWallIndex)
    if spaceIndex % self.mapSize != 1 : walls.append(leftWallIndex)
    if spaceIndex % self.mapSize != 0 : walls.append(rightWallIndex)
    if spaceIndex < self.mapSize * self.mapSize - self.mapSize : walls.append(lowerWallIndex)

    return walls

  def getWallSpaces(self, wallIndex):
    wallNumber = wallIndex - self.mapSize * self.mapSize
    isAVerticalWall = self.isAVerticalWall(wallNumber)

    if isAVerticalWall:
      upperSpaceIndex = wallNumber - ((wallNumber / (self.mapSize * 2 - 1)) + 1)
      lowerSpaceIndex = upperSpaceIndex + self.mapSize

      return [upperSpaceIndex, lowerSpaceIndex]
    else:
      rightSpaceIndex = wallNumber - ((wallNumber / (self.mapSize * 2 - 1)) * 3)
      leftSpaceIndex = rightSpaceIndex + 1

      return [rightSpaceIndex, leftSpaceIndex]


  def isAVerticalWall(self, wallNumber):
    return (wallNumber % ((self.mapSize * 2) - 1)) < (self.mapSize - 1)