import pickle
from framework import *
from holdem import *
from calling_station import Calling_station
from betting_station import Betting_station 
import time
import numpy as np
import sys
from cheater_bot import Cheater_player
from threading import Thread, Lock, Semaphore
import os
lock = Lock()
numAvail = Semaphore(3)
path="./bots/"
data_name = "All_vs_cheater.txt"
class Worker(Thread):
	def __init__(self, fname):
		Thread.__init__(self)
		self.fname = fname
	def run(self):
		global path, lock, numAvail, data_name
		success = False
		auto = None
		data = ""
		cheaterBot = Cheater_player()
		if fname[-1]=='p':
			try:
				print path+fname
				auto = pickle.load(open(path+fname, 'rb'))
				#print "Passed"
				success = True
			except ImportError as e:
				#pass
				print e
		if not success:
			numAvail.release()
			return
		result = []
		for i in range(5):
			result.append( 
				auto.compete(cheaterBot, 1000, debug=0))
		print 'File ',fname
		print 'mean ', np.mean(result)
		print 'std ', np.std(result)
		print str(result)
		print "============="
		data+= 'File:' + fname
		data+= 'mean:' + str(np.mean(result))
		data+= 'std:' + str(np.std(result))
		data+= str(result)
		data+= "============="
		with lock:
			with open(data_name, 'a') as f:
				f.write(data)
		numAvail.release()
		

classes = ['pairStatus', 'anotherStatus', 'realizedStatus', 'coarserStatus']
dirList=os.listdir(path)
for fname in dirList:
	numAvail.acquire()
	Worker(fname).start()
