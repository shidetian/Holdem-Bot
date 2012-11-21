import numpy as np
import UnbiasedNet
import holdem

def basebet(stage):
    if stage <=1:
        return 2
    else:
        return 4

class HandStat:
    '''
    Given a list of Card objects, analyze features like
    number of high cards, number of pairs,
    connected and suited
    '''
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards
        self.board = []

    def rank_list(self, cards=None):
        if cards is None:
            cards = self.cards
        return [card.num for card in cards]

    def suit_list(self, cards=None):
        if cards is None:
            cards = self.cards
        return [card.suit for card in cards]

    def update_board(self, cards=None, card=None):
        if card is None:
            self.board.extend(cards)
        else:
            self.board.append(card)

    def stat(self, cards=None, features=None):
        if cards is None:
            cards = self.cards
        stats = {}
        suits = self.suit_list(cards)
        ranks = self.rank_list(cards)
        if 14 in ranks:
            ranks.append( 1 ) # ace can be 1 in a wheel straight
        ranks = sorted( ranks )
        distances = [ ranks[i+1] - ranks[i] for i in range(len(ranks)-1) ]
        #------------Preflop's hand------------------------
        if len(cards) >= 2:
            stats['pair'] = int( distances.count(0) > 0 )    
            stats['2-connected'] = distances.count(1) + distances.count(2)
            suitCount = [suits.count(i) for i in range(4)]
            stats['2-suited'] = int( max(suitCount) >= 2 )
            stats['1-high'] = int( ranks[-1] > 12 )
            stats['2-high'] = int( ranks[-2] > 8 )

        #------------Flop's board------------------
        if len(cards) >= 3:
            stats['pairs'] = int( distances.count(0) > 1 ) # 3-of-a-kind too
            stats['3-suited'] = int( max(suitCount) >= 3 )
            # Find sum of consecutive distances for nonpair
            distanceSum = []
            stats['3-of-a-kind'] = 0 # or 4-of-a-kind
            for i in range(len(distances) - 1):
                if distances[i]>0 and distances[i+1]>0:
                    distanceSum.append( distances[i+1] + distances[i] )
                elif distances[i]==0 and distances[i+1]==0:
                    stats['3-of-a-kind'] = 1
            if distanceSum == []:
                distanceSum = [0] # to prevent min from raising error
            stats['3-connected'] = int( min(distanceSum) < 5 )
            stats['3-high'] = int( ranks[-3] > 7 )
        #-----------Turn's board--------------------
        if len(cards) >= 4:
            stats['4-suited'] = int( max(suitCount) >= 4 )
            distanceSum = [ distances[i+2] + distances[i+1] +
                            distances[i] for i in
                            range(len(distances) - 2) if
                            (distances[i]>0 and distances[i+1]>0
                             and distances[i+2]>0) ]
            if distanceSum == []:
                distanceSum = [0]
            stats['4-connected'] = int( min(distanceSum) < 5 )
        #----------River's board------------------------
        if len(cards) >= 5:
            stats['5-suited'] = int( max(suitCount) >= 5 )
            distanceSum = [ sum(distances[i+k] for k in range(4))
                            for i in range(len(distances) - 3) if
                            (distances[i]>0 and distances[i+1]>0
                             and distances[i+2]>0 and
                             distances[i+3]>0) ]
            if distanceSum == []:
                distanceSum = [0]
            stats['5-connected'] = int( min(distanceSum) < 5 )

        if features is None:
            return stats
        else:
            return [stats[key] for key in features]

    # 5 preflop features
    #
two_features = ['pair', '1-high', '2-high', '2-connected', '2-suited']
three_features = two_features + ['pairs', '3-high', '3-connected',
                            '3-suited', '3-of-a-kind']
four_features = three_features + ['4-suited', '4-connected']
five_features = four_features + ['5-suited', '5-connected']
final_features = ['pair', '1-high', '2-high', 'pairs', '3-of-a-kind',
                  '5-suited', '5-connected']



