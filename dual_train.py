import pickle
import UnbiasedNet
import anotherStatus as fw
import anotherStatus
import calling_station
import time
import numpy as np
from cheater_bot import Cheater_player
nameA = 'twinA.p'
nameB = 'twinB.p'
start=time.time()
ALPHA = 0.001
#LAMBS = [0.75, 0.8, 0.85, 0.9, 0.95, 1]
LAMB = 0.9
n_train = 10000
blockSize = 500
#cheaterBot = Cheater_player()
csBot = calling_station.Calling_station()
#net = UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
#					   alpha=ALPHA, lamb=LAMB, randomInit=True)
#auto = fw.AnotherAutoPlayer(net, name="twinA")
#net2 = BiasedPerceptron(fw.n_in, fw.n_hidden, fw.n_out,
#                            alpha=ALPHA, lamb=LAMB, randomInit=True)
#auto = fw.AnotherAutoPlayer(net, name="superbot")
#ai = fw.AnotherAutoPlayer(net2, name='cpu', frenzy=1)
# auto = pickle.load(open("0.75frenzy_vs_calling.p", 'rb'))
# auto2 = pickle.load(open("0.75frenzy_vs_cheater.p", 'rb'))

auto = pickle.load(open(nameA, 'rb'))
auto2 = pickle.load(open(nameB, 'rb'))
lastTime = start
for i in range(n_train/blockSize):
	if i%2==0:
		auto.train(blockSize, auto2, debug=0, frenzy=1)
		pickle.dump(auto, open(nameA, "wb"))
	else:
		auto2.train(blockSize, auto, debug=0, frenzy=1)
		pickle.dump(auto2, open(nameB, "wb"))
	print "partial training used time", time.time()-lastTime
	lastTime = time.time()
print "the training used time", time.time()-start


auto = pickle.load(open(nameA, 'rb'))
result = []
for i in range(5):
	result.append( 
		auto.compete(cheaterBot, 2000, debug=0))
print 'Lambda:', LAMB
print 'Results against cheater bot: ', result
print 'mean', np.mean(result)
print 'std', np.std(result)

print "========"

auto2 = pickle.load(open(nameB, 'rb'))
result = []
for i in range(5):
	result.append( 
		auto2.compete(cheaterBot, 2000, debug=0))
print 'Lambda:', LAMB
print 'Results against cheater bot: ', result
print 'mean', np.mean(result)
print 'std', np.std(result)