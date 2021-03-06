from environment import Environment
from qagent import QAgent

environment = Environment(4)
qagent = QAgent(environment, 0.1, 0.8, 0.1)

qagent.load()
qagent.train(1000)
environment.drawMap(qagent.generate())
qagent.save()