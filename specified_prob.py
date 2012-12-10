import framework
import numpy
import UnbiasedNet
from framework import *

class specified_prob(framework.Auto_player):
    def __init__(self, stat=None, name="anonymous", 
                 prob_list={'Check':0.25,'Call':0.25, 'Raise':0.25, 
                            'CheckFold':0.25}):
        self.name=name
        if stat==None:
            self.status=framework.Status()
        else:
            self.status=stat
        self.prob_list=prob_list
    def decision_helper(self):
        x=numpy.random.rand()
        if x < self.prob_list['Check']:
            return 'Check'
        elif x<self.prob_list['Check']+self.prob_list['Call']:
            return 'Call'
        elif x< (self.prob_list['Check']+self.prob_list['Call']+
                 self.prob_list['Raise']):
            return 'Raise'
        else:
            return 'CheckFold'
    def decision(self, player2, gameO, playerNum, debug=0):
        #make decision on next move
        if debug:
            print "it's "+self.name+" 's turn!"
        possible_next=[]
        current= self.status
        stage=current.stage
        if (stage>0 and current.vec_act[stage][0]==0 and 
            current.dealer==0 and player2.status.vec_act[stage][0]==0):
           #this is the case when you are the first to act in a post-flop round
            possible_next=[current.check_first(), current.praise()]
            game_actions = ["Check", "Raise"]
        elif (current.vec_act[stage][1]< 4*basebet(stage)):
           #this is the case when you are not in first case, and you may still
           #raise
            possible_next=[current.check_fold(), 
                           current.call(), current.praise()]
            game_actions = ["CheckFold", "Call", "Raise"]
        else:
           #all other cases
            possible_next=[current.check_fold(), current.call()]
            game_actions = ["CheckFold", "Call"]
        action=self.decision_helper()
        while action not in game_actions:
            action=self.decision_helper()
        index=game_actions.index(action)
        self.status = possible_next[index].copy()
       #update the other guy's status vector resulting from your act
        player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
        player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
        player2.status.stage= self.status.stage
        if debug:
           #print "after the decision is made at stage:", stage
           #print self.status.vec_act[stage]
           #print player2.status.vec_act[stage]
            print self.name+" decided to ", game_actions[index]
        return game_actions[index]

if __name__== "__main__":
    net= UnbiasedNet.NeuralNet(framework.n_in, framework.n_hidden, 
                               framework.n_out, alpha=0.1,
                               lamb=0.9, randomInit=True)
    auto= framework.Auto_player(net, name="auto")

    auto2=specified_prob(prob_list={'Check':0.1, 'Call': 0.2, 'Raise':0.3,
                                   'CheckFold':0.4})
    auto.train(10, auto2, debug=1)
    auto.compete(auto2)
