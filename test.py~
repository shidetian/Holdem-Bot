import numpy as np
import holdem
import UnbiasedNet
import framework as fw
import calling_station
import pickle
superbot= pickle.load(open("player.p", "rb"))
ancientbot= pickle.load(open("ancientbot.p", "rb"))
csbot= pickle.load(open("csbot.p", "rb"))
#print superbot.net.w_out
#print ancientbot.net.w_out

#print superbot.net.w_in[1]
#print ancientbot.net.w_in[1]

#print superbot.net.w_in[50]
#print ancientbot.net.w_in[50]
ancientbot.net.alpha=0.001
for i in range(500):
    ancientbot.train(1,csbot, debug=0)
    print ancientbot.net.w_out[0]
#print superbot.net.w_out
#print ancientbot.net.w_out
print ancientbot.net.w_out
print ancientbot.net.w_in[1]
