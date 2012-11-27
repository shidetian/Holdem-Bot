import numpy as np
import holdem
import UnbiasedNet
import framework as fw
import calling_station
import betting_station
import pickle
import time
start = time.time()
superbot= pickle.load(open("player.p", "rb"))
ancientbot= pickle.load(open("ancientbot.p", "rb"))
csbot= pickle.load(open("csbot.p", "rb"))
bsbot= betting_station.Betting_station()
lion150= pickle.load(open("lion150.p", "rb"))
lion150_1_2=pickle.load(open("lion150_2.p", "rb"))
lion150_1_3=pickle.load(open("lion150_3.p", "rb"))
chor= pickle.load(open("5_vs_Aggressive_0.9.p", "rb"))
wins=[]
for i in range(20):
    wins.append(chor.compete(csbot, 2000, debug=0))
print wins
print np.mean(wins)
print np.std(wins)
print "used", time.time()-start
