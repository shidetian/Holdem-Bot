import numpy as np

def sigmoid(x, c=1):
    return 1.0 / (1 + np.exp( -c * x ))

def step(x):
    if x >= 0: return 1
    else: return 0

def biased(x):
    # add the entry 1 to the front of an list/array
    return np.append( 1, x )
    

class BiasedPerceptron:
    # same as Neural network, excpet n_hidden, n_out is not used.
    def __init__(self, n_in, n_hidden=50, n_out=1, alpha=0.001, lamb=0.9, randomInit=True):
        # Size of the network
        self.n_in = n_in
        self.n_out = 1
        # parameters
        self.alpha = alpha
        self.lamb = lamb
        # Weight vectors
        self.w = np.random.uniform(-.5, .5, (n_in + 1, n_out))
        
    def deepcopy(self):
        newnet= BiasedPerceptron(self.n_in, 50, self.n_out,
                          alpha=self.alpha, lamb=self.lamb)
        newnet.w= 1* self.w
        return newnet

    ###### Predicting
    def predict(self, x):
        # Given x, an array of n_in input,
        # return a np.array of the hidden
        return np.dot( np.transpose(self.w), biased(x) )


    ############# supervised Learning
    def learnOnline(self, x, y, alpha=.5):
        '''
        learning for neural network
        '''
        # hBiased is 2-dimensional: 1 by n_hidden+1
        o = self.predict(x)
        error = y - o
        self.w += alpha * error * biased(x)[:, np.newaxis]

    def learnTD(self, xLis, y):
        '''
        matrix implementation of learnTD
        learning for 1 entire round, with x being a 2d array
        and y be the payout at the end
        '''
        trace = np.zeros((self.n_in + 1, self.n_out))
        w_change = np.zeros((self.n_in + 1, self.n_out))
        for i in range(len(xLis)):
            # n_in + 1
            currX = xLis[i]
            xBiased = biased( currX )[:,np.newaxis]
            # n_out
            currY = self.predict( currX )
            if i < len(xLis) - 1:
                nextY = self.predict( xLis[i+1] )
                error = nextY - currY
            else: # last update's reward is the payout y.
                error = y - currY
            trace *= self.lamb
            trace += xBiased
            w_change += self.alpha * error * trace
            
        self.w += w_change
