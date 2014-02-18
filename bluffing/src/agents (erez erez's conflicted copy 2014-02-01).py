
'''
Created on Jan 28, 2014

@author: rl-25lin
'''
from final_project.bluffing.src.game import NUM_CARD_TYPES
import game
import util
class BluffbotAgent(game.Agent):
    
    def __init__(self,index,numPlayers):
        
        self.seenPile = game.Pile()
        self.numWasCaughtLying = 0
        self.index = index
        self.hands = [ game.Pile() for i in range(numPlayers)] # to also hold estimates of opponents hands
    
    def getNumWasCaughtLying(self):
        return self.numWasCaughtLying
    def getIndex(self):
        return self.index
    def playOffense(self, state):
        return (1,1)
    """
    Returns False if agent thinks target has lied, True if agent thinks he told the truth
    """
    def playDefense(self,state, offensePlayerIndex):
        return False


    def extractLargestGroup(self,hand,lastCard):
        j=0       # Iteration counter
        i=lastCard-1 #start searching for group before current card
        if i==0:
            i=NUM_CARD_TYPES-1
        currGroupSize=0
        lastGroupSize=0
        maxGroupSize=0
        distMaxGroup=0
        while j<NUM_CARD_TYPES+2:
            while hand[i]==0 and j<NUM_CARD_TYPES+2: #find the first card which is in the hand
                i=i+1
                if i==NUM_CARD_TYPES:
                    i=0
                j=j+1
            if j==NUM_CARD_TYPES+2:
                break

            lastGroupSize=currGroupSize
            currGroupSize=0
            dist= abs(i-lastCard)
            while hand[i]>0 and j<NUM_CARD_TYPES:
                currGroupSize=currGroupSize+1
                i=i+1
                if (i>=NUM_CARD_TYPES):
                    i=1
                j=j+1
            distLast=abs(i-lastCard)
            if dist>distLast:
                dist=distLast
            if lastGroupSize+currGroupSize>maxGroupSize:
                maxGroupSize=lastGroupSize+currGroupSize
                distMaxGroup=dist
            elif lastGroupSize+currGroupSize==maxGroupSize and dist<distMaxGroup:
                distMaxGroup=dist
        return distMaxGroup, maxGroupSize
