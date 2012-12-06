from UnbiasedNet import NeuralNet

n = NeuralNet(5, 5, 1, randomInit=False, subdiv=[(0,0),(3,3),(5,5)])
print n.w_in
n.learnTD([[1,1,1,1,1]], 10)
print n.w_in
