from HandStat import *
#from framework import *
import pickle
from UnbiasedNet import *
import call_defeater
import tight_aggressive
import framework
import numpy as np
import calling_station

csbot=calling_station.Calling_station()
lion150= pickle.load(open("lion150.p","rb"))
lion150_2=pickle.load(open("lion150_2.p", "rb"))
lion150_3=pickle.load(open("lion150_3.p", "rb"))
chor1=pickle.load(open("0.005_0.9_40000.p" ,"rb"))
chor2=pickle.load(open("0.005_0.9_60000.p" ,"rb"))
chor3=pickle.load(open("0.005_0.9_80000.p" ,"rb"))
chor4=pickle.load(open("0.005_0.9_100000.p" ,"rb"))
chor5=pickle.load(open("0.005_0.9_120000.p" ,"rb"))
chor6=pickle.load(open("0.005_0.9_140000.p" ,"rb"))
chor7=pickle.load(open("0.005_0.9_160000.p" ,"rb"))
chor8=pickle.load(open("0.005_0.9_180000.p" ,"rb"))
chor9=pickle.load(open("0.005_0.9_200000.p" ,"rb"))
bots= [chor1, chor2, chor3, chor4, chor5, chor6, chor7, chor8, chor9]
for bot in bots:
    wins=[]
    for i in range(10):
        wins.append(bot.compete(csbot, 1000, debug=0))
    print "alpha= 0.001 and decreases over time"
    print "name= ", bot.name
    print wins
    print 'mean', np.mean(wins)
    print 'std', np.std(wins)
