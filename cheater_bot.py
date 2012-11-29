import numpy as np
import holdem
from holdem import Card
import UnbiasedNet
import framework as fw
from threading import Condition, Lock
from collections import deque
from subprocess import call, check_output
from random import random
#when set to true, always stays in if percentage is higher, else fold with probabiliity of other player winning
isAgressive=False
def basebet(stage):
	if stage <=1:
		return 2
	else:
		return 4
#Emulate an autoplayer by blocking on human actions
class Cheater_player(fw.Auto_player):
	def __init__(self):
		#self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out, randomInit=False)
		self.status= fw.Status()
		self.name="Cheater"
		#self.doneSomething = Condition(self.lock)
		#self.work = deque();
	def decision(self, player2, gameO=None, playerNum=-1,debug=0):
		if debug:
			print "it's the Cheater's turn!"
		assert gameO!=None
		assert playerNum!=-1
		#0 preflop
		stage=self.status.stage
		current= self.status
		odds = calculateOddsWithGame(gameO, playerNum)
		shouldFold = odds[1]-(odds[0]+(5-stage)/5.0 * random()) > 0
		if (stage>0 and current.vec_act[stage][0]==0 and 
			current.dealer==0 and player2.status.vec_act[stage][0]==0):
			#this is the case when you are the first to act in a post-flop round
			#possible_next=[current.check_first(), current.praise()]
			#raise with diff in probability
			if (odds[0]-odds[1])+0.5 > random():
				action = "Raise"
				next = self.status.praise()
			else:
				action = "Check"
				next = self.status.check_first()
			#game_actions = ["Check", "Raise"] 
		elif (current.vec_act[stage][1]< 4*basebet(stage)):
			#this is the case when you are not in first case, and you may still
			#raise
			#possible_next=[current.check_fold(), 
			#			  current.call(), current.praise()]
			if shouldFold:
				action = "CheckFold"
				next = self.status.check_fold()
			elif (odds[0]-odds[1])+0.5 > random():
				action = "Raise"
				next = self.status.praise()
			else:
				action= "Call"
				next=self.status.call()
			#game_actions = ["CheckFold", "Call", "Raise"]
		else:
			#all other cases
			#possible_next=[current.check_fold(), current.call()]
			if shouldFold:
				action="CheckFold"
				next = self.status.check_fold()
			else:
				action="Call"
				next=self.status.call()
			#game_actions = ["CheckFold", "Call"]
		self.status= next.copy()
		#update the other guy's status vector resulting from your act
		player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
		player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
		player2.status.stage= self.status.stage
		return action
def all_indices(value, qlist):
	return np.nonzero(qlist)[0].tolist()

def calculateOddsWithGame(game, playerNum):
	tempCard = Card(1,2)
	myCards = game.players[playerNum].cards
	opCards = game.players[not playerNum].cards
	
	args = [tempCard.getCardOfNumA(myCard.num)+tempCard.getCharOfSuit(myCard.suit) for myCard in myCards]
	args += [tempCard.getCardOfNumA(myCard.num)+tempCard.getCharOfSuit(myCard.suit) for myCard in opCards]
	args+=["--"]
	args += [tableCards.getCardOfNumA(tableCards.num)+tableCards.getCharOfSuit(tableCards.suit) for tableCards in game.table]
	return [float(num) for num in (check_output(["pokenum.exe", "-h", "-t"] + args).split()[2:])]

def calculateOdds(player1, player2, stage):
	tempCard = Card(1,2)
	#print player2.status.vec_cards
	#print player1.status.vec_cards
	myCards = [tempCard.num_to_card(num) for num in all_indices(1, player1.status.vec_cards[0])]
	#myCards = Card.num_to_card(self.status.vec_cards[0])
	opCards = [tempCard.num_to_card(num) for num in all_indices(1, player2.status.vec_cards[0])]
	args = [tempCard.getCardOfNumA(myCard.num)+tempCard.getCharOfSuit(myCard.suit) for myCard in myCards]
	args += [tempCard.getCardOfNumA(myCard.num)+tempCard.getCharOfSuit(myCard.suit) for myCard in opCards]
	args+=["--"]
	if stage>=1:
		flopCards = [tempCard.num_to_card(num) for num in all_indices(1, player1.status.vec_cards[1])]
		args += [turnCard.getCardOfNumA(turnCard.num)+turnCard.getCharOfSuit(turnCard.suit) for turnCard in flopCards]
	if stage>=2:
		turnCards = [tempCard.num_to_card(num) for num in all_indices(1, player1.status.vec_cards[2])]
		args += [turnCard.getCardOfNumA(turnCard.num)+turnCard.getCharOfSuit(turnCard.suit) for turnCard in turnCards]
	if stage>=3: #should be just one 
		riverCards = [tempCard.num_to_card(num) for num in all_indices(1, player1.status.vec_cards[3])]
		args += [turnCard.getCardOfNumA(turnCard.num)+turnCard.getCharOfSuit(turnCard.suit) for turnCard in riverCards]
	#print check_output(["pokenum.exe", "-h"] + args)
	return [float(num) for num in (check_output(["pokenum.exe", "-h", "-t"] + args).split()[2:])]
