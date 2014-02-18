'''
Created on Feb 3, 2014

@author: rl-25lin
'''

class Pile:
    def __init__(self, numSuits , numCardTypes , pileArray = None ):
        self.pileSize = 0
        self.numSuits = numSuits
        self.numCardTypes = numCardTypes
        if pileArray != None:
            self.pileArr = [[pileArray[j][i] for i in range(numCardTypes)] for j in range(numSuits)]
        else:
            self.pileArr = [[ 0 for i in range(numCardTypes)] for j in range(numSuits)]
        self.cardFreqs = self.getAllCardFreqs()
         
    def getAllCardFreqs(self):
        cardFreqs = []
        for i in range(self.numCardTypes):
            sumCards = 0
            for j in range(self.numSuits):
                sumCards += self.pileArr[j][i]
            cardFreqs.append(sumCards)
        return cardFreqs
           
    def getCardFreqs(self , cardNum):
        return self.cardFreqs[cardNum-1]
    def hasCard(self , card):
        return  self.pileArr[card[0]-1][card[1]-1]
    def getAllOfCardsNum(self , cardNum):
        if self.cardFreqs[cardNum-1] > 0:
            move = []
            j = 1
            while j <= self.numSuits:
                card = (j , cardNum)
#                 print"[getAllOfCardsNum] checking card", card
                if self.hasCard( card ):
                    move.append(  card  )
                j += 1
            return move
        else:
            return None
        
    def getChoice(self,cardNum , numberOfCards):
        """
        returns list containing numberOfCards cards of type cardNum. If doesn't exist, return None
        If more cards exist than needed, returns one possible group (if we have 3 aces, and want 2, 
        we get a single combination of 2 aces)
        """
        if self.cardFreqs[cardNum-1] >= numberOfCards :
            move = []
            j = 1
            size = 0
            while size < numberOfCards:
                card = (j , cardNum)
                if self.hasCard( card ):
                    size += 1
                    move.append(  card  )
                j += 1
            return move
        else:
            return None
            
    def addCard(self, card, is1D=None,factor=None):  # check that card to be added doesn't already  exist in hand
        if (is1D)(not is1D and not  self.pileArr[card[0]-1][card[1]-1]):
            plus=1
            if (factor):
                plus=factor
            self.pileArr[card[0]-1][card[1]-1] =self.pileArr[card[0]-1][card[1]-1]+ plus
            self.pileSize += 1
            self.cardFreqs[card[1]-1] += 1

    def addCards(self, cardList, is1D=None,factor=None):
        if cardList != None:
            for card in cardList:
                self.addCard(card,is1D,None)
                
    def removeCard(self, card,is1D,factor):
        if ((is1D)or (not is1D and self.pileArr[card[0]-1][card[1]-1])): # check that card to be removed exists
            minus=1
            if is1D:
                minus=factor
            self.pileArr[card[0]-1][card[1]-1] = self.pileArr[card[0]-1][card[1]-1]-minus
            self.pileSize -= 1
            self.cardFreqs[card[1]-1] -= 1
            return True
        return False


    # maybe we would want to use that to decrease floating point num in defense mode
    def removeCards(self , cardList,numToDecrease=None, is1D=None, factor=None):
        for card in cardList:
            if (not is1D and not self.removeCard(card,is1D,factor)):
                return False
        return True

    def getSize(self):
        return self.pileSize
    
    def getAsList(self):
        cardsList = []
        for i in range (self.numCardTypes):
            cardNum = i+1
            currCards = self.getAllOfCardsNum(cardNum)
            if currCards!= None:
                cardsList += currCards 
        return cardsList
            
    def deepcopy(self):
        newPile = Pile(self.numSuits , self.numCardTypes, self.pileArr)
        newPile.pileSize = self.pileSize
        newPile.cardFreqs = self.cardFreqs[:]
        return newPile
    def __str__(self):
        headstr = ""
        
        for i in range(self.numCardTypes):
            headstr += (str(i+1)+" | ")
        headstr += "\n"
        for j in range(self.numSuits):
            rowstr = ""
            for i in range(self.numCardTypes):
                rowstr += str(self.pileArr[j][i])+" "*len(str(i+1))+"| "
            headstr += rowstr+"\n"
        headstr += str(self.cardFreqs)+"\n"
        return headstr    


def getCardDistance( card1 , card2, numCards):
    card1Num = card1
    card2Num = card2
    smallCard = min(card1Num, card2Num)
    bigCard = max(card1Num, card2Num)
    return min(abs(smallCard-bigCard) , (smallCard-bigCard)%numCards)
    



