#from final_project.bluffing.src.game import NUM_CARD_TYPE
#import Pile
#__author__ = 'Erez'
#"""
#The method gets:
#	hand- 1d array of the amount of cards the player has from each card
#	lastCard- the last card played
#and returns the largest size of group, and its distance from lastCard
#
#Assumptions: The group can start from lastCard +1/ last Card or lastCard -1
#	     A group is two sequences of neighbor cards with one space between them
#"""
#
## assumptions:
## hand= cardFreqs
## lastCard = is between 1 to NUM_CARD_TYPE
#
##output 2- no matter
##       0- stay
##       1- up
##       -1- down
#
#
#
#def getNext( card):
#    if card == NUM_CARD_TYPE:
#        return 1
#    return card+1
#
#def getPrev( card):
#    if card == 1:
#        return NUM_CARD_TYPE
#    return card-1
#

def getSuggestion(lastCard,index,cardDist):
    dist= Pile.getCardDistance( lastCard,index, NUM_CARD_TYPE)
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



#
#def extractLargestGroup(hand,lastCard):
#    if not (0 in hand):
#        return 2
#    j=0       # Iteration counter
#    i=lastCard-1 #start searching for group before current card
#    if i==0:
#        i=NUM_CARD_TYPE-1
#
#    lastGroupIndex=[0,0]
#    currGroupIndex= [0,0]
#
#    currGroupSize=0
#    lastGroupSize=0
#    maxGroupSize=0
#    distMaxGroup=NUM_CARD_TYPE
#    currSuggestion=0
#
#
#    while j<=NUM_CARD_TYPE+2:
#        while hand[i-1]==0 and j<=NUM_CARD_TYPE+2: #find the first card which is in the hand
#            i=getNext(i)
#            j=j+1
#        if j>NUM_CARD_TYPE+2:
#                break
#
#        lastGroupIndex= currGroupIndex[:]
#        lastGroupSize=currGroupSize
#
#        currGroupSize=0
#        currGroupIndex[0]=i
#
#        while hand[getNext(i)-1]>0 and j<=NUM_CARD_TYPE+2:
#            currGroupSize=currGroupSize+hand[i-1]
#            i=getNext(i)
#            j=j+1
#        if j<=NUM_CARD_TYPE+2:
#            currGroupSize=currGroupSize+hand[i-1]
#            currGroupIndex[1]=i
#        else:
#            currGroupIndex[1]=getPrev(i)
#
#        size=currGroupSize
#
#        if (not (lastGroupIndex[0]==0)) and Pile.getCardDistance( lastGroupIndex[1] , currGroupIndex[0], NUM_CARD_TYPE)==2:
#            startIndex=lastGroupIndex[0]
#            size=size+lastGroupSize
#        else:
#            startIndex=currGroupIndex[0]
#
#        groupIndexes=[startIndex, currGroupIndex[1]]
#
#        if size>=maxGroupSize:
#            dist=Pile.getCardDistance(lastCard,groupIndexes[0],NUM_CARD_TYPE)
#            dist2=Pile.getCardDistance(lastCard,groupIndexes[1],NUM_CARD_TYPE)
#            if dist <= dist2:
#                index=groupIndexes[0]
#            else:
#                index=groupIndexes[1]
#                dist=dist2
#
#            if size>maxGroupSize or distMaxGroup>dist:
#                distMaxGroup=dist
#                maxGroupSize=size
#                currSuggestion=getSuggestion(lastCard,index)
#        i=getNext(i)
#        j=j+1
#    return currSuggestion
import math
def centerMassSuggestion(hand,lastCard=None):
    sumX=0
    sumY=0
    angles=[]
    const= 2* math.pi/len(hand)
    for i in range(0,len(hand)):
        sumX=sumX+hand[i]*math.cos(const*i)
        sumY=sumY+hand[i]*math.sin(const*i)
    angle=math.atan2(sumY,sumX)
    if angle<0:
        angle=2*math.pi+angle
    card= round(angle/const)
    card= card%len(hand)
    if not lastCard:
        return card+1
    return getSuggestion(lastCard,card,len(hand))

if __name__ == '__main__':
    print "starting game"
    hand=[0,2,3,1,5]
    print hand
    out= centerMassSuggestion(hand)
    print out
# If you want to run only this- define NUM_CARD_TYPE as global and loose the first import from game
#if __name__ == '__main__':
#    print "starting game"
#    hand=[0,5,0,0,0,0,5,0,5,0]
#    out= extractLargestGroup(hand,1)
#    print out