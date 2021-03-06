'''
Created on Jan 28, 2014

@author: rl-25lin
'''

import game
import util
import random
import re
from game import CARDS_PER_TURN, NUM_CARD_TYPES , NUM_SUITS
from collections import deque
from math import floor
import Pile
class BluffbotAgent(game.Agent):
    
    def __init__(self,index,numPlayers , epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0):
        
        self.seenPile = Pile.Pile(NUM_SUITS , NUM_CARD_TYPES)
        
        self.index = index
        self.hands = [ Pile.Pile(NUM_SUITS , NUM_CARD_TYPES) for i in range(numPlayers)] # to also hold estimates of opponents hands
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.numTraining = numTraining
        self.wDict = util.Counter()
        self.worstCards = []
        self.canLie = False
        self.numPlayers=numPlayers


    def initDef(self):
        self.lieFactor=[0.2 for i in range(0,self.numPlayers)]  #######new
        sizeHand=self.hands[self.index].getSize()
        numCards= NUM_CARD_TYPES*NUM_SUITS
        self.rivalPiles=[[Pile.Pile(1 , NUM_CARD_TYPES) for j in range(0,NUM_SUITS)] for i in range(0,self.numPlayers)]
        self.rivalPiles[self.index]=None
        hand=self.hands[i].getAllCardFreqs()
        othersHave=[NUM_SUITS-hand for i in range(0,NUM_CARD_TYPES)]

        for i in range(0, self.numPlayers):
            for j in range(0,NUM_SUITS): # Gaining the amount of a given type
                self.calcInitProb(numCards,j,sizeHand,othersHave,i)



    # Calculating the propability having a card in the given amount
    def calcInitProb(self,numCards,amountOfCard,sizeHand,othersHave,index):
        for k in range(0,NUM_CARD_TYPES):
            if (self.numPlayers==2):
                has=floor((numCards-othersHave[k])/amountOfCard)
                self.rivalPiles[index][amountOfCard].addCards([k for z in range(0,has)
                continue
            if amountOfCard<=othersHave[k]:
                prop=choose(othersHave[k],amountOfCard)
                prop=prop*choose(numCards-othersHave[k],sizeHand-amountOfCard)
                prop=prop/choose(numCards,sizeHand)
            else:
                prop=0
            self.rivalPiles[index][amountOfCard].addCard(k,True,prop)

#choose of a over b
def choose(self, a,b):
    sum=1
    if a<b:
        return 0
    if a==b:
        return sum
    for m in range(b+1,a+1):
        sum=sum*m
    return m

""""
    The starategy is to let every rival player gain the possibility of having the cards the players doesnt have
"""
    def updateDefense(self,action):
        numCards,said,agentNum= action
        if (agentNum!=self.index):
            self.rivalPiles[agentNum].removeCards(said,numCards, True, self.lieFactor[agentNum])

    def updateDefGetPile(self,pile,agentNum):
        if agentNum==self.index:

        #else:




    def __str__(self):
        printstr = "BluffbotAgent, #"+str(self.index)+"\n"
        return printstr
#     def caughtLying(self):
#         self.numWasCaughtLying += 1
    def getNumWasCaughtLying(self):
        return self.numWasCaughtLying
    def getIndex(self):
        return self.index
    """
    Orders the cards according to our priority of getting rid of them (worst cards are first). Cards are ordered according
    to the direction we want to go relative to current last card.0 means we prefer to go down from the current last card, 
    meaning we want to get rid of our high cards, 1 vice versa
    
    POSSIBLE OPTIMIZATION: don't only order by rank but also by size num suits available (2 tens shouldn't be lied with before 9,8 for example)
    """
    def orderWorstCards(self,state, prefDirection): 
        self.worstCards = []
        lastCardNum = state.getSaidLastCard()[1]
        pivot = (lastCardNum+ (NUM_CARD_TYPES/2))% NUM_CARD_TYPES +1
        print "pivot is ", pivot
        
        legalNums = self.getLegalCardNums(lastCardNum)
        print"legal nums are",legalNums
            
        lieNumbers = deque([num+1 for num in range(NUM_CARD_TYPES) if (num+1) not in legalNums])
        for i in range(len(lieNumbers)-1):
            if (abs(lieNumbers[i+1]-lieNumbers[i])%NUM_CARD_TYPES) != 1:
                break
        
        midCard = lieNumbers[i]
        print "midCard , i are ",midCard,i
        print "[orderWorstCards] lie numbers are", lieNumbers
        if prefDirection == 0:
            lieNumbers = deque(reversed(lieNumbers))
            legalNums = reversed(legalNums)
        while lieNumbers[0] != pivot:
            lieNumbers.rotate(1)
        print "[orderWorstCards] rotated lie numbers are", lieNumbers
        newMidIndex = list(lieNumbers).index(midCard)
        lowerHalf = list(lieNumbers)[:newMidIndex+prefDirection] # correction to index if we prefer up direction
        upperHalf = reversed(list(lieNumbers)[newMidIndex+prefDirection:])
        orderedLieNums = lowerHalf+list(upperHalf)+list(legalNums)
        print "[orderWorstCards] orderedLieNums are", orderedLieNums
        
        self.canLie = False
        for cardNum in orderedLieNums:
            print" card Num is ",cardNum
            cardsList = state.hands[self.index].getAllOfCardsNum(cardNum)
            if cardsList != None:
                self.worstCards += cardsList
                if cardNum not in legalNums: # we do have a card 
                    self.canLie = True
                    
         
         
        print "[orderWorstCards] worstCardList is", self.worstCards    
        
    """
    Returns False if agent thinks target has lied, True if agent thinks he told the truth
    """
    def playDefense(self,state, offensePlayerIndex):


        return False
   
    
    def getLegalActions(self, state):
        legalActions = []
        self.orderWorstCards(state , 0)
        currHand = state.hands[self.index]
        #terminal state, no legal actions
        if currHand.getSize() == 0:
            return None 
        # add beginning state!!!
        
        lastCardNum = state.getSaidLastCard()[1]

        legalNums = self.getLegalCardNums(lastCardNum)
        
        for i in range(min(currHand.getSize(),CARDS_PER_TURN) ): # so we don't attempt to play more than we have
            playSize = i+1
            for num in legalNums: # find moves for each legal num- if last card is 6, legal nums are 5 6 7
                realBL = []
                saidBL = []
                realGL = []
                saidGL = []
                realT = []
                saidT = []
                cards = currHand.getChoice(num , playSize)
                if cards != None:
                    for cardIndex in range(len(cards)):
                        realT.append(cards[cardIndex])
                        saidT.append(cards[cardIndex])
                        if self.canLie: # True if we have cards that aren't in the legal cards group, meaning we can lie with them >:)
                            realGL.append(self.worstCards[cardIndex])
                            saidGL.append(cards[cardIndex])
                    legalActions.append( (realT , saidT ,self.index )  )
                    if self.canLie:
                        legalActions.append((realGL , (len(realGL),num) , self.index ) )
                else:
                    for cardIndex in range(playSize):
                        realBL.append(self.worstCards[cardIndex])
                        saidBL.append((1,num))
                        
                    legalActions.append((realBL , (len(realBL),num) , self.index))
                    
                    
            #################
            
            
        return legalActions
                           
        
    def getValue(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "terminal state"
        if not self.getLegalActions(state): 
            return 0.0
        poliVal = self.getPoliVal(state)
        return poliVal[1] # the value

    def getPolicy(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        if not self.getLegalActions(state):
            return None
        
        poliVal = self.getPoliVal(state)
        return poliVal[0] # the action
    
    def getPoliVal(self,state):
        maxVal=-float('inf')
        actionsList=[]
        for nextAction in self.getLegalActions(state):
            if maxVal<self.getQValue(state,nextAction):
                maxVal=self.getQValue(state,nextAction)
                actionsList=[nextAction]
            if abs(maxVal - self.getQValue(state,nextAction)) < 0.01:
                actionsList.append(nextAction)
        return random.choice(actionsList), maxVal
  
    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        return self.getPolicy(state)
    
    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        featureDict = self.featExtractor.getFeatures(state,action)
        sigma = 0
        for feat in featureDict.keys():
            sigma += featureDict[feat]*self.wDict[feat]
        return sigma
    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        maxNextQval = 0.0
        oldQ = self.getQValue(state, action)
        ### finding max Q value on succesors
        if not not self.getLegalActions(nextState):
            nextActionQvals= [self.getQValue(nextState, nextAction) for nextAction in self.getLegalActions(nextState)]
            maxNextQval=max(nextActionQvals)
        correction =  (reward+self.discount*maxNextQval-oldQ)
        
        featureDict = self.featExtractor.getFeatures(state,action)
        for feat in featureDict.keys():
            self.wDict[feat] += self.alpha*correction*featureDict[feat] 

class NaivebotAgent(game.Agent):
    
    def __init__(self,index,numPlayers , naiveFactor = 0.5,numTraining=0):
        
        self.index = index
        self.naiveFactor = naiveFactor
        self.hands = [ Pile.Pile(NUM_SUITS , NUM_CARD_TYPES) for i in range(numPlayers)] # to also hold estimates of opponents hands
        self.numTraining = numTraining
        self.initAgent()
    
    def initAgent(self):
        self.numWasCaughtLying = 0
        self.canLie = False
    def getNumWasCaughtLying(self):
        return self.numWasCaughtLying
#     def getIndex(self):
#         return self.index
    def __str__(self):
        printstr = "NaivebotAgent, #"+str(self.index)+"\n"
        return printstr
    def findClosestCard(self,state): ### fix min prob!
        currHand = state.hands[self.index]
        lastCardNum = state.getSaidLastCard()[1]
        cardFreqs = currHand.getAllCardFreqs()
        dList = [(num+1 ,Pile.getCardDistance(num+1 , lastCardNum, NUM_CARD_TYPES)) for num in range(len(cardFreqs)) if cardFreqs[num]>0  ]
        print "findClosestCard: " ,dList
        minCard = dList[0]
        for pair in dList:
            if pair[1] < minCard[1]:
                minCard = pair
        return minCard[0]
                
        
    def getAction(self, state):
        """
        Naivebot first tries to play most cards he can (truthfully if possible), tiebreaker between same length actions is according to 
        which action gets him closer to his closest card
        """
        bestActs = []
        legalActs = self.getLegalActions(state)
        if state.getSaidLastCard() == None:
            return random.choice(legalActs)
        
        closestCard = self.findClosestCard(state)
        minD = NUM_CARD_TYPES
        actSizeList = [len(act[0]) for act in legalActs]
        maxSize = max(actSizeList)
        biggestActs = [act for act in legalActs if len(act[0]) == maxSize]
            
        
        for act in biggestActs:
#             print "in GetAction, action is", act
#             print "act[1][0] is ",act[1][0]
            newD = Pile.getCardDistance(closestCard, act[1][1],NUM_CARD_TYPES) #distance between said card and closest card
#             print "dist is ",newD
            if newD == minD:
                bestActs.append(act)
            if newD < minD:
                bestActs = []
                
                minD = newD
                bestActs.append(act)
            
        return random.choice(bestActs)
                
            
            
    def playDefense(self,state, offensePlayerIndex):
        if state.isWinner(offensePlayerIndex):
            return True
        if util.flipCoin(self.naiveFactor):
            return True
        else:
            return False

    def getLegalActions(self, state):
        legalTrueActions = []
        legalFalseActions = []
        currHand = state.hands[self.index]
        handList = state.hands[self.index].getAsList()
        #terminal state, no legal actions
        if currHand.getSize() == 0:
            return None 
        # add beginning state!!!
        if state.getSaidLastCard() == None:
            for card in handList:
                legalTrueActions.append(([card] , (1 , card[1]) , self.index))
            return legalTrueActions
        lastCardNum = state.getSaidLastCard()[1]

        legalNums = self.getLegalCardNums(lastCardNum)
        
        for i in range(min(currHand.getSize(),CARDS_PER_TURN) ): # so we don't attempt to play more than we have
            playSize = i+1
            for num in legalNums: # find true moves
                trueMove = []
                badLieMove =[]
                real =[]
                said=[]
                cards = currHand.getChoice(num , playSize)
                if cards != None:
                    for cardIndex in range(len(cards)):
                        real.append(cards[cardIndex])
                        said.append(cards[cardIndex])
                        trueMove.append((cards[cardIndex] , cards[cardIndex], self.index))
                    legalTrueActions.append( (real , (len(real) , num) , self.index)  )
                else:
                    tmp = handList[:]
                    for cardIndex in range(playSize):
                        randomCard = random.choice(tmp)
                        tmp.remove(randomCard)
                        real.append(randomCard)
                        said.append((1,num))
                        badLieMove.append(  (randomCard, (1,num),self.index)  )
                    legalFalseActions.append( (real,( len(real) ,num ) , self.index ))
                    
                    
            #################
            
        if legalTrueActions != [] : #############EREZ: try not legalTrueActions
            return legalTrueActions
        else:
            return legalFalseActions
class HumanAgent(game.Agent):
    def __init__(self,index,numPlayers ):
        self.numPlayers = numPlayers
        self.index = index
        self.initAgent()
        
    def initAgent(self):
        self.numWasCaughtLying = 0
    def convertStrToTuple(self , str):
        trimStr = str.replace(' ' ,'')
        trimStr = trimStr.strip('()')
        trimStrSplit = trimStr.split(',')
        print trimStrSplit
        return (int(trimStr[0]),int(trimStr[1]))
    """
    Gets move from human input. No validity checking yet
    """    
    def getAction(self, state):
        realMove = []
        hand = state.hands[self.getIndex()]
        print "Your hand is \n"+str(hand)
        print "Last cards are "+ str(state.getSaidLastCard())
        print "Enter card numbers you wish to play"
        inputStr = raw_input("Enter card number you wish to play and amount (in the format amount,cardNum , 'f' when finished")
        while(inputStr != 'f'):
            
            inputSplit = inputStr.split(',')
            amount = int(inputSplit[0])
            cardNum = int(inputSplit[1])
            realChoice = hand.getChoice(cardNum , amount)
            if realChoice != None:
                realMove +=(realChoice)
            inputStr = raw_input("Enter card number you wish to play and amount (in the format amount,cardNum , 'f' when finished")
        inputStr = raw_input("And what will you say these cards are?")
        saidCards = (len(realChoice), int(inputStr))
        action = ( realMove , saidCards,self.getIndex()   )
        print action
        return action

    def playDefense(self,state, offensePlayerIndex):
        print "What will you play? Your hand is \n"+str(state.hands[self.getIndex()])
        print "Last cards are "+ str(state.getSaidLastCard())+", played by opponent "+str((self.getIndex()-1)%self.numPlayers)
        rawDefense = raw_input("Play defense: enter t if you think the move is true, f if you think opponent lied")
        if rawDefense == 't':
            return False # playDefense returns false if we think move is true
        if rawDefense == 'f':
            return True
        
        return True
    def caughtLying(self):
        self.numWasCaughtLying += 1
    def getNumWasCaughtLying(self):
        return self.numWasCaughtLying
    def getIndex(self):
        return self.index