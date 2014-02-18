# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
from game import NUM_CARD_TYPES, NUM_SUITS, TOTAL_CARDS

"Feature extractors for Pacman game states"

import util
import game
from math import atan2,cos,sin,pi
import Pile

class FeatureExtractor:  
  def getFeatures(self, state, action):    
    """
      Returns a dict from features to counts
      Usually, the count will just be 1.0 for
      indicator functions.  
    """
    util.raiseNotDefined()

class OffenseFeatureExtractor(FeatureExtractor):
    def getFeatures(self, state , action):
        feats = util.Counter()
        winValue = 100
        real , said , agentIndex = action 
        
        tempState = state.deepCopy()
        tempState.doAction(action)
        lastCardNum = tempState.getSaidLastCard()[1]
        oldHandList = state.hands[agentIndex].getAsList()
        newHand  = tempState.hands[agentIndex]
#         distance , size = extractLargestGroup(newHand.getAllCardFreqs(), state.realLastCard[1]) #  EREZ the tool
#         feats["distanceFromLG"] = (NUM_CARD_TYPES - distance+1)/NUM_CARD_TYPES
        
        feats["numberOfCardsPlayed"] = said[0]
        cm , var = centerMass(newHand)
        distance = Pile.getCardDistance(lastCardNum, cm, NUM_CARD_TYPES)
        feats["distanceFromCM"] = (NUM_CARD_TYPES - distance+1)/NUM_CARD_TYPES
        feats["var"] = 10 - var # curve fit matlab?
        if newHand.getSize()==0 and real == said: # this is the winning move
            feats["win"]= winValue
        else:
            feats["win"] = 0
#         feats["size"] = size / newHand.getSize()
        factor= cos( (pi /2) * tempState.pile.getSize()/TOTAL_CARDS) # to take into account size of deck
        if real != said:
            if said in oldHandList: #means it is a good lie
                feats["goodLie"] = pow(factor,2)
            else:
                feats["badLie"] = pow(factor,2) # 
        else:
            feats["truth"] = 1
        if tempState.isWinner(agentIndex): # we want to discourage lying if this is the winning action
            feats["goodLie"]=-2
            feats["badLie"]=-2
        # use probability table from defense player to estimate how good a lie is
        return feats
        

class DefenseFeatureExtractor(FeatureExtractor):
    def getFeatures(self, state , action):
        feats = util.Counter()
        said, said , agentIndex = action
        tempState = state.deepcopy()
        tempState.get


        tempState.doAction(action)




        oldHand = state.hands[agentIndex]
        newHand  = tempState.hands[agentIndex]
        distance , size = extractLargestGroup(newHand.getAllCardFreqs(), state.realLastCard[1]) #  EREZ the tool
        feats["distanceFromLG"] = (NUM_CARD_TYPES - distance+1)/NUM_CARD_TYPES
        feats["size"] = size / newHand.getSize()
        factor= cos( (pi /2) * tempState.getSize()/TOTAL_CARDS) # to take into account size of deck
        #if real != said:
        #    if said in oldHand: #means it is a good lie
        #        feats["goodLie"] = factor^2
        #    else:
        #        feats["badLie"] = factor^2 #
        #else:
        #    feats["truth"] = 1

        # use probability table from defense player to estimate how good a lie is

        # add feature for terminal state? this is because lies will be less successful at end of game- maybe we shouldn't try it at all
        return feats


def centerMass(hand,lastCard=None):
    sumX=0
    sumY=0
    handFreqs = hand.getAllCardFreqs()
    angles=[]
    const= 2* pi/NUM_CARD_TYPES
    for i in range(0,NUM_CARD_TYPES):
        sumX=sumX+handFreqs[i]*cos(const*i)
        sumY=sumY+handFreqs[i]*sin(const*i)
    angle=atan2(sumY,sumX)
    if angle<0:
        angle=2*pi+angle
#     card= round(angle/const)
    card= int(round(angle/const)+1)
    card= card%len(handFreqs)
    var = 0
    for i in range(1,NUM_CARD_TYPES+1):
        prob = float(handFreqs[i-1]) / hand.getSize()
