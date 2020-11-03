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
    print_play(play)
    winner, reason = select_winner(play)
    print('Player {:<d} wins: {:s}.'.format(winner,reason))


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
    
#    if reason=='max':
#        maxval = 0
#        maxplayerdict1 = {}
#        for key, val in cards.items():
#            if val[2][0] >= maxval:
#                maxval=val[2][0]
#                maxplayerdict1[key]=val
#
#        if len(maxplayerdict1) > 1:
#            maxval = 0
#            maxplayerdict2 = {}
#            for key, val in maxplayerdict1.items():
#                if val[1][0] >= maxval:
#                    maxval=val[1][0]
#                    maxplayerdict2[key]=val
#            
#            return list(maxplayerdict2.keys())[0], reason
#        else:
#            return list(maxplayerdict1.keys())[0] , reason    
#

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


def print_play(play):
    display = {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A',
    }

    for k,v in play.items():
        print('{:2d}. {:>2s}{} {:>2s}{} {:>2s}{}'.\
        format(k, display.get(v[0][0], str(v[0][0])), v[0][1],\
               display.get(v[1][0], str(v[1][0])), v[1][1],\
               display.get(v[2][0], str(v[2][0])),v[2][1]),end="\n\n")

if __name__ == '__main__':
    main()
