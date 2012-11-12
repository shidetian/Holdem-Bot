import numpy as np

def sigmoid(x, c=1):
    return 1.0 / (1 + np.exp( -c * x ))

def step(x):
    if x >= 0: return 1
    else: return 0

class NeuralNet:

    def __init__(self, n_in, n_hidden, n_out, alpha=.5, beta=.5, lamb=1.0,
                 randomInit=True):
        # Size of the network
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.n_out = n_out
        # Parameters
        self.alpha = alpha
        self.beta = beta
        self.lamb= lamb
        # Weight vectors
        if randomInit:
            self.w_in = np.random.uniform(-.5, .5, (n_in, n_hidden))
            self.w_out = np.random.uniform(-.5, .5, (n_hidden, n_out))
        else:
            self.w_in = np.ones((n_in, n_hidden))
            self.w_out = np.ones((n_hidden, n_out))

    ####### Predicting
    def in_to_hidden(self, x):
        # Given x, an array of n_in input,
        # return a np.array of the hidden
        return sigmoid(np.dot( np.array(x), self.w_in ))

    def hidden_to_out(self, h):
        # Given h, an array of n_out hidden input,
        # return the predicted real valued
        return np.dot( h, self.w_out )

    def predict(self, x):
        # Given input, return a 1d np.array of real-valued output
        return self.hidden_to_out( self.in_to_hidden( x ) )
    
    ####### supervised learning
    def learnOnline(self, x, y):
        '''
        Supervised learning for neural network.
        This should give the same result as TD(1).
        '''
        # hBiased is 2-dimensional: 1 by n_hidden+1
        x = np.array( x )
        x = x[np.newaxis, : ]
        h = self.in_to_hidden(x)
        o = self.predict(x)
        error_out = y - o
        delta_out = error_out
        delta_in =  h * (1 - h) * np.dot( error_out, np.transpose(self.w_out) )
        # n_hidden+1 by 1 * n_out gives n_hidden+1 by n_out
        
        self.w_out += self.beta * np.transpose(h) * delta_out
        # n_in+1 by 1 * n_hidden gives n_in+1 by n_hidden
        self.w_in += self.alpha * np.transpose(x) * delta_in
        
    ######### reinforcement learning
    def learnTD(self, xLis, y):
        '''
        learning for 1 entire round, with x being a 2d array
        and y be the payout at the end
        '''
        trace_in = np.zeros((self.n_in, self.n_hidden, self.n_out))
        trace_out = np.zeros((self.n_hidden, self.n_out))
        w_out_change = np.zeros((self.n_hidden, self.n_out))
        w_in_change = np.zeros((self.n_in, self.n_hidden))
        for i in range(len(xLis)):
            # n_in + 1
            currX = xLis[i]
            # n_hidden + 1
            h = self.in_to_hidden( currX )
            # n_out
            currY = self.predict( currX )
            if i < len(xLis)-1:
                nextY = self.predict( xLis[i+1] )
                error_out = nextY - currY
            else: # last update's reward is the payout y.
                error_out = y - currY
            trace_out *= self.lamb
            trace_in *= self.lamb            
            for j in range(self.n_hidden):
                for k in range(self.n_out):
                    trace_out[j][k] += h[j]
                    for i in range(self.n_in):
                        # c * h * (1 - h) is the gradient of sigmoid
                        trace_in[i][j][k] += ( h[j] *(1 - h[j]) *
                                              self.w_out[j][k] * currX[i])
            for j in range(self.n_hidden):
                for k in range(self.n_out): 
                    w_out_change[j][k] += self.beta * error_out[k] * trace_out[j][k]
                for i in range(self.n_in):
                    w_in_change[i][j]+=self.alpha * sum( error_out[k]
                                * trace_in[i][j][k] for k in range(self.n_out) )
        self.w_out += w_out_change
        self.w_in += w_in_change

