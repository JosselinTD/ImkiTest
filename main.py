from environment import Environment
from qagent import QAgent

environment = Environment(4)
qagent = QAgent(environment, 0.1, 0.8, 0.1, 10)

qagent.train(500)
# print(qagent.qMap)
print(qagent.generate())