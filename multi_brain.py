import anotherStatus as fw
import numpy as np
import holdem
import UnbiasedNet
import pickle
#list_of_opponents is a two dimension vector of size len(lis_of_bots)*4. 
#each column denotes 'Check', 'Call', 'Raise', 'CheckFold'
list_of_opponents=pickle.load(open("./bots/list_of_opponents.p", "rb"))

def distance(a, b):
    suma=0
    sumb=0
    for i in range(4):
        suma +=a[i]
        sumb +=b[i]
    for i in range(4):
        a[i]/= (suma*1.0)
        b[i]/= (sumb*1.0)
    distance=0
    for i in range(4):
        distance+= max(a[i],b[i])/min(a[i], b[i])
    return distance

class Multi_brain(fw.MyAutoPlayer):
    def __init__(self, list_of_bots, 
                 stat=None, name= "multi_core"):
        self.opponent_stat={'Check':1, 'Call':1, 'Raise':1, 'Fold':1}
        self.index_next_bot=0
        self.num_of_bots=len(list_of_bots)
        self.list_of_bots=list_of_bots
        if stat==None:
            self.status=fw.AnotherStatus()
        else:
            self.status=stat
        self.name=name
    def choose_bot(self):
        distances=[0]*self.num_of_bots
        opponent_stat_vec=[self.opponent_stat['Check'],
                           self.opponent_stat['Call'],
                           self.opponent_stat['Raise'],
                           self.opponent_stat['Fold']]
        for i in range(self.num_of_bots):
            distances[i]=distance(opponent_stat_vec, list_of_opponents[i])
        index_next_bot= distances.index(min(distances))
#       print 'list_of_opponents', list_of_opponents
#        print 'distances', distances
#        print 'opponent', opponent_stat_vec
        return index_next_bot
#    def decision(self, player2, gameO, palyerNum, debug=0):
#        active_bot=list_of_bots[self.next_bot]
#        action=active_bot.decision(player2, gameO, palyerNum, debug=debug)
#        self.status=active_bot.status.copy()
#        return action
    def sim_one_hand(self, player2, game, dealer=0, debug=0):
        next_bot=self.list_of_bots[self.index_next_bot]
        result=next_bot.sim_one_hand(player2, game, dealer=dealer)
        self.opponent_stat=game.history[1]
        self.index_next_bot=self.choose_bot()
        print "next_bot", self.index_next_bot
        return result

if __name__== "__main__":
    bot_beats_calling=pickle.load(open("./bots/specified_training_vs_calling_.005_0.6_0.5_0.5_0.02_0.15.p","rb"))
    bot_beats_betting=pickle.load(open("./bots/goodbot_less_fold_coarser_true_vs_betting_.005_0.65.p", "rb"))
    bot_beats_raising=pickle.load(open("./bots/specified_training_vs_raising_.005_0.6_0.5_0.5_0.05_0.0001.p", "rb"))
    bot_beats_Q1=pickle.load(open("./bots/goodbot_specified_training_vs_Q1_.005_.65.p","rb"))
    bot_beats_Q2=pickle.load(open("./bots/specified_training_vs_Q2_.005_0.7_0.5_0.5_0.05_0.15.p","rb"))
    bot_beats_Q3=pickle.load(open("./bots/specified_training_vs_Q3_.005_0.7_0.5_0.5_0.05_0.1realized.p","rb"))
    bot_beats_Q4=pickle.load(open("./bots/specified_training_vs_Q4_.005_0.6_0.5_0.5_0.05_0.05realized.p","rb"))
    bot_beats_Q5=pickle.load(open("./bots/specified_training_vs_Q5_.005_0.6_0.5_0.5_0.02_0.15.p","rb"))
    bot_beats_Q6=pickle.load(open("./bots/specified_training_vs_Q6_.005_0.6_0.5_0.5_0.1_0.2.p","rb"))
    bot_beats_Q7=pickle.load(open("./bots/specified_training_vs_Q7_.005_0.7_0.5_0.5_0.05_0.15.p","rb"))
    bot_beats_Q8=pickle.load(open("./bots/specified_training_vs_Q8_.005_0.6_0.5_0.5_0.1_0.05.p","rb"))
    list_of_bots=(bot_beats_calling, bot_beats_betting, bot_beats_raising,
                 bot_beats_Q1, bot_beats_Q2, bot_beats_Q3, bot_beats_Q4,
                 bot_beats_Q5, bot_beats_Q6, bot_beats_Q7, bot_beats_Q8)
    multi= Multi_brain(list_of_bots)
    pickle.dump(multi, open("./bots/multi_1.p", "wb"))
