__author__ = 'Erez'
"""
The method gets:
	hand- 1d array of the amount of cards the player has from each card
	lastCard- the last card played
and returns the largest size of group, and its distance from lastCard

Assumptions: The group can start from lastCard +1/ last Card or lastCard -1
	     A group is two sequences of neighbor cards with one space between them
"""


def getDist(i, j, numCards):
    dist = abs(i - j)
    distAlt = abs(i + numCards - j)
    distAltSec = abs(i - (numCards + j))
    return min(dist, distAlt, distAltSec)


def extractLargestGroup(self, hand, lastCard):
    j = 0       # Iteration counter
    i = lastCard - 1 #start searching for group before current card
    if lastCard==0:
        i = NUM_CARD_TYPES - 1
    currGroupSize = 0
    lastGroupSize = 0
    maxGroupSize = 0
    distMaxGroup = NUM_CARD_TYPES
    startGroupInd = 0
    lastGroupInd=0
    currGroupInd = 0
    numBrakes = 0

    while j < NUM_CARD_TYPES + 2:

        #find the first card which is in the hand
        numBrakes=0
        while hand[i] == 0 and j < NUM_CARD_TYPES + 2:
            i = i + 1
            if i == NUM_CARD_TYPES:
                i = 0
            j = j + 1
            numBrakes = numBrakes + 1

        if j == NUM_CARD_TYPES + 2:
            break

        lastGroupInd= currGroupInd
        currGroupInd = i
        lastGroupSize = currGroupSize
        currGroupSize = 0

        dist = getDist(i, lastCard, NUM_CARD_TYPES)
        while hand[i] > 0 and j < NUM_CARD_TYPES+2:
            currGroupSize = currGroupSize + hand[i]
            i = i + 1
            if (i == NUM_CARD_TYPES):
                i = 0
            j = j + 1
        distLast = getDist(i, lastCard, NUM_CARD_TYPES)
        if dist > distLast:
            dist = distLast
            currGroupInd = i

        currInd=currGroupInd
        newGroupSize = currGroupSize

        if numBrakes == 1: # A group is defined by one brake in it
            newGroupSize = newGroupSize + lastGroupSize
            currInd=min(currGroupInd,lastGroupInd)

        if newGroupSize >= maxGroupSize:
            maxGroupSize = newGroupSize
            distMaxGroup = dist
            startGroupInd = currGroupInd

        elif lastGroupSize + currGroupSize == maxGroupSize and dist < distMaxGroup:
            distMaxGroup = dist
            startGroupInd = currGroupInd

    return distMaxGroup, maxGroupSize
