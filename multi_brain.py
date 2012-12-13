import framework.py as fw
import numpy as np
import holdem
import UnbiasedNet
import pickle
#list_of_opponents is a two dimension vector of size len(lis_of_bots)*4. 
#each column denotes 'Check', 'Call', 'Raise', 'CheckFold'
list_of_opponents=pickle.load(open("list_of_opponents.p", "rb"))

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

class multi_brain(fw.Auto_player):
    def __init__(self, opponent_stat, next_bot, num_of_bots, list_of_bots, 
                 stat=None, name= "multi_core"):
        self.opponent_stat={'Check':0, 'Call':0, 'Raise':0, 'CheckFold':0}
        self.next_bot=0
        self.num_of_bots=len(list_of_bots)
        self.list_of_bots=list_of_bots
        if stat==None:
            self.status=Status()
        else:
            self.status=stat
    def choose_bot(self):
        distances=[0]*num_of_bots
        opponent_stat_vec=(self.opponent_stat['Check'],
                           self.opponent_stat['Call'],
                           self.opponent_stat['Raise'],
                           self.opponent_stat['CheckFold'])
        for i in range(num_of_bots):
            distances[i]=distance(opponent_stat_vec, list_of_opponents[i])
        self.next_bot= distances.index(min(distances))
    def compete(self, opponent, num_of_games=100, debug=0):
        start_cash=0
        
