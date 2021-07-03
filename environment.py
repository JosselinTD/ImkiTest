import math
import re

class Environment:
  def __init__(self, mapSize):
    self.mapSize = mapSize
    self.allActions = []
    for i in range(self.mapSize * self.mapSize):
      self.allActions.append('SP' + str(i+1))
      self.allActions.append('TP' + str(i+1))
      self.allActions.append('EP' + str(i+1))

    for i in range((self.mapSize - 1) * self.mapSize * 2):
      self.allActions.append('W' + str(i+1))

  def reward(self, state, action):
    if not self.isActionLegal(state, action):
      raise AttributeError(f"Action {action} not allowed in state {state}")
    
    index = self.extractIndex(action, 'W' in action)
    reward = 0
    if 'W' not in action:
      if 'SP' in action or 'TP' in action or 'EP' in action: reward += 1 # 1 point when adding a room
      if '1' in state:
        spColumn = state.index('1') % self.mapSize
        spRow = int(math.ceil(float(state.index('1')) / self.mapSize))
        actionColumn = index % self.mapSize
        actionRow = int(float(index) / self.mapSize)
        reward += abs(spColumn - actionColumn) + abs(spRow - actionRow) * 3 # +3 point for each case between starting room and other room
    else:
      if '1' in state and ('2' in state or '3' in state):
        previouslyAdjacentSpaces = self.listAllAdjacentSpaces(state, state.index('1') + 1)
        newState = self.updateState(state, action)
        newlyAdjacentSpaces = self.listAllAdjacentSpaces(newState, newState.index('1') + 1)
        if ('2' in state and state.index('2') + 1 not in previouslyAdjacentSpaces and state.index('2') + 1 in newlyAdjacentSpaces) or ('3' in state and state.index('3') + 1 not in previouslyAdjacentSpaces and state.index('3') + 1 in newlyAdjacentSpaces): reward += 5 # +5 point when connecting starting room to another room
    return reward

  def curatedActions(self, state):
    return [action for action in self.allActions if self.isActionLegal(state, action)]

  def updateState(self, state, action):
    if not self.isActionLegal(state, action):
      raise AttributeError(f"Action {action} not allowed in state {state}")

    index = self.extractIndex(action, 'W' in action)
    newValue = '0'
    if 'SP' in action: newValue = '1'
    if 'TP' in action: newValue = '2'
    if 'EP' in action: newValue = '3'
    
    state = state[:index] + newValue + state[index + 1:]

    return state

  def getStartingState(self):
    spaces = '0' * (self.mapSize * self.mapSize)
    walls = '4' * ((self.mapSize - 1) * self.mapSize * 2)

    return spaces + walls

  def isActionLegal(self, state, action):
    index = self.extractIndex(action, 'W' in action)
    wallNumber = index - self.mapSize * self.mapSize

    # Index issues
    if 'W' not in action and index > self.mapSize * self.mapSize: return False
    if 'W' in action and wallNumber > (self.mapSize - 1) * self.mapSize * 2: return False
    # Already existing rooms
    if '1' in state and 'SP' in action: return False
    if '2' in state and 'TP' in action: return False
    if '3' in state and 'EP' in action: return False

    # Already filled room
    if 'W' not in action and state[index] != '0': return False

    # All non wall illegal action have been filtered when we are here
    if 'W' not in action: return True

    # Already breaked walls
    if state[index] == '0': return False

    return True

  def extractIndex(self, action, isWall):
    shift = -1
    if isWall : shift = self.mapSize * self.mapSize - 1
    return int(re.search(r'\d+', action).group()) + shift

  def listAllAdjacentSpaces(self, state, spaceIndex):
    spacesToAnalyze = [spaceIndex]
    adjacentSpaces = []
    while len(spacesToAnalyze) > 0:
      spaceToAnalyze = spacesToAnalyze.pop()
      adjacentSpaces.append(spaceToAnalyze)
      walls = self.getSpaceWalls(spaceToAnalyze)
      for wall in walls:
        if state[wall - 1] == '0': # getSpaceWalls return indexes starting on 1 and not 0
          spacesToAnalyze.extend(self.getWallSpaces(wall))
      spacesToAnalyze = [space for space in spacesToAnalyze if space not in adjacentSpaces and space > 0 and space <= self.mapSize * self.mapSize]
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
    if spaceIndex <= self.mapSize * self.mapSize - self.mapSize : walls.append(lowerWallIndex)

    return walls

  def getWallSpaces(self, wallIndex):
    wallNumber = wallIndex - self.mapSize * self.mapSize
    isAVerticalWall = self.isAVerticalWall(wallNumber - 1)
    if not isAVerticalWall:
      upperSpaceIndex = wallNumber - (math.ceil(wallNumber / (self.mapSize * 2 - 1)) * 3)
      lowerSpaceIndex = upperSpaceIndex + self.mapSize
      return [int(math.ceil(upperSpaceIndex)), int(math.ceil(lowerSpaceIndex))]
    else:
      rightSpaceIndex = wallNumber - (int(wallNumber / (self.mapSize * 2 - 1)) * 3)
      leftSpaceIndex = rightSpaceIndex + 1

      return [int(math.ceil(rightSpaceIndex)), int(math.ceil(leftSpaceIndex))]

  def isAVerticalWall(self, wallNumber):
    return (wallNumber % ((self.mapSize * 2) - 1)) < (self.mapSize - 1)

  def isRoomsConnected(self, state):
    if '1' in state and '2' in state and '3' in state:
      adjacentSpaces = self.listAllAdjacentSpaces(state, state.index('1') + 1)
      return state.index('2') + 1 in adjacentSpaces and state.index('3') + 1 in adjacentSpaces
    return False

  def drawMap(self, state): # quick function to draw map in console
    spaces = state[:(self.mapSize * self.mapSize)]
    walls = state[(self.mapSize * self.mapSize):]

    print('.'.join(('-' * (self.mapSize * 2 + 1)).split()))
    for row in range(self.mapSize):
      # Space row
      rowString = '|'
      rowSpaces = spaces[self.mapSize * row:self.mapSize * row + self.mapSize].replace('0', ' ')
      rowWalls = walls[self.mapSize * row * 2 - row:self.mapSize * row * 2 - row + self.mapSize - 1].replace('0', ' ').replace('4', '|')
      for i, space in enumerate(rowSpaces):
        rowString += space
        if i != len(rowSpaces) - 1:
          rowString += rowWalls[i]
      rowString += '|'
      print(rowString)

      # Wall row
      if row < self.mapSize - 1:
        rowString = '|'
        rowWalls = walls[self.mapSize * row * 2 - row + self.mapSize - 1:self.mapSize * row * 2 - row + self.mapSize - 1 + self.mapSize].replace('0', ' ').replace('4', '-')
        for i, wall in enumerate(rowWalls):
          rowString += wall
          if i != len(rowWalls) - 1:
            rowString += ' '
        rowString += '|'
        print(rowString)
    print('.'.join(('-' * (self.mapSize * 2 + 1)).split()))
    print(state)