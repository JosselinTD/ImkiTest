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
    self.assertEqual(self.qagent.getQState(self.blankMap), {'SP1': 0, 'TP1': 0, 'EP1': 0, 'SP2': 0, 'TP2': 0, 'EP2': 0, 'SP3': 0, 'TP3': 0, 'EP3': 0, 'SP4': 0, 'TP4': 0, 'EP4': 0, 'SP5': 0, 'TP5': 0, 'EP5': 0, 'SP6': 0, 'TP6': 0, 'EP6': 0, 'SP7': 0, 'TP7': 0, 'EP7': 0, 'SP8': 0, 'TP8': 0, 'EP8': 0, 'SP9': 0, 'TP9': 0, 'EP9': 0, 'SP10': 0, 'TP10': 0, 'EP10': 0, 'SP11': 0, 'TP11': 0, 'EP11': 0, 'SP12': 0, 'TP12': 0, 'EP12': 0, 'SP13': 0, 'TP13': 0, 'EP13': 0, 'SP14': 0, 'TP14': 0, 'EP14': 0, 'SP15': 0, 'TP15': 0, 'EP15': 0, 'SP16': 0, 'TP16': 0, 'EP16': 0})
    self.assertEqual(self.qagent.getQState(self.fullWallMap), {'SP1': 0, 'TP1': 0, 'EP1': 0, 'SP2': 0, 'TP2': 0, 'EP2': 0, 'SP3': 0, 'TP3': 0, 'EP3': 0, 'SP4': 0, 'TP4': 0, 'EP4': 0, 'SP5': 0, 'TP5': 0, 'EP5': 0, 'SP6': 0, 'TP6': 0, 'EP6': 0, 'SP7': 0, 'TP7': 0, 'EP7': 0, 'SP8': 0, 'TP8': 0, 'EP8': 0, 'SP9': 0, 'TP9': 0, 'EP9': 0, 'SP10': 0, 'TP10': 0, 'EP10': 0, 'SP11': 0, 'TP11': 0, 'EP11': 0, 'SP12': 0, 'TP12': 0, 'EP12': 0, 'SP13': 0, 'TP13': 0, 'EP13': 0, 'SP14': 0, 'TP14': 0, 'EP14': 0, 'SP15': 0, 'TP15': 0, 'EP15': 0, 'SP16': 0, 'TP16': 0, 'EP16': 0, 'W1': 0, 'W2': 0, 'W3': 0, 'W4': 0, 'W5': 0, 'W6': 0, 'W7': 0, 'W8': 0, 'W9': 0, 'W10': 0, 'W11': 0, 'W12': 0, 'W13': 0, 'W14': 0, 'W15': 0, 'W16': 0, 'W17': 0, 'W18': 0, 'W19': 0, 'W20': 0, 'W21': 0, 'W22': 0, 'W23': 0, 'W24': 0})
    self.assertEqual(self.qagent.getQState(self.endMap), {'W5': 0, 'W8': 0, 'W9': 0, 'W12': 0, 'W14': 0, 'W16': 0, 'W17': 0, 'W19': 0, 'W21': 0, 'W22': 0, 'W23': 0})
    self.assertEqual(self.qagent.getQState(self.spMap), {'TP2': 0, 'EP2': 0, 'TP3': 0, 'EP3': 0, 'TP4': 0, 'EP4': 0, 'TP5': 0, 'EP5': 0, 'TP6': 0, 'EP6': 0, 'TP7': 0, 'EP7': 0, 'TP8': 0, 'EP8': 0, 'TP9': 0, 'EP9': 0, 'TP10': 0, 'EP10': 0, 'TP11': 0, 'EP11': 0, 'TP12': 0, 'EP12': 0, 'TP13': 0, 'EP13': 0, 'TP14': 0, 'EP14': 0, 'TP15': 0, 'EP15': 0, 'TP16': 0, 'EP16': 0})
    self.assertEqual(self.qagent.getQState(self.connectingMap), {'EP2': 0, 'EP3': 0, 'EP4': 0, 'EP5': 0, 'EP6': 0, 'EP8': 0, 'EP9': 0, 'EP10': 0, 'EP11': 0, 'EP12': 0, 'EP13': 0, 'EP14': 0, 'EP15': 0, 'EP16': 0, 'W3': 0, 'W4': 0, 'W5': 0, 'W6': 0, 'W7': 0, 'W8': 0, 'W9': 0, 'W10': 0, 'W11': 0, 'W12': 0, 'W13': 0, 'W14': 0, 'W15': 0, 'W16': 0, 'W17': 0, 'W18': 0, 'W19': 0, 'W20': 0, 'W21': 0, 'W22': 0, 'W23': 0, 'W24': 0})

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