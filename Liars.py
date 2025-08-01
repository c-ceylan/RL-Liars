from Card import Card
from Deck import Deck

# TODO: Write a rules README

# XXX: For Liars, suits are irrelevant, so don't keep track of them?

class Liars():
    '''
    Everybody starts with 2 cards.
    If you lose the round, you gain a card.
    If you reach 6 cards, you can no longer see your cards.
    If you lose another round after reaching 6, you lose the game.
    
    Min no opponents is 1, max no opponents is 7.
    
    The card rankings are as usual w/ Ace ranking the highest.
    2 is the wild card, can be counted as any ranked card.
    
    The number guessed always outranks the rank of the card guessed.
        (e.g. 3-9s outranks 2-Aces)
    
    For combination guesses, major number determines rank priority,
    if the major number ranks are equal, minor number detirmines priority.
        (e.g. 3-Aces-2-9s outranks 3-Kings-2-Jacks;
              3-Aces-2-9s outranks 3-Aces-2-6s)
    
    Allowed number guesses and their prioritization are as follows:
        2, 3, 3-2, 4, 5, 5-3, 6, 7, 8, 8-4
        
    The next player has to either call your guess, 
    or raise either the number of cards or the rank of the cards.

    '''
    def __init__(self, no_players):
        # Number of players: [2, 8]
        self.no_players = no_players
        
        self.reset_game()
        
        self.game_over = 0
            
    def reset_game(self):
        # My Player ID is 0. 
        # Other players go from 1-to-N.
        self.player_no_cards = {}
        
        for i in range(self.no_players):
            self.player_no_cards[i] = 2
            
    def check_game_over(self):
        # I lost.
        if self.player_no_cards[0] > 6:
            self.game_over = -1
        # All opponents are eliminated, I won.
        elif len(self.player_no_cards) == 1:
            self.game_over = 1
        # Game continues.
        else:
            self.game_over = 0
            
        return self.game_over
    
    def start_round(self):
        # Reset Deck
        self.deck = Deck()
        
        self.this_round_cards_per_player = {}
        self.this_round_cards_per_player_shown = {}
        
        for playerID, no_cards in self.player_no_cards.items():
            cards_for_player = self.deck.draw_cards(no_cards)
            
            self.this_round_cards_per_player[playerID] = cards_for_player
            
            if no_cards < 6:
                self.this_round_cards_per_player_shown[
                    playerID] = cards_for_player
            else:
                self.this_round_cards_per_player_shown[
                    playerID] = [C.get_blind_copy() for C in cards_for_player]
    
    def end_round(self, losing_player):
        pass
    
    def see_my_cards(self):
        print(self.this_round_cards_per_player_shown[0])
    
        
if __name__ == "__main__":
    L = Liars(3)
        