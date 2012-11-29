import numpy as np
import holdem
import UnbiasedNet
import framework as fw
from threading import Condition, Lock
from collections import deque

def basebet(stage):
    if stage <=1:
        return 2
    else:
        return 4
#Emulate an autoplayer by blocking on human actions
class Human_player(fw.Auto_player):
    def __init__(self):
        #self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out, randomInit=False)
        self.status= fw.Status()
        self.name="Human"
        self.lock = Lock()
        self.doneSomething = Condition(self.lock)
        self.work = deque();
    def decision(self, player2, gameO=None, playerNum=-1,debug=0):
        with self.lock:
            if debug:
                print "it's the human's turn!"
            stage=self.status.stage
            while len(self.work)==0:
                self.doneSomething.wait()
            action = self.work.popleft()
            if action=="Call":
                next=self.status.call()
            elif action=="Check":
                next = self.status.check_first()
            elif action=="CheckFold":
                next = self.status.check_fold()
            elif action=="Raise":
                next = self.status.praise()
            elif action=="Fold":
                next = self.status.check_fold()
            self.status= next.copy()
            #update the other guy's status vector resulting from your act
            player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
            player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
            player2.status.stage= self.status.stage
            return action
    def humanAction(self, action):
        with self.lock:
            self.work.append(action)
            self.doneSomething.notify()
