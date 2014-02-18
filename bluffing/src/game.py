'''
Created on Jan 27, 2014

CHANGE action type in said to (numberof cards, said number)
 add human agent 


@author: rl-25lin
'''
NUM_CARD_TYPES = 10
NUM_SUITS = 2
TOTAL_CARDS = NUM_CARD_TYPES*NUM_SUITS
CARDS_PER_TURN = 2 

from util import *
from util import raiseNotDefined
import random
import agents
import Pile
import logging
# from featureExtractors import FeatureExtractor
from featureExtractors import centerMassSuggestion

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:
    
    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, index=0):
        self.index = index
        self.numWasCaughtLying = 0

    def initAgent(self):
        raiseNotDefined()
    def getAction(self, state):
        raiseNotDefined()
    def playDefense(self,state, offensePlayerIndex):
        raiseNotDefined()
    def caughtLying(self):
        self.numWasCaughtLying += 1
    def getNumWasCaughtLying(self):
        return self.numWasCaughtLying
    def getIndex(self):
        return self.index
        
    """
    Returns list of lists of cards to be played- [  [card1, card2] ,[card3] ] 
    """
    def getLegalCardNums(self,lastCardNum):
        aboveCardNum = (lastCardNum+1) % NUM_CARD_TYPES # to allow aces high and low
        if lastCardNum == 1:
            belowCardNum = NUM_CARD_TYPES
        else :
            belowCardNum = lastCardNum-1
        legalNums = [belowCardNum , lastCardNum , aboveCardNum]
        return legalNums


class GameState:
    
    
    
    def __init__(self , numPlayers):
        self.numPlayers = numPlayers
        self.playerOutOfCards = False
        self.pile = Pile.Pile(NUM_SUITS , NUM_CARD_TYPES)
        self.realLastCard = None
        self.saidLastCard = None
        self.pileSize = 0
        self.hands = [Pile.Pile(NUM_SUITS , NUM_CARD_TYPES) for j in range(numPlayers)]
        
    def deepCopy(self):
        newGameState = GameState(self.numPlayers)
        newGameState.playerOutOfCards = self.playerOutOfCards
        newGameState.realLastCard = self.realLastCard
        newGameState.saidLastCard = self.saidLastCard
        newGameState.pile = self.pile.deepcopy()
        newGameState.hands = [self.hands[j].deepcopy() for j in range(self.numPlayers)]
        newGameState.pileSize = self.pileSize
        return newGameState
    
  #  def resolveAccusation(self,defPlayerIndex , offPlayerIndex):
  #      print "resolving accusation: player %d accused player %d of lying"  % (defPlayerIndex , offPlayerIndex)
    
    def dealCards(self):
        print "dealing cards"
        deck = [i+1 for i in range(NUM_CARD_TYPES*NUM_SUITS)]
        print deck
        random.shuffle(deck)
        print deck
        i=0
        while len(deck) > 0:
                
            currNum = deck.pop()
            currCard = (currNum/NUM_CARD_TYPES , currNum%NUM_CARD_TYPES)
            self.hands[i].addCard(currCard)
            i = (i+1)%self.numPlayers
    
    
    def isWinner(self , agentIndex):
        if self.hands[agentIndex].getSize() == 0:
            return True
        else:
            return False
        
    def getRealLastCard(self): #make this return group of cards
        return self.realLastCard
    def getSaidLastCard(self): 
        return self.saidLastCard
    
    def doAction(self, play):
        real , said , agentIndex = play
        if not self.hands[agentIndex].removeCards(real):
            return False
        self.saidLastCard = (len(real) ,  said[1]) # ( amount of cards , number   )
        self.realLastCard = real[:]
        self.pile.addCards(real)
        
    def resolveAccusation(self ,nextPlayerIndex,currAgentIndex , play ):
        numCards, saidCard=self.saidLastCard
        
        lied=False
        for card in self.realLastCard:
            if card[1]!=saidCard or len(self.realLastCard) != numCards: #check that numbers are the same 
                lied=True
                break
        if lied:
            pileTakerIndex = currAgentIndex
            self.hands[currAgentIndex].addCards(self.pile.getAsList())
            self.saidLastCard = None
            self.realLastCard = None
            
        else:
            pileTakerIndex = nextPlayerIndex
            self.hands[nextPlayerIndex].addCards(self.pile.getAsList())
            self.saidLastCard = None
            self.realLastCard = None
        self.pile=Pile.Pile(NUM_SUITS , NUM_CARD_TYPES)
        
        
        
        return (lied , play[0] , pileTakerIndex)
            
        
    def __str__(self):
        printstr = ""
        playerIndex = 1
        printstr += "real last card: "+str(self.realLastCard)+ ",  said last card: "+str(self.saidLastCard)+" , pile size: "+str(self.pileSize)+"\n"
        printstr += "Current pile is \n"+str(self.pile)+"\n"
        handsList = [str(self.hands[j]) for j in range(self.numPlayers)]
        for handStr in handsList:
            printstr += "player "+str(playerIndex)+" hand is: \n"+handStr+"\n"
            playerIndex += 1
        
        return printstr
            
