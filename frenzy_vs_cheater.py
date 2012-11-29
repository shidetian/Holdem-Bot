import pickle
import UnbiasedNet
import anotherStatus as fw
import calling_station
import time
import numpy as np
from cheater_bot import Cheater_player
name = 'frenzy_vs_cheater.p'
start=time.time()
ALPHA = 0.005
LAMBS = [0.8, 0.85, 0.9, 0.95, 1]
n_train = 5000
blockSize = 500
cheaterBot = Cheater_player()
csBot = calling_station.Calling_station()
for LAMB in LAMBS:
	net = UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
						   alpha=ALPHA, lamb=LAMB, randomInit=True)
	auto = fw.AnotherAutoPlayer(net, name="superbot")
	#net2 = BiasedPerceptron(fw.n_in, fw.n_hidden, fw.n_out,
	#                            alpha=ALPHA, lamb=LAMB, randomInit=True)
	#auto = fw.AnotherAutoPlayer(net, name="superbot")
	#ai = fw.AnotherAutoPlayer(net2, name='cpu', frenzy=1)
	lastTime = start
	for i in range(n_train/blockSize):
		auto.train(blockSize, cheaterBot, debug=0, frenzy=1)
		pickle.dump(auto, open(str(LAMB) + name, "wb"))
		print "partial training used time", time.time()-lastTime
		lastTime = time.time()
print "the training used time", time.time()-start


j=0
for LAMB in LAMBS:  
	auto = pickle.load(open(str(LAMB)+name, 'rb'))
	result = []
	for i in range(5):
		result.append( 
			auto.compete(csBot, 2000, debug=0))
	print 'Lambda:', LAMB
	print 'Results against betting bot: ', result
	print 'mean', np.mean(result)
	print 'std', np.std(result)
