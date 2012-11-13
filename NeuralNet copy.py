import numpy as np

def sigmoid(x, c=1):
    return 1.0 / (1 + np.exp( c * x ))

def biased(x):
    # add the entry 1 to the front of a row vector.
    # Any methods using this only deal with row vector (not rows of vectors).
    one = np.append( 1, x )
    return np.resize(one, (1,one.shape[-1]))

class NeuralNet:

    def __init__(self, n_in, n_hidden, n_out):
        # Size of the network
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.n_out = n_out
        # Weight vectors
        self.w_in = np.ones( (n_hidden+1, n_in + 1) ) ## To be randomized
        self.w_out = np.ones( (n_out, n_hidden + 1) )
        self.trace_in = np.zeros((self.n_hidden+1, self.n_in+1))
        self.trace_out = np.zeros((self.n_out, self.n_hidden+1))
        self.alpha = .5
        self.beta = .5
        self.lamb =.8

    def resetTrace(self):
        self.trace_in = np.zeros((self.n_hidden+1, self.n_in+1))
        self.trace_out = np.zeros((self.n_out, self.n_hidden+1))

    def in_to_hidden(self, x):
        # Given a a numpy row vector, produce hidden "binary" results
        return sigmoid(np.dot( biased(x), np.transpose(self.w_in) ))

    def hidden_to_out(self, h):
        return np.dot( h, np.transpose(self.w_out) )

    def predict(self, x):
        return self.hidden_to_out( in_to_hidden( x ) )

    def learn(self, x, y):
        # Given a training example (x,y), this updates the weight vectors
        h = self.in_to_hidden(x)
        error_out = y - self.predict(x)
        delta_in = h * (1 - h) * np.dot(error_out, self.w_out)
        self.w_out += self.beta * np.dot( np.transpose(error_out), h )
        self.w_in += self.alpha * np.dot( np.transpose(delta_in), biased(x) )

    def predictBinary(self, x):
        # standard neural network with 0,1 predictions
        return sigmoid(self.hidden_to_out( self.in_to_hidden( x ) ))

    def learnBinary(self, x, y):
        # learning for neural network with 0,1 predictions
        h = self.in_to_hidden(x)
        o = self.predictBinary(x)
        error_out = y - o
        delta_out = o * (1 - o) * error_out
        delta_in = h * (1 - h) * np.dot(error_out, self.w_out)
        self.w_out += self.beta * np.dot( np.transpose(delta_out), h )
        self.w_in += self.alpha * np.dot( np.transpose(delta_in), biased(x) )

    def batchLearnBinary(self, data, iterations=None):
        # data[0] is a 2d array of inputs and data[1] is the list of targets.
        # Target of data[0][k] is data[1][k]
        dataSize = len(data[1])
        assert len(data[0]) == dataSize
        assert len(data[0][0]) == self.n_in
        error = [ True ] * dataSize
        if iterations is None:
            iterations = 0
            while True in error:
                k = np.random.random_integers( dataSize ) - 1
                self.learnBinary( data[0][k], data[1][k] )
                # test for error
                for j in range( len(error) ):
                    if self.predictBinary( data[0][j] ) > 0.5:
                        if data[1][j] == 1:
                            error[j] = True
                        else:
                            error[j] = False
                    else:
                        if data[1][j] == 1:
                            error[j] = False
                        else:
                            error[j] = True
                iterations += 1
            return iterations

        else:           
            for it in range(iterations) :
                for k in range( len(data[1]) ):
                    self.learnBinary( data[0][k], data[1][k])
                    print self.w_in
                    print self.w_out

    def learnTD(self, x, y):
        ## error_out replaces gradient_out in the AI homework
        ## trace is the eligibility trace denoted by e before.
        h = self.in_to_hidden(x)
        error_out = y - self.predict(x)
        delta_in = h * (1 - h) * np.dot(error_out, self.w_out)
        
        self.trace_in *= self.lamb
        self.trace_in -= np.dot(np.transpose(delta_in), biased(x))
        #? the following is correct?
        self.trace_out *= self.lamb
        self.trace_out -= np.dot(np.transpose(error_out), h)
        
        self.w_out += self.beta * error_out * trace_out
        self.w_in += self.alpha * error_out * trace_in
        
if __name__ == "__main__":
    net = NeuralNet(3, 2, 1)
# Testing in_to_hidden for row matrix
    data = np.array([0, 0, 0])
    h = net.in_to_hidden( data )
    print "The input is \n", data
    print "The hidden output is \n", h
    print "Sigmoid of h is \n", sigmoid(h)
    
# Testing hidden_to_out
    print "The output is \n", net.hidden_to_out( h )
    
# XOR data
    xor = [np.array( [[0,0],
                      [0,1],
                      [1,0],
                      [1,1]] ),
           [0,1,1,0] ]
    net = NeuralNet(2, 6, 1)
    net.batchLearnBinary( xor )