class StatStatus:
    '''
    vec_cards for vector of the cards' statistics 1 row for each stage
    At stage 0, only features in two_features are updated for all 4 rows
    At stage 1, more_features, 2 of them (1 for all 5 cards and 1 for
    the 3 table cards only), are updated for last 3 rows.
    #dealer=0 means not dealer, 
    #vec_act stands for action, is of dim 4*3, row corresponds to stage
    #column i is the bet of player i, 1<=i <=2; column 3 indicates whether 
    #this stage is over
    '''
    def __init__(self, dealer=0):
        self.vec_cards = {'my preflop': np.zeros(len(two_features)),
                        'flop': np.zeros(len(three_features)),
                        'my flop': np.zeros(len(five_features)),
                        'turn': np.zeros(len(four_features)),
                        'my turn': np.zeros(len(five_features)),
                        'river': np.zeros(len(five_features)),
                        'my river': np.zeros(len(final_features))}
        self.dealer=dealer
        self.vec_act=np.zeros((4,3))
        self.stage=0;
        self.cards = None
    def longvec(self):
        #this just concatenate the vectors
        return np.concatenate([ self.vec_cards['my preflop'],
                    self.vec_cards['flop'], self.vec_cards['my flop'],
                    self.vec_cards['turn'], self.vec_cards['my turn'],
                    self.vec_cards['river'], self.vec_cards['my river'],
                               np.array([self.dealer]),
                               self.vec_act[0], self.vec_act[1],
                               self.vec_act[2], self.vec_act[3],
                               np.array([self.stage])])
    def copy(self):
        new_one= StatStatus()
        new_one.vec_cards={key:self.vec_cards[key] for key in self.vec_cards}
        new_one.dealer=1*self.dealer
        new_one.vec_act=1*self.vec_act
        new_one.stage=1*self.stage
        new_one.cards = self.cards
        return new_one
    
    def update_preflop(self, cards):
        self.cards = list(cards) # needed later
        hand = HandStat( cards=cards )
        self.vec_cards['my preflop'] = hand.stat( features=two_features )
        
    def update_flop(self, table):
        #table is a list of Cards
        board = HandStat(table)
        self.vec_cards['flop'] = board.stat( features=three_features )
        my = HandStat( self.cards + table )
        self.vec_cards['my flop'] = my.stat( features=five_features )        
        self.stage=1
        
    def update_turn(self, table):
        board = HandStat(table)
        self.vec_cards['turn'] = board.stat( features=four_features )
        my = HandStat( self.cards + table )
        self.vec_cards['my turn'] = my.stat( features=five_features )
        self.stage=2
        
    def update_river(self, table):
        board = HandStat(table)
        self.vec_cards['river'] = board.stat( features=five_features )
        my = HandStat( self.cards + table )
        self.vec_cards['my river'] = my.stat( features=final_features )
        self.stage=3
        
    def check_fold(self):
        #go fraom one status to another status throught check/fold
        new_stat=self.copy()
        stage=self.stage
        new_stat.vec_act[stage]=(1*np.array([self.vec_act[stage][0], 
                                           self.vec_act[stage][1], 1]))
        new_stat.stage=stage+1
        return new_stat
    
    def check_first(self):
        #this happens when you are the first one to act and you check
        new_stat=self.copy()
        stage=self.stage
        new_stat.vec_act[stage]=(1*np.array([self.vec_act[stage][0], 
                                           self.vec_act[stage][1], 0])) 
        return new_stat
    def call(self):
        #calls
        new_stat=self.copy()
        stage=self.stage
        if stage==0 and self.vec_act[0][0]==1:
            new_stat.vec_act[stage]=1*np.array([2,2,0])
        else:
            new_stat.vec_act[stage]=(1*np.array([self.vec_act[stage][1], 
                                               self.vec_act[stage][1], 1]))
            new_stat.stage=stage+1
        return new_stat
    def praise(self):
        #raise
        new_stat=self.copy()
        stage=self.stage
        newbet=self.vec_act[stage][1]+basebet(stage)
        new_stat.vec_act[stage]=(1*np.array([newbet,
                                          self.vec_act[stage][1], 0]))
        return new_stat

