import random
import time

# Deck class. Contains list of element representing cards.
class Deck:
    def __init__(self,n):
        self.deck=[2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6,6, 7,7,7,7, 8,8,8,8, 9,9,9,9, 10,10,10,10,
        'J','J','J','J', 'Q','Q','Q','Q', 'K','K','K','K', 'A','A','A','A']
        if n>1:
            for i in range(n-1):
                self.deck.extend(self.deck)

    def getDeck(self):
        return self.deck

# Bank class. Stores both dealer and player's money 
class Bank:
    def __init__(self,dealerMoney,playerMoney,bet):
        self.dealerMoney=dealerMoney
        self.playerMoney=playerMoney
        self.bet=bet

    def getDealerMoney(self):
        return self.dealerMoney

    def getPlayerMoney(self):
        return self.playerMoney

    def setDealerMoney(self,money):
        self.dealerMoney=money

    def setPlayerMoney(self,money):
        self.playerMoney=money

    def setBet(self,bet):
        self.bet=bet

# Dealer class. Handles dealing procedures, calculations, and decisions
class Dealer:
    def __init__(self,deck):
        self.deck=deck.getDeck()   # input all cards to dealer, line 13

    def shuffleDeck(self):
        random.shuffle(self.deck)

    def initialDeal(self):     # give 2 cards to each player and dealer, then output on screen, hide the second card of dealer
        self.playerHand=[]
        self.dealerHand=[]
        self.playerHand.append(self.deck.pop())   #\
        self.playerHand.append(self.deck.pop())   # \ line 41
        self.dealerHand.append(self.deck.pop())   # /
        self.bottomCard=self.deck.pop()           #/
        self.dealerHand.append('?')
        self.displayCards()    # line 119

    def getDealerHand(self):
        return self.dealerHand

    def getPlayerHand(self):
        return self.playerHand

    def playerHit(self):   # player hits 1 card
        self.playerHand.append(self.deck.pop())
        print('Player hits...')
        time.sleep(1)
        self.displayCards()   # line 119

    def isBlackjack(self,hand):   # determine if someone has blackjack
        self.dealerHand.remove('?')
        self.dealerHand.append(self.bottomCard)
        if 'A' in hand and ((10 in hand) or ('J' in hand) or ('Q' in hand) or ('K' in hand)):
            self.dealerHand.pop()
            self.dealerHand.append('?')
            return True
        else:
            self.dealerHand.pop()
            self.dealerHand.append('?')
            return False
            
    def flipBottomCard(self):   # dealer gets second card
        self.dealerHand.remove('?')
        self.dealerHand.append(self.bottomCard)
        print('Dealer flips bottom card...')
        time.sleep(1)
        self.displayCards()   # after getting second card, dealer reveals all cards again, line 119

    def dealerHit(self):   # dealer hits 1 card
        self.dealerHand.append(self.deck.pop())
        print('Dealer hit...')
        time.sleep(1)
        self.displayCards()   # line 119

    def calculatePoints(self,hand):   # calculate points on hand
        outcomes=[0,0]
        for i in hand:
            if i=='J' or i=='Q' or i=='K':
                outcomes[0]+=10
                outcomes[1]+=10
            elif i=='A':      # A has 2 choices of points
                outcomes[0]+=1
                outcomes[1]+=11
            else:
                outcomes[0]+=i
                outcomes[1]+=i
        return outcomes         # output is player's point, 1 output if there's no A, 2 if there's A

    def bustOrNot(self,outcomes):   # check if total point is over 21
        if outcomes[0]> 21 and outcomes[1]>21:
            return False
        else:
            return True

    def isUnderSeventeen(self,outcomes):   # rule: if the dealer has less than 17 pts, he has to hit another card
        if outcomes[0] < 17 and outcomes[1] < 17:
            return True
        else:
            return False

    def displayCards(self):   # output the cards on screen
        print('\nDealer Hand: ',end='')
        for i in self.dealerHand:   # line 51-53
            print('[',i,'] ',end='')
        print('\n\nPlayer Hand: ',end='')
        for k in self.playerHand:   # line 49-50
            print('[',k,'] ',end='')
        print('\n')
        
    def checkForBlackjack(self):
        blackJack='none'
        if dealer.isBlackjack(dealer.dealerHand) and dealer.isBlackjack(dealer.playerHand):   # line 68
            blackJack='tie'
            print('Both Dealer and Player have Blackjack')
        elif dealer.isBlackjack(dealer.dealerHand):
            blackJack='dealer'
            self.flipBottomCard()   # line 80
            print('Dealer has Blackjack')
        elif dealer.isBlackjack(dealer.playerHand):
            blackJack='player'
            print('Player has Blackjack')
        return blackJack

    def optimalHand(self,outcomes):  # analyzes 2 different kinds of points (if there's A)
        if outcomes[0]<=21 and outcomes[1]<=21:
            return outcomes[1]
        elif outcomes[0]<=21 and outcomes[1]>21:
            return outcomes[0]
        else:
            return

    def payout(self,winner,bank):   # announce the winner + money
        if winner=='dealer':
            bank.dealerMoney+=bank.bet
            bank.playerMoney-=bank.bet
            print('You LOST $',bank.bet)
        elif winner=='player':
            bank.dealerMoney-=bank.bet
            bank.playerMoney+=bank.bet
            print('You WON $',bank.bet)
        elif winner=='tie':
            print("It's a TIE!")

    def decideWinner(self, dealerPoints, playerPoints):   # compares points of dealer and player, higher one will win
        if dealerPoints > playerPoints:
            return "dealer"
        elif dealerPoints < playerPoints:
            return "player"
        else:
            return "tie"

