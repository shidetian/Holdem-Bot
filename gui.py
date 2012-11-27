import Tkinter
from tkFileDialog import askopenfilename
import pickle
from human_player import Human_player
from Tkinter import *
from holdem import *
#from PIL import Image, ImageTk
from framework import *
from threading import Thread
import time
from HandStat import *

running = False
class SimulationThread(Thread):
	def __init__(self, p1, p2, game):
		Thread.__init__(self)
		self.p1 = p1
		self.p2 = p2
		self.game = game
	def run(self):
		global running
		self.p1.sim_one_hand(self.p2, self.game, dealer=not self.game.dealer, debug=1)
		running = False
	def kill(self):
		raise NameError("Killed")
class HoldemGUI():
	def __init__(self):
		self.game = None
		self.p1 = None
		self.p2 = Human_player()
		tk = Tkinter
		
		root = tk.Tk()
		#cv = tk.Canvas(root, width=800, height=600)
		#cv.pack(side=tk.LEFT)
		
		#load card images
		c = Card(1,1)
		self.cards= {}
		for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
			for card in range(2,15):
				#self.cards[card, suit[0]]=tk.PhotoImage(Image.open("D:\\Dropbox\\CS4780\\Project\\Machine-Learning\\cards\\"+suit+"\\"+c.getCardOfNum(card)+suit[0]+".eps"))
				self.cards[card, suit[0]] = tk.PhotoImage(file=".\\cards_gif\\"+suit[0].lower()+c.getCardOfNum(card).lower()+".gif")
		self.unknownCard = tk.PhotoImage(file=".\\cards_gif\\b2fv.gif")
		root.title("Hold'em Poker")
		root.minsize(800, 600)

		#need self.backbround b/c python garbage collects it otherwise
		self.backGround = tk.PhotoImage(file=".\\bkg.gif")
		backGroundLabel = tk.Label(root, image=self.backGround)
		backGroundLabel.place(x=0,y=0, relwidth=1, relheight=1)
		
		tpFrame = tk.Frame(root)
		tpFrame.pack(side = tk.TOP, fill = tk.Y)
		
	
		self.newGameB = tk.Button(tpFrame, text="New Game", command=self.newGame)
		self.newGameB.config(state=DISABLED)
		self.newGameB.pack(side=tk.LEFT)
		
		loadBotB = tk.Button(tpFrame, text="Load Bot", command=self.loadBot)
		loadBotB.pack(side=tk.LEFT)
		
		showCardsB = tk.Button(tpFrame, text="Show Hand", command = self.displayPocketCards)
		showCardsB.pack(side=tk.LEFT)
		
		p1ActionFrame = tk.Frame(root)
		p1ActionFrame.pack(side=tk.TOP, fill = tk.Y)
		self.p1Action = tk.StringVar()
		p1ALabel = tk.Label(p1ActionFrame, textvariable=self.p1Action)
		p1ALabel.pack(side=tk.LEFT)
		
		#holds the frames for displaying each player's cards as well as table
		tableFrame = tk.Frame(root, width=800, height=600)
		tableFrame.place(in_=root, anchor="c", relx=.5, rely=.5)
		#tableFrame.pack(side=tk.TOP, fill=tk.Y)
		p1Frame = tk.Frame(tableFrame, bg="white", width=800, height=100)
		p1Frame.pack(side=tk.TOP)
		
		self.p1Card1 = Label(p1Frame, text = "P1 C1")
		self.p1Card1.pack(side=tk.LEFT, fill=tk.X)
		self.p1Card2 = Label(p1Frame, text = "P1 C2")
		self.p1Card2.pack(side=tk.LEFT, fill=tk.X)
		
		communityFrame = tk.Frame(tableFrame, width=800, height=400)
		communityFrame.pack(side=tk.TOP, fill=tk.BOTH)
		#labels hold will hold cards
		self.f1Card = Label(communityFrame, text = "Flop1")
		self.f1Card.pack(side=tk.LEFT)
		self.f2Card = Label(communityFrame, text = "Flop2")
		self.f2Card.pack(side=tk.LEFT)
		self.f3Card = Label(communityFrame, text = "Flop3")
		self.f3Card.pack(side=tk.LEFT)
		self.tCard = Label(communityFrame, text = "Turn")
		self.tCard.pack(side=tk.LEFT)
		self.rCard = Label(communityFrame, text = "River")
		self.rCard.pack(side=tk.LEFT)
		p2Frame = tk.Frame(tableFrame, width=800, height=100)
		p2Frame.pack(side=tk.BOTTOM)
		
		self.p2Card1 = tk.Label(p2Frame, text = "P2 C1", image = None)
		self.p2Card1.pack(side=tk.LEFT)
		self.p2Card2 = Label(p2Frame, text = "P2 C2")
		self.p2Card2.pack(side=tk.LEFT)
		
		#Frame holding player action button
		btFrame = tk.Frame(root)
		btFrame.pack(side=tk.BOTTOM, fill = tk.Y)
		
		p2ActionFrame = tk.Frame(root)
		p2ActionFrame.pack(side=tk.BOTTOM, fill = tk.Y)
		self.p2Action = tk.StringVar()
		p2ALabel = tk.Label(p2ActionFrame, textvariable=self.p2Action)
		p2ALabel.pack(side=tk.LEFT)
		
		self.checkB = tk.Button(btFrame, text="Check", command=self.pCheck)
		self.checkB.pack(side=LEFT)
		self.callB = tk.Button(btFrame, text = "Call", command=self.pCall)
		self.callB.pack(side=LEFT)
		self.raiseB = tk.Button(btFrame, text="Raise", command=self.pRaise)
		self.raiseB.pack(side=LEFT)
		self.foldB = tk.Button(btFrame, text="Fold", command=self.pFold)
		self.foldB.pack(side=LEFT)
		self.endRoundB = tk.Button(btFrame, text="End Round", command=self.pEndRound)
		self.endRoundB.pack(side=LEFT)
	def pCheck(self):
		self.p2.humanAction("CheckFold")
		#self.p2Action.set("Check")
		self.toggleButtons()
	def pRaise(self):
		#self.p2Action.set("Raise")
		self.p2.humanAction("Raise")
		self.toggleButtons()
	def pCall(self):
		#self.p2Action.set("Call")
		self.p2.humanAction("Call")
		self.toggleButtons()
	def pFold(self):
		#self.p2Action.set("Fold")
		self.p2.humanAction("Fold")
		self.toggleButtons()
	def updateAction(self, args):
		(player, action) = args
		if player==0:
			self.p1Action.set(action)
			self.p2Action.set("")
		elif player==1:
			self.p2Action.set(action)
			self.p1Action.set("")
	def toggleButtons(self, ignored=None):
		#time.sleep(0.5)
		(checkAllowed, callAllowed, raiseAllowed, foldAllowed) = self.game.allowableActions(1)
		if checkAllowed:
			self.checkB.config(state=NORMAL)
		else:
			self.checkB.config(state=DISABLED)
		if callAllowed:
			self.callB.config(state=NORMAL)
		else:
			self.callB.config(state=DISABLED)
		if raiseAllowed:
			self.raiseB.config(state=NORMAL)
		else:
			self.raiseB.config(state=DISABLED)
		if foldAllowed:
			self.foldB.config(state=NORMAL)
		else:
			self.foldB.config(state=DISABLED)
		self.updateTableCards()
	def pEndRound(self):
		self.game.endRound()
		self.playHand()
		self.cleanUpCards()
		self.displayPocketCards(1)
	def newGame(self):
		self.game = Holdem(5,10, debug=True)
		self.game.registerCallBack(HoldemGUI.toggleButtons, self)
		self.game.registerCallBack(HoldemGUI.updateAction, self)
		self.cleanUpCards()
		self.displayPocketCards(1)
		self.playHand()
	#Note this might be problematic if sim_one_hand hangs for some reason
	def playHand(self):
		global running
		if running:
			print "Simulation thread still running, further actions will lead to kittens dying\n"
			print "Attempting to kill..."
			try:
				self.simThread.kill()
			except NameError:
				print "Killed"
		running=True
		self.simThread = SimulationThread(self.p1,self.p2,self.game)
		self.simThread.start()
	def updateTableCards(self):
		if len(self.game.table)>=3:
			#print "Update table cards"
			self.f1Card.config(image = self.cards[self.game.table[0].num, self.game.table[0].getCharOfSuit(self.game.table[0].suit)])
			self.f2Card.config(image = self.cards[self.game.table[1].num, self.game.table[1].getCharOfSuit(self.game.table[1].suit)])
			self.f3Card.config(image = self.cards[self.game.table[2].num, self.game.table[2].getCharOfSuit(self.game.table[2].suit)])
		if len(self.game.table)>=4:
			self.tCard.config(image = self.cards[self.game.table[3].num, self.game.table[3].getCharOfSuit(self.game.table[3].suit)])
		if len(self.game.table)>=5:
			self.rCard.config(image = self.cards[self.game.table[4].num, self.game.table[4].getCharOfSuit(self.game.table[4].suit)])
	#0 to display 0, 1 to display player 1, 2 to display all
	def displayPocketCards(self, player=2):
		#print "Called"
		if self.game==None:
			return
		if player==1 or player==2:
			p2Cards = self.game.players[1].cards
			self.p2Card1.config(image = self.cards[p2Cards[0].num, p2Cards[0].getCharOfSuit(p2Cards[0].suit)])
			self.p2Card2.config(image = self.cards[p2Cards[1].num, p2Cards[1].getCharOfSuit(p2Cards[1].suit)])
		if player==0 or player==2:
			p1Cards = self.game.players[0].cards
			self.p1Card1.config(image = self.cards[p1Cards[0].num, p1Cards[0].getCharOfSuit(p1Cards[0].suit)])
			self.p1Card2.config(image = self.cards[p1Cards[1].num, p1Cards[1].getCharOfSuit(p1Cards[1].suit)])
		#self.p2Card1.config(image = self.backGround)
	def cleanUpCards(self):
		self.f1Card.configure(image=self.unknownCard)
		self.f2Card.config(image=self.unknownCard)
		self.f3Card.config(image=self.unknownCard)
		self.tCard.config(image=self.unknownCard)
		self.rCard.config(image=self.unknownCard)
		self.p1Card1.config(image=self.unknownCard)
		self.p2Card2.config(image=self.unknownCard)
		self.p1Card2.config(image=self.unknownCard)
		self.p2Card1.config(image=self.unknownCard)
		self.p1Action.set("")
		self.p2Action.set("")
	def loadBot(self):
		filename = askopenfilename()
		if filename=="":
			return
		self.p1 = pickle.load(open(filename, "rb"))
		self.p1.debug=True
		self.newGameB.config(state=NORMAL)
	#t.ondrag(clickHandler)
	def startGUI(self):
		Tkinter.mainloop()

if __name__=="__main__":
	HoldemGUI().startGUI()