import pickle
auto=pickle.load(open("preflop_bot", "rb"))
print auto.net.w_in
print len(auto.net.w_in)
