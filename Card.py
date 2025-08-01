class Card():
    ''' 
    Blind Card: -1
    
    Suits:
        Hearts: 0
        Spades: 1
        Diamonds: 2
        Clubs: 3
        
    Ranks:
        Jack: 11
        Queen: 12
        King: 13
        Ace: 1 
    '''
    def __init__(self, suit, rank, blind=False):
        self.suit = suit
        self.rank = rank
        
        self.blind = blind
        
        self.suit_str_map = {0: "\u2661", 
                             1: "\u2660",
                             2: "\u2662",
                             3: "\u2663"}
        
        self.rank_str_map = {2: '2', 3: '3', 4: '4', 5: '5', 
                             6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 
                             11: 'J', 12: 'Q', 13: 'K', 1: 'A'}
        
    def __repr__(self):
        if self.blind:
            return '..'
        else:
            return f'{self.suit_str_map[self.suit]}{self.rank_str_map[self.rank]}'
    
    def __eq__(self, other):
        return (self.suit == other.suit) & (self.rank == other.rank)
    
    def get_blind_copy(self):
        return Card(self.suit, self.rank, blind=True)
    
    def get_liars_priority(self):
        if self.rank in range(3, 14):
            return self.rank
        # Ace, return 14
        elif self.rank == 1:
            return 14
        # 2, Wild Card, return 15
        elif  self.rank == 2:
            return 15

        
if __name__ == "__main__":
    C = Card(0, 5)