# Support Functions:
def isInt(s):    # check if integer or not
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def getNumOfDecks():
    while True:
        numOfDecks=input('Dealer: How many decks do you want to play with? (1-8): ')
        if isInt(numOfDecks) and 1<=int(numOfDecks)<=8:
            return int(numOfDecks)
    
def placeBet(bank):   # ask for bet each game, update to Dealer class
    chipCount(bank)   # line 203
    invalid=True
    while invalid:
        bet=input('Dealer: Please place your bet ($5 increment): ')
        if not isInt(bet):
            print('Dealer: The bet needs to be an integer!')
        elif int(bet)<=0:
            print('Dealer: The bet needs to be more than $0!')
        elif int(bet)>bank.getPlayerMoney():
            print('Dealer: You can only bet how much you have!')
        elif int(bet)>bank.getDealerMoney():
            print('Dealer: You cannot bet more than how much the dealer has left!')
        elif int(bet)%5!=0:
            print('Dealer: The bet needs to be a $5 increment!')
        else:
            bank.setBet(int(bet))
            invalid=False

def chipCount(bank):     # check money
    print('Bank: Dealer has $'+str(bank.getDealerMoney())+'. Player has $'+str(bank.getPlayerMoney()))

def ifContinue():   # ask if player wants to play more
    while True:
        userContinue=input('Dealer: Do you want to continue (Y/N)?: ')
        if userContinue=='y' or userContinue=='Y':
            return True
        elif userContinue=='n' or userContinue=='N':
            return False

def playerOptions(bank,dealer,playerOutcomes):     # return player's point atm, gives option to player each turn
    print('Dealer: You have',dealer.optimalHand(playerOutcomes))    # tells points, line 142
    while True:
        option=input('Options: 1->Hit, 2->Stay, 3->Chip Count: ')
        if option=='1':
            return option
        elif option=='2':
            return option
        elif option=='3':
            chipCount(bank)

def ifBroke(bank):   # check if someone's broke
    if bank.getDealerMoney()==0:   # line 23
        print('Dealer broke!')
        return True
    elif bank.getPlayerMoney()==0:   #line 26
        print('Player broke!')
        return True
    else:
        return False

def buildBank():   # set money for players, output is bank = initial money
    invalid=True
    while invalid:
        money=input('How much money do you want to start with? ($100 to $5000, $5 increment): ')
        if not isInt(money):
            print('Bank: Money needs to be an integer!')
        elif int(money)<100:
            print('Bank: Minimum $100!')
        elif int(money)>5000:
            print('Bank: Maximum $5000!')
        elif int(money)%5!=0:
            print('Bank: Must be $5 increment!')
        else:
            bank=Bank(int(money),int(money),0)   # bank becomes object of Bank class,line 17
            invalid=False
    return bank

def printBanner():
    print("********************************************************************\n")
    print("                          CIS 40 Final Project                      \n")
    print("                              Blackjack                             \n")
    print("                              Have Fun!                             \n")
    print("********************************************************************\n")

