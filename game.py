"""
A simple card game a la poker.

10 players. 52 cards.

Each player is dealt with 3 cards drawn randomly one-by-one to players in turn.

Cards have weights from 2-14.

select_winner will decide who wins.
"""
import secrets


def main():
    """
    The main method
    """
    deck = init_deck()
    play = deal(deck,10)
    # print_play(play)
    print(play_bid(play))
    # winner, reason = select_winner(play)
    # print('Player {:<d} wins: {:s}.'.format(winner,reason))


def init_deck():
    """
    Initialize the deck.
    """
    deck = [(i,'♠️ ') for i in range(2,15)]\
    + [(i, '♦️ ') for i in range(2,15)]\
    + [(i,'♥️ ') for i in range(2,15)]\
    + [(i,'♣️ ') for i in range(2,15)]

    return deck

def deal(deck,num):
    """
    Deal the cards.
    """
    secretsgen = secrets.SystemRandom()
    play = {}
    for i in range(1, 4) :
        for j in range(1, num+1):

            # play is a dict {playernum:[card1, card2, card3]}
            nextnum = secretsgen.randint(0, len(deck)-1)
            nextcard = deck[nextnum]
            del deck[nextnum]
            if j not in play:
                play[j] = [nextcard]
            else:
                play[j].append(nextcard)
    return play

def tiebreak(cards, reason):
    """
    Find maximum of the card set.
    """
    doubledict = {}

    if reason=='double' and len(cards)>1:
        for key, val in cards.items():
            # figure out the double value
            dval = val[0][0] if val[0][0] == val[1][0] else val[1][0]
            doubledict[dval]=key
        
        return sorted(doubledict.items())[-1][1], reason
    

    tot = {}
    for key, val in cards.items():
        tot[val[0][0] + val[1][0] + val[2][0]] = key

    #return sorted(tot.items(), key=lambda x: x[0])[-1][1]
    return sorted(tot.items())[-1][1], reason


def select_winner(play):
    """
    Select the winner.
    """
    color = {}
    sequence = {}
    coloredsequence = {}
    double = {}
    triple = {}

    for k,val in play.items():
        val.sort(key = lambda x:x[0]) # sort cards so its easy to find sequence
        #print('{:2d} {}'.format(k, val))

        if val[0][1] == val[1][1] == val[2][1]:
            color[k] = val

        if val[0][0] == val[1][0] == val[2][0]:
            triple[k] = val

        if val[0][0] == val[1][0] or val[1][0] == val[2][0] or val[0][0] == val[2][0]:
            double[k] = val

        if (val[0][0] == val[1][0]-1 and val[1][0] == val[2][0]-1)\
             or sorted([val[0][0],val[1][0],val[2][0]])==[2,3,14]:
            sequence[k] = val

        if ((val[0][0] == val[1][0]-1 and val[1][0] == val[2][0]-1) \
            or (sorted([val[0][0],val[1][0],val[2][0]])==[2,3,14])) \
            and val[0][1] == val[1][1] == val[2][1]:

            coloredsequence[k] = val


    if triple:
        return tiebreak(triple,"triple")

    if coloredsequence:
        return tiebreak(coloredsequence, "colored sequence")

    if sequence:
        return tiebreak(sequence, "sequence")

    if color:
        return tiebreak(color, "colour")

    if double:
        return tiebreak(double, "double")
    
    max_sorted = sorted(play.items(), key=lambda x: (x[1][2], x[1][1], x[1][0]), reverse=True)
    maxkey = max_sorted[0][0]

    return maxkey, "max"


def print_play(play,x):
    display = {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A',
    }

    v = play.get(x)
    print('{:>2s}{} {:>2s}{} {:>2s}{}'.\
    format(display.get(v[0][0], str(v[0][0])), v[0][1],\
            display.get(v[1][0], str(v[1][0])), v[1][1],\
            display.get(v[2][0], str(v[2][0])),v[2][1]),end="\n\n")


"""
The logic for bidding and continuing gameplay stays here
"""
def play_bid(play):
    bid = 1
    total_bid = 0
    folded = 0
    keys_to_pop = []

    while True:
                
        if len(play) > 2:
            print("\nCuurent bid for : {cur_bid} $ and Total Bid is {total} $".
            format(cur_bid = bid,total = total_bid))

            for i in play:
                print("\nplayer {}'s turn: \n  ".format(i))

                if folded == 9:
                    return "You win with {}$ everyone else Folded".format(total_bid)

                print_play(play,i)
                choice = input("Press 'F' to Fold or 'B' to Bid : ")

                if choice == "F" :
                    keys_to_pop.append(i)
                    folded += 1
                    print("Player {} Folded".format(i))
                
                elif choice == "B" :
                    total_bid += bid
                    print("Player {player} bidded; Total bid increased to {total} $ ".
                    format(player = i, total = total_bid))

        else:
            if len(play) == 1:
                for i in play:
                    return "Player {} Won with total amount {}$".format(i, total_bid)

            print("Only two player's left")
            print("\nCuurent bid for : {cur_bid} $ and Total Bid is {total} $".
            format(cur_bid = bid,total = total_bid))

            for i in play:
                print("\nplayer {}'s turn: \n  ".format(i))
                print_play(play,i)
                choice = input("Press 'F' to Fold or 'B' to Bid or 'S' to Bid and Show : ")

                if choice == "F":
                    keys_to_pop.append(i)
                    print("Player {} Folded".format(i))
                    break

                elif choice == "S" :
                    winner, reason = select_winner(play)
                    Result = "Player {:<d} wins: {:s} with total amount {:d}$".format(winner,reason, total_bid)
                    return Result

                elif choice == "B" :
                    total_bid += bid
                    print("Player {player} bidded; Total bid increased to {total} $ ".
                    format(player = i, total = total_bid))
                    
        for i in keys_to_pop:
            play.pop(i)
        keys_to_pop = []
        bid += 1

    while(True):
        choice = input()


if __name__ == '__main__':
    main()