class Game:
    def __init__(self , numPlayers,  agentList, numGames = 1):
        self.numPlayers = numPlayers
        for agent in agentList:
            print "initializing agent", str(agent)
        self.agents = agentList
        self.numGames = numGames
        print "num games will be ", self.numGames
        self.winnerTable = [0 for i in range(numPlayers)] 
    """
    Deals cards, initializes agents at start of game. Doesn't change Q learning values (to allow them to update over multiple games)
    """
    def initGame(self):
        for agent in self.agents:
            agent.initAgent()
        self.gameState = GameState(self.numPlayers)
        self.gameState.dealCards()
            
    def getDefenseAgents(self, agentIndex):
        defenseAgentList = []
        for i in range(self.numPlayers):
            if i!= agentIndex:
                defenseAgentList.append(i)
        return defenseAgentList
          
    def runGame(self):
        i = 0
        roundNum = 1
        gameOver  = False
        while not gameOver:
            print "[runGame] - starting round ",roundNum
            for i in range(self.numPlayers):
                reward = 0
                currAgent = self.agents[i]
                
                accusers = []
                prevGameState = self.gameState.deepCopy()
                play = currAgent.getAction(self.gameState) # returns tuple (real, said , agentIndex)
                playStr = str(currAgent) + " played " + str(play)
                print playStr
                self.gameState.doAction( play) #
#                 print "gameState is ", str(self.gameState)
                defenseAgents = self.getDefenseAgents(i) # list of all other agents
                reward=len(play[0]) #amount of cards played
                for defPlayerIndex in defenseAgents:
                    if self.agents[defPlayerIndex].playDefense(self.gameState,currAgent.getIndex()):
                        accusers.append(defPlayerIndex)
                
                if len(accusers) > 0: # someone accused currAgent
                    accIndex = random.choice(accusers)
                    print str(accusers)+" shouted liar, "+str(accIndex)+ " shouted first!"    
                    lied , realCardsList , pileTakerIndex =  self.gameState.resolveAccusation(accIndex,currAgent.getIndex() , play)
                    print "Accusation was "+str(lied)+" pile taken by agent "+str(pileTakerIndex)+". Updated gamestate is:"
                    print str(self.gameState) 
                    if lied:
                        reward = -(reward+prevGameState.pile.getSize())
                        currAgent.caughtLying()
                    if self.gameState.isWinner(i):
                        gameOver = True
                        break
#                     for defPlayerIndex in defenseAgents: ## give all agents chance to update their knowledge
#                             self.agents[defPlayerIndex].updateInfo(realCardsList, pileTakerIndex)
                if self.gameState.isWinner(i):
                    gameOver = True
                    break
            roundNum += 1
            print " Is game over =  ,"+str(gameOver)+ " reward is "+ str(reward)
        
        print "game over! Winner is agent", str(self.agents[i])
        self.winnerTable[i] += 1

#                 currAgent.update(i, reward,prevGameState , play ,self.gameState)
                        
                    
                    
                    
                    
                
"""
Add ability to add ctor parameters for each bot type!
"""
def agentFactory(agentChar , agentIndex , numPlayers):
    if agentChar == 'n':
        newNaive = agents.NaivebotAgent(agentIndex , numPlayers )
        return newNaive
    if agentChar == 'b':
        newBluff = agents.BluffbotAgent(agentIndex , numPlayers)
        return newBluff
    if agentChar == 'h':
        newHuman = agents.HumanAgent(agentIndex , numPlayers)
        return newHuman
    print "Error - invalid agent type!"
    return None
    
def readCommand( args):
    numGames = int(args[1])
    agentTypes = args[2:]
    numPlayers = len(agentTypes)
    agentList =[]
    for agentCharIndex in range(len(agentTypes)):
        agentList.append(agentFactory(agentTypes[agentCharIndex], agentCharIndex,numPlayers))
    newGame = Game(numPlayers, agentList,numGames)    
    return newGame

if __name__ == '__main__':
    print "args are" , str(sys.argv)
    print "starting game"
    logger = logging.getLogger('gameLog')
    game = readCommand(sys.argv)
#     game.gameState.saidLastCard = (1 , 10)
#     print str(game.gameState)
    for i in range(game.numGames):
        game.initGame()
#         print " center mass suggestion"
#         centerMassSuggestion(game.gameState.hands[0])
        
        game.runGame()
        
        
    print "winner table is ", str(game.winnerTable)
#     bluffAgent = agents.BluffbotAgent(0,4)
#     naiveAgent = agents.NaivebotAgent(1,4)
#     legalBluffActs = game.agents[0].getLegalActions(game.gameState)
#     print "legal bluffbot Actions are:",str(legalBluffActs)
#     print" num of actions is", len(legalBluffActs)
#     
#     legalNaiveActs = naiveAgent.getLegalActions(game.gameState)
#     print "findClosestCard:", naiveAgent.findClosestCard(game.gameState)
#     print "legal naiveAgent Actions are:",str(legalNaiveActs)
#     print" num of actions is", len(legalNaiveActs)
#     print" chosen action by naivebot is ", naiveAgent.getAction(game.gameState)
#     distance , size = extractLargestGroup(game.gameState.hands[0].getAllCardFreqs(), game.gameState.saidLastCard[1])
#     print " distance, size are ", distance , size
    
    
    
    