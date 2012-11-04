import numpy as np

def sigmoid(x, c=1):
    return 1.0 / (1 + np.exp( c * x ))

def biased(x):
    # add the entry 1 to the front of a row vector.
    # Any methods using this only deal with row vector (not rows of vectors).
    return np.append( 1, x )

class NeuralNet:

    def __init__(self, n_in, n_hidden, n_out):
        # Size of the network
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.n_out = n_out
        # Weight vectors
        self.w_in = np.ones( (n_hidden+1, n_in + 1) ) ## To be randomized
        self.w_out = np.ones( (n_out, n_hidden + 1) )

    def in_to_hidden(self, x):
        # Given a a numpy row vector, produce hidden "binary" predictions
        return sigmoid(np.dot( biased(x), np.transpose(self.w_in) ))

    def hidden_to_out(self, h):
        return np.dot( h, np.transpose(self.w_out) )

    def predict(self, x):
        return self.hidden_to_out( in_to_hidden( x ) )

    def learn(self, x, y, alpha=0.1, beta=0.1):
        # Given a training example (x,y), this updates the weight vectors
        h = self.in_to_hidden(x)
        error_out = y - self.predict(x)
        delta_in = h * (1 - h) * np.dot(error_out, self.w_out)
        self.w_out += beta * np.dot( np.transpose(error_out), h )
        self.w_in += alpha * np.dot( np.transpose(delta_in), biased(x) )

    def predictBinary(self, x):
        # standard neural network with 0,1 predictions
        return sigmoid(self.hidden_to_out( in_to_hidden( x ) ))

    def learnBinary(self, x, y, alpha=0.1, beta=0.1):
        # learning for neural network with 0,1 predictions
        h = self.predictBinary(x)
        o = self.predictBinaory(x)
        error_out = y - o
        delta_out = o * (1 - o) * error_out
        delta_in = h * (1 - h) * np.dot(error_out, self.w_out)
        self.w_out += beta * np.dot( np.transpose(delta_out), h )
        self.w_in += alpha * np.dot( np.transpose(delta_in), biased(x) )

    def learnTD(self, x, y, trace_in=None, trace_out=None,
                alpha=0.1, beta=0.1, lamb=0.8):
        ## Make sure the algorithm is correct
        ## error_out replaces gradient_out in the AI homework
        ## trace is the eligibility trace denoted by e before.
        h = self.in_to_hidden(x)
        error_out = y - self.predict(x)
        delta_in = h * (1 - h) * np.dot(error_out, self.w_out)
        if trace_in is None:
            trace_in = np.zeros((self.n_hidden+1, self.n_in+1))
        if trace_out is None:
            trace_out = np.zeros((self.n_out, self.n_hidden+1))
        trace_in = lamb*trace_in - np.dot(np.transpose(delta_in), biased(x))
        trace_out = lamb*trace_out - np.dot(np.transpose(error_out), h)
        
        self.w_out += beta * error_out * trace_out
        self.w_in += alpha * error_out * trace_in
        
net = NeuralNet(3, 2, 1)
# Testing in_to_hidden for row matrix of size 2
# and 2 time steps time steps
data = np.array([0, 0, 0])
h = net.in_to_hidden( data )
print "The input is \n", data
print "The hidden output is \n", h
print "Sigmoid of h is \n", sigmoid(h)

# Testing hidden_to_out
print "The output is \n", net.hidden_to_out( h )