#         print "i , prob , distance" ,i, prob , Pile.getCardDistance(i, card, NUM_CARD_TYPES)
        var += pow(Pile.getCardDistance(i, card, NUM_CARD_TYPES) , 2)*prob
    if not lastCard:
        return card , var# add variance
    return card , var# add variance

def centerMassSuggestion(hand,lastCard=None):
    sumX=0
    sumY=0
    angles=[]
    const= 2* pi/NUM_CARD_TYPES
    for i in range(0,NUM_CARD_TYPES):
        sumX=sumX+hand[i]*cos(const*i)
        sumY=sumY+hand[i]*sin(const*i)
    angle=atan2(sumY,sumX)
    if angle<0:
        angle=2*pi+angle
    card= round(angle/const)
    card= card%len(hand)
    if not lastCard:
        return card+1 # add variance
    return getSuggestion(lastCard,card) # add variance









def getNext( card):
    if card == NUM_CARD_TYPES:
        return 1
    return card+1

def getPrev( card):
    if card == 1:
        return NUM_CARD_TYPES
    return card-1

"""
The method gets:
    hand- 1d array of the amount of cards the player has from each card
    lastCard- the last card played
and returns the largest size of group, and its distance from lastCard

Assumptions: The group can start from lastCard +1/ last Card or lastCard -1
         A group is two sequences of neighbor cards with one space between them
"""

def getSuggestion(lastCard,index):
    dist= Pile.getCardDistance( lastCard,index, NUM_CARD_TYPES)
    if dist==0:
        return 0
    elif lastCard>index:
        if lastCard-index==dist:
            return -1
        else:
            return 1
    else:
        if index-lastCard== dist:
            return 1
        return -1




def extractLargestGroup(hand,lastCard):
    if not (0 in hand):
        return 2
    j=0       # Iteration counter
    i=lastCard-1 #start searching for group before current card
    if i==0:
        i=NUM_CARD_TYPES-1

    lastGroupIndex=[0,0]
    currGroupIndex= [0,0]

    currGroupSize=0
    lastGroupSize=0
    maxGroupSize=0
    distMaxGroup=NUM_CARD_TYPES
    currSuggestion=0


    while j<=NUM_CARD_TYPES+2:
        while hand[i-1]==0 and j<=NUM_CARD_TYPES+2: #find the first card which is in the hand
            i=getNext(i)
            j=j+1
        if j>NUM_CARD_TYPES+2:
                break

        lastGroupIndex= currGroupIndex[:]
        lastGroupSize=currGroupSize

        currGroupSize=0
        currGroupIndex[0]=i

        while hand[getNext(i)-1]>0 and j<=NUM_CARD_TYPES+2:
            currGroupSize=currGroupSize+hand[i-1]
            i=getNext(i)
            j=j+1
        if j<=NUM_CARD_TYPES+2:
            currGroupSize=currGroupSize+hand[i-1]
            currGroupIndex[1]=i
        else:
            currGroupIndex[1]=getPrev(i)

        size=currGroupSize

        if (not (lastGroupIndex[0]==0)) and Pile.getCardDistance( lastGroupIndex[1] , currGroupIndex[0], NUM_CARD_TYPES)==2:
            startIndex=lastGroupIndex[0]
            size=size+lastGroupSize
        else:
            startIndex=currGroupIndex[0]

        groupIndexes=[startIndex, currGroupIndex[1]]

        if size>=maxGroupSize:
            dist=Pile.getCardDistance(lastCard,groupIndexes[0],NUM_CARD_TYPES)
            dist2=Pile.getCardDistance(lastCard,groupIndexes[1],NUM_CARD_TYPES)
            if dist <= dist2:
                index=groupIndexes[0]
            else:
                index=groupIndexes[1]
                dist=dist2

            if size>maxGroupSize or distMaxGroup>dist:
                distMaxGroup=dist
                maxGroupSize=size
                currSuggestion=getSuggestion(lastCard,index)
        i=getNext(i)
        j=j+1
    return currSuggestion