# Main scripts
printBanner()   # greetings, line 252
bank=buildBank()  # = initialize money, line 235
numOfDecks=getNumOfDecks()    # ask for number of decks, line 178
deck=Deck(numOfDecks)   # set up all cards, line 5
print("You're playing with",numOfDecks,'deck,',numOfDecks,'* 52 =',numOfDecks*52,'cards total.')
dealer=Dealer(deck)   # dealer is now object of Dealer class, has all tools with cards, line 39
print('Dealer starts shuffling...')
dealer.shuffleDeck()     # shuffle all cards, line 43
time.sleep(1)
print('Dealer finished shuffling.')
time.sleep(1)

userContinue=True
while userContinue:   # main loop to start game
    placeBet(bank)     # ask for bet, line 184
    print('Dealer starts dealing...')
    time.sleep(1)
    dealer.initialDeal()   # dealer and player get first 2 cards, line 46

    blackJack=dealer.checkForBlackjack()   # check for blackjack first, line 128
    if blackJack!='none':   # if there is blackjack
        dealer.payout(blackJack,bank)   # announce winner, line 150
        chipCount(bank)    # announce money, line 203
        if ifBroke(bank)==True:   # check if someone is broke, line 225
            break
        userContinue=ifContinue()   # ask for another round, line 206
        if userContinue==False:   # if player chooses no, stop game
            break
        else:
            continue

    playerOutcomes=dealer.calculatePoints(dealer.getPlayerHand()) # calculate player's point, line 93  # get cards of player, line 59
    option=playerOptions(bank,dealer,playerOutcomes)   # ask for decision from player, line 214

    playerNotBust=True
    while playerNotBust and option=='1':   # loop for player to hit cards
        dealer.playerHit()   # player hits a card, line 62
        playerOutcomes=dealer.calculatePoints(dealer.getPlayerHand())  # calculate player's point again, line 291
        if dealer.bustOrNot(playerOutcomes)==False:   # check if player busts, line 107
            print('Player bust!')
            dealer.payout('dealer',bank)   # if player busts, announce winner is dealer, line 150
            playerNotBust=False   # loop is canceled
        else:
            option=playerOptions(bank,dealer,playerOutcomes)   # if not busts, ask for option again, line 292

    if ifBroke(bank)==True:   # check if someone is broke, line 225
        break
    if playerNotBust==False:   # when player busts, turn ends, dealer announces money and asks if player wants to play more, line 301
        chipCount(bank)    # announce money, line 203
        userContinue=ifContinue()   # ask if play another round, line 206
        if userContinue==False:
            break
        else:
            continue
        
    dealer.flipBottomCard()   # dealer reveals second card, line 80
    dealerOutcomes=dealer.calculatePoints(dealer.getDealerHand())  # calculate dealer's point, line 93
    if dealer.isUnderSeventeen(dealerOutcomes)==False:  # check if dealer's point is under 17, line 113
        underSeventeen=False
    else:
        underSeventeen=True

    dealerNotBust=True
    while underSeventeen and dealerNotBust:  # loop for dealer to hit cards
        dealer.dealerHit()   # dealer hits a card, line 87
        dealerOutcomes=dealer.calculatePoints(dealer.dealerHand)  # calculate dealer's point again, line 316
        if dealer.isUnderSeventeen(dealerOutcomes)==False:   # check if dealer's point is still under 17 or not, line 317
            underSeventeen=False
        if dealer.bustOrNot(dealerOutcomes)==False:   # check if dealer busts, line 107
            print('Dealer bust!')
            dealer.payout('player',bank)   # if dealer busts, announce winner is player, line 150
            dealerNotBust=False   # loop is canceled
            
    if ifBroke(bank)==True:   # check if someone is broke, line 225
        break
    if dealerNotBust==False:   # when dealer busts, dealer announces money and asks if player wants to play more, line 331
        chipCount(bank)   # announce money, line 203
        userContinue=ifContinue()   # ask if play another round, line 206
        if userContinue==False:
            break
        else:
            continue

    dealerPoints=dealer.optimalHand(dealerOutcomes)   # assign dealer's point, line 142
    playerPoints=dealer.optimalHand(playerOutcomes)   # assign player's point, line 142

    winner=dealer.decideWinner(dealerPoints, playerPoints)   # determine winner, line 162
    dealer.payout(winner, bank)   # announces winner, line 150

    chipCount(bank)   # announce money, line 203
    if ifBroke(bank)==True:   # check if someone is broke, line 225
        break
    userContinue=ifContinue()   # no one busts, either wins by normal way, ask if player wants to play more, if not, exit the loop

print('Game Over!')
