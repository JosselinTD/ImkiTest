from environment import Environment
import unittest

class TestEnvironmentClass(unittest.TestCase):
  blankMap = '0000000000000000000000000000000000000000'

  fullWallMap = '0000000000000000444444444444444444444444'

  endMap = '1000000002000003000040444004040440404440'

  spMap = '1000000000000000000000000000000000000000'

  connectingMap = '1000002000000000004444444444444444444444'

  def setUp(self):
    self.environment = Environment(4)

  def test_initialisation(self):
    self.assertEqual(self.environment.mapSize, 4, 'incorrect map size')
    self.assertEqual(len(self.environment.allActions), 16 * 3 + 24, 'incorrect all actions size')

  def test_isAVerticalWall(self):
    self.assertEqual(self.environment.isAVerticalWall(0), True)
    self.assertEqual(self.environment.isAVerticalWall(1), True)
    self.assertEqual(self.environment.isAVerticalWall(2), True)

    self.assertEqual(self.environment.isAVerticalWall(3), False)
    self.assertEqual(self.environment.isAVerticalWall(4), False)
    self.assertEqual(self.environment.isAVerticalWall(5), False)
    self.assertEqual(self.environment.isAVerticalWall(6), False)

    self.assertEqual(self.environment.isAVerticalWall(7), True)
    self.assertEqual(self.environment.isAVerticalWall(8), True)
    self.assertEqual(self.environment.isAVerticalWall(9), True)

    self.assertEqual(self.environment.isAVerticalWall(10), False)
    self.assertEqual(self.environment.isAVerticalWall(11), False)
    self.assertEqual(self.environment.isAVerticalWall(12), False)
    self.assertEqual(self.environment.isAVerticalWall(13), False)

    self.assertEqual(self.environment.isAVerticalWall(14), True)
    self.assertEqual(self.environment.isAVerticalWall(15), True)
    self.assertEqual(self.environment.isAVerticalWall(16), True)

    self.assertEqual(self.environment.isAVerticalWall(17), False)
    self.assertEqual(self.environment.isAVerticalWall(18), False)
    self.assertEqual(self.environment.isAVerticalWall(19), False)
    self.assertEqual(self.environment.isAVerticalWall(20), False)

    self.assertEqual(self.environment.isAVerticalWall(21), True)
    self.assertEqual(self.environment.isAVerticalWall(22), True)
    self.assertEqual(self.environment.isAVerticalWall(23), True)
  
  def test_illegalAction(self):
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'W200'), False)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'SP200'), False)

    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'SP1'), True)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'TP1'), True)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'EP1'), True)
    self.assertEqual(self.environment.isActionLegal(self.endMap, 'SP1'), False)
    self.assertEqual(self.environment.isActionLegal(self.endMap, 'TP1'), False)
    self.assertEqual(self.environment.isActionLegal(self.endMap, 'EP1'), False)

    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'W1'), False)
    self.assertEqual(self.environment.isActionLegal(self.fullWallMap, 'W1'), True)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'W12'), False)
    self.assertEqual(self.environment.isActionLegal(self.fullWallMap, 'W12'), True)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'W16'), False)
    self.assertEqual(self.environment.isActionLegal(self.fullWallMap, 'W16'), True)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'W21'), False)
    self.assertEqual(self.environment.isActionLegal(self.fullWallMap, 'W21'), True)
    self.assertEqual(self.environment.isActionLegal(self.blankMap, 'W24'), False)
    self.assertEqual(self.environment.isActionLegal(self.fullWallMap, 'W24'), True)

  def test_getSpaceWalls(self):
    self.assertEqual(self.environment.getSpaceWalls(6), [5+16,8+16,9+16,12+16])
    self.assertEqual(self.environment.getSpaceWalls(1), [1+16,4+16])
    self.assertEqual(self.environment.getSpaceWalls(12), [14+16,17+16,21+16])
    self.assertEqual(self.environment.getSpaceWalls(16), [21+16,24+16])

  def test_getWallSpaces(self):
    self.assertEqual(self.environment.getWallSpaces(1+16), [1,2])
    self.assertEqual(self.environment.getWallSpaces(2+16), [2,3])
    self.assertEqual(self.environment.getWallSpaces(3+16), [3,4])

    self.assertEqual(self.environment.getWallSpaces(4+16), [1,5])
    self.assertEqual(self.environment.getWallSpaces(5+16), [2,6])
    self.assertEqual(self.environment.getWallSpaces(6+16), [3,7])
    self.assertEqual(self.environment.getWallSpaces(7+16), [4,8])

    self.assertEqual(self.environment.getWallSpaces(8+16), [5,6])
    self.assertEqual(self.environment.getWallSpaces(9+16), [6,7])
    self.assertEqual(self.environment.getWallSpaces(10+16), [7,8])

    self.assertEqual(self.environment.getWallSpaces(11+16), [5,9])
    self.assertEqual(self.environment.getWallSpaces(12+16), [6,10])
    self.assertEqual(self.environment.getWallSpaces(13+16), [7,11])
    self.assertEqual(self.environment.getWallSpaces(14+16), [8,12])

    self.assertEqual(self.environment.getWallSpaces(15+16), [9,10])
    self.assertEqual(self.environment.getWallSpaces(16+16), [10,11])
    self.assertEqual(self.environment.getWallSpaces(17+16), [11,12])

    self.assertEqual(self.environment.getWallSpaces(18+16), [9,13])
    self.assertEqual(self.environment.getWallSpaces(19+16), [10,14])
    self.assertEqual(self.environment.getWallSpaces(20+16), [11,15])
    self.assertEqual(self.environment.getWallSpaces(21+16), [12,16])

    self.assertEqual(self.environment.getWallSpaces(22+16), [13,14])
    self.assertEqual(self.environment.getWallSpaces(23+16), [14,15])
    self.assertEqual(self.environment.getWallSpaces(24+16), [15,16])

  def test_listAllAdjacentSpaces(self):
    self.assertEqual(self.environment.listAllAdjacentSpaces(self.fullWallMap, 3), [3])
    self.assertEqual(len(self.environment.listAllAdjacentSpaces(self.blankMap, 1)), 16)
    self.assertEqual(self.environment.listAllAdjacentSpaces(self.endMap, 1), [1, 5, 9, 13, 10, 2, 3, 7, 11, 15, 16, 8, 4])
    self.assertEqual(self.environment.listAllAdjacentSpaces(self.connectingMap, 1), [1, 2, 3])

  def test_reward(self):
    self.assertEqual(self.environment.reward(self.fullWallMap, 'W1'), 0)
    self.assertEqual(self.environment.reward(self.fullWallMap, 'SP1'), 1)
    self.assertEqual(self.environment.reward(self.endMap, 'W8'), 0)
    self.assertEqual(self.environment.reward(self.spMap, 'TP2'), 2)
    self.assertEqual(self.environment.reward(self.spMap, 'TP6'), 3)
    self.assertEqual(self.environment.reward(self.spMap, 'TP16'), 7)
    self.assertEqual(self.environment.reward(self.connectingMap, 'W6'), 5)

  def test_curatedActions(self):
    self.assertEqual('W' not in ', '.join(self.environment.curatedActions(self.blankMap)), True)
    self.assertEqual('SP' not in ', '.join(self.environment.curatedActions(self.endMap)), True)
    self.assertEqual('TP' not in ', '.join(self.environment.curatedActions(self.endMap)), True)
    self.assertEqual('EP' not in ', '.join(self.environment.curatedActions(self.endMap)), True)

  def test_updateState(self):
    self.assertEqual(self.environment.updateState(self.blankMap, 'SP1'), '1000000000000000000000000000000000000000')
    self.assertEqual(self.environment.updateState(self.blankMap, 'SP2'), '0100000000000000000000000000000000000000')
    self.assertEqual(self.environment.updateState(self.blankMap, 'TP3'), '0020000000000000000000000000000000000000')
    self.assertEqual(self.environment.updateState(self.blankMap, 'EP4'), '0003000000000000000000000000000000000000')
    self.assertEqual(self.environment.updateState(self.fullWallMap, 'W4'), '0000000000000000444044444444444444444444')

  def test_getStartingState(self):
    self.assertEqual(self.environment.getStartingState(), self.fullWallMap)
  
  def test_isRoomsConnected(self):
    self.assertEqual(self.environment.isRoomsConnected(self.blankMap), False)
    self.assertEqual(self.environment.isRoomsConnected(self.fullWallMap), False)
    self.assertEqual(self.environment.isRoomsConnected(self.endMap), True)
    self.assertEqual(self.environment.isRoomsConnected(self.spMap), False)
    self.assertEqual(self.environment.isRoomsConnected(self.connectingMap), False)


if __name__ == '__main__':
  unittest.main()