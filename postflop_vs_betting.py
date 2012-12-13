import pickle
import UnbiasedNet
import postflopStatus as fw
from calling_station import Calling_station
from betting_station import Betting_station 

result_name = 'postflop_vs_betting.txt'
ALPHA = 0.005
n_train = 100000

stat_obj = fw.AnotherStatus()
n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )
n_cards += 1 # This includes dealer info

for init in [True, False]:
    for LAMB in [0.65, 0.7, 0.75, 0.8, 0.85, 0.9]:
        name = 'postflop_vs_betting_.005_' + str(LAMB) + '_1e5.p'
        
        print n_cards

        net = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out, randomInit=True,
                                   alpha=ALPHA, alpha_win=2*ALPHA, lamb=LAMB,
                                    subdiv=[(0,0), (n_cards,n_cards),
                                            (fw.n_in,n_cards)])
        auto = fw.AnotherAutoPlayer(net, name="superbot")
        ai = Betting_station()
        auto.train(n_train, ai, debug=0, frenzy=1)
        pickle.dump(auto, open(name, "wb"))

        result = []
        for i in range(10):
            result.append( auto.compete(ai, 5000, debug=0) )
        data = '\n Learning rate: ' + str(ALPHA)
        data += '\n Lambda: ' + str(LAMB)
        data += '\n Number of training: ' + str(n_train)
        data += '\n Results: ' + str(result)
        print data
        
        
        with open(result_name, 'a') as f:
            f.write(data)
