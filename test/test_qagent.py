from qagent import QAgent
from environment import Environment
import unittest

class TestQAgentClass(unittest.TestCase):
  blankMap = '0000000000000000000000000000000000000000'

  fullWallMap = '0000000000000000444444444444444444444444'

  endMap = '1000000002000003000040444004040440404440'

  spMap = '1000000000000000000000000000000000000000'

  connectingMap = '1000002000000000004444444444444444444444'

  def setUp(self):
    self.environment = Environment(4)
    self.qagent = QAgent(self.environment, 0.1, 0.8, 0.1, 25)

  def test_initialisation(self):
    self.assertEqual(self.qagent.environment, self.environment)
    self.assertEqual(self.qagent.alpha, 0.1)
    self.assertEqual(self.qagent.gamma, 0.8)
    self.assertEqual(self.qagent.epsilon, 0.1)
    self.assertEqual(self.qagent.iterationLife, 25)

  def test_getQState(self):
    self.qagent.updateQValue(self.connectingMap, 'W6')
    self.assertEqual(self.qagent.getQState(self.blankMap), {})
    self.assertEqual(self.qagent.getQState(self.connectingMap), {'W6': 0.5})

  def test_getQValue(self):
    self.assertEqual(self.qagent.getQValue(self.blankMap, 'SP1'), 0)

  def test_getBestAction(self):
    self.qagent.updateQValue(self.connectingMap, 'W6')
    self.assertEqual(self.qagent.getBestAction(self.connectingMap), 'W6')

  def test_updateQValue(self):
    self.assertEqual(self.qagent.updateQValue(self.connectingMap, 'W6'), self.environment.updateState(self.connectingMap, 'W6'))
    self.assertEqual(self.qagent.getQValue(self.connectingMap, 'W6'), 0.5)
    self.assertEqual(self.qagent.updateQValue('1000002000000000044444444444444444444444', 'W2'), self.connectingMap)
    self.assertEqual(self.qagent.getQValue('1000002000000000044444444444444444444444', 'W2'), 0 + 0.1 * (0 + 0.8 * 0.5))
    self.assertEqual(self.qagent.updateQValue(self.connectingMap, 'W6'), self.environment.updateState(self.connectingMap, 'W6'))
    self.assertEqual(self.qagent.getQValue(self.connectingMap, 'W6'), 0.5 + 0.1 * (5 + 0.8 * -0.5))

  def test_selectAction(self):
    self.qagent.updateQValue(self.connectingMap, 'W6')
    self.qagent.epsilon = 0
    self.assertEqual(self.qagent.selectAction(self.connectingMap), 'W6')
    self.qagent.epsilon = 1
    self.assertEqual(self.qagent.selectAction(self.connectingMap) == self.qagent.selectAction(self.connectingMap), False) # Can occasionaly fail

if __name__ == '__main__':
  unittest.main()