class MyAutoPlayer:
   def __init__(self, neural_net, name= "anonymous", frenzy= False):
       self.name= name
       self.net= neural_net
       self.status=StatStatus()
       self.frenzy= frenzy
   def cum_bet(self):
       #compute the total bet 
       sum=0
       for i in range(4):
           sum = sum+ self.status.vec_act[i][0]
       return sum
   def decision(self, player2, debug=0):
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
       if (stage>0 and current.vec_act[stage][0]==0 and 
           player2.status.vec_act[stage][0]==0 and current.dealer==0):
           #this is the case when you are the first to act in a post-flop round
           possible_next=[current.check_first(), current.praise()]
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
       values=[0]*len(possible_next)
       if self.frenzy==False:
           for i in range(len(possible_next)):
               values[i] = self.net.predict(possible_next[i].longvec())[0]
               index=values.index(max(values))
       else:
           index= np.random.randint(0, len(possible_next))
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
   def post_blinds(self, player2, dealer=0):
       if dealer==0:
           dealer_player= player2
           nondealer_player= self
       else:
           dealer_player= self
           nondealer_player= player2
       nondealer_player.status.vec_act[0]=[2,1,0]
       dealer_player.status.vec_act[0]=[1,2,0]
   def action(self, player2, dealer=0, debug=0, game = None):
       stage= self.status.stage
       if (dealer==0 and stage==0) or (dealer==1 and stage>0) :
           first= player2
           second= self
       else:
           first= self
           second= player2
       while (1):
           game.performAction(first.decision(second, debug), (dealer==0 and stage==0) or (dealer==1 and stage>0))
           if debug:
               print "stage moved to ", first.status.stage, second.status.stage
               print first.status.vec_act[stage]
               print second.status.vec_act[stage]
           if (first.status.vec_act[stage][2]==1):
               break
           game.performAction(second.decision(first, debug), not ((dealer==0 and stage==0) or (dealer==1 and stage>0)))
           if debug:
               print "stage moved to", first.status.stage,second.status.stage
               print first.status.vec_act[stage]
               print second.status.vec_act[stage]
           if (second.status.vec_act[stage][2]==1):
               break
   
   def sim_one_hand(self, player2, game, dealer=0, debug=0):
       stat_seq=[]
       output=0
       #clear up possible leftover status from last game
       self.status=StatStatus(dealer=dealer)
       player2.status=StatStatus(dealer=1-dealer)
       #initialize the game and deal the pocket cards.
       game.setName(player2.name, self.name)
       #post the blind
       self.post_blinds(player2, dealer)
       #deal the hands
       self.status.update_preflop(game.players[0].cards)
       player2.status.update_preflop(game.players[1].cards)
       stat_seq.append(self.status.longvec())
       if debug:
           print "blinds:"
           print self.status.vec_act[0][0], self.status.vec_act[0][1]
       #pre-flop action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "preflop:", self.status.vec_act[0]
           print "preflop:", player2.status.vec_act[0]
       if (self.status.vec_act[0][0] < player2.status.vec_act[0][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[0][0] > player2.status.vec_act[0][0]):
           return (stat_seq, player2.cum_bet())
       #deal the flop
       #game._endStage_();
       self.status.update_flop(game.table)
       player2.status.update_flop(game.table)
       stat_seq.append(self.status.longvec())
       #flop action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "on the flop:"
           print self.status.vec_act[1][0], self.status.vec_act[1][1]
       if (self.status.vec_act[1][0]< player2.status.vec_act[1][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[1][0] > player2.status.vec_act[1][0]):
           return (stat_seq, player2.cum_bet())
       #deal the turn 
       #game._endStage_();
       self.status.update_turn(game.table)
       player2.status.update_turn(game.table)
       stat_seq.append(self.status.longvec())
       #turn action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "on the turn:" 
           print self.status.vec_act[2][0], self.status.vec_act[2][1]
       if (self.status.vec_act[2][0]< player2.status.vec_act[2][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[2][0] > player2.status.vec_act[2][0]):
           return (stat_seq, player2.cum_bet())
       #deal the river
       #game._endStage_()
       self.status.update_river(game.table)
       player2.status.update_river(game.table)
       stat_seq.append(self.status.longvec())
       #river action
       self.action(player2, dealer, debug, game)
       stat_seq.append(self.status.longvec())
       if debug:
           print "on the river:"
           print self.status.vec_act[3][0], self.status.vec_act[3][1]
       if (self.status.vec_act[3][0]< player2.status.vec_act[3][0]):
           return [stat_seq, -self.cum_bet()]
       elif (self.status.vec_act[3][0] > player2.status.vec_act[3][0]):
           return (stat_seq, player2.cum_bet())
       #show down
       game.stage=4
       res= game.checkWinner()
       # game.endRound()
       if (res[0]>res[1]):
           return (stat_seq, self.cum_bet())
       elif (res[0]< res[1]):
           return (stat_seq, -self.cum_bet())
       else:
           if debug:
               print "it's a tie"
           return (stat_seq, 0)

   def learn_one(self, stat_seq, output):
       #update all the weights
       #no matter which way we take to encode infomation,
       #this function should be virtually identical
       self.net.learnTD( stat_seq, output)
       return 
   def train(self,num_of_train, opponent, debug=0, frenzy=0):
       self.frenzy= frenzy
       game= holdem.Holdem(2, 4, 4, debug);
       for i in range(num_of_train):
           result=self.sim_one_hand(opponent, game, dealer=i%2, debug=debug)
           game.endRound()
           # print result[1]
           self.learn_one(result[0], result[1])
           self.status = StatStatus()
           opponent.status= StatStatus()
       self.frenzy= 0
   def compete(self, opponent, num_of_games=100, debug=1):
       start_cash=0
       game= holdem.Holdem(2, 4, 4, debug);
       for i in range(num_of_games):
           result=self.sim_one_hand(opponent, game, dealer=i%2, debug=debug)
           game.endRound()
           if debug:
               print "End of one hand. The winning is", result[1], "\n"
           start_cash= start_cash+ result[1]
       return start_cash


stat_rep = StatStatus()
n_in = len(stat_rep.longvec())
n_hidden = 40
n_out = 1
