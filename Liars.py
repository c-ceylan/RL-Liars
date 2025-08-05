import numpy as np

from Card import Card
from Deck import Deck

class InvalidGuess(Exception):
    pass

class Liars():
    '''
    Everybody starts with 2 cards.
    If you lose the round, you gain a card.
    If you reach 6 cards, you can no longer see your cards.
    If you lose another round after reaching 6, you lose the game.
    
    Minimum number of players is 2, maximum number of players is 8.
    
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
        
    def reset_game(self):
        # My Player ID is 0. 
        # Other players go from 1-to-N.
        self.player_no_cards = {}
        
        for i in range(self.no_players):
            self.player_no_cards[i] = 2
            
        self.game_over = -1
        
        # Random player starts.
        self.starting_player = np.random.randint(0, self.no_players)
        
        self.current_player = self.starting_player
        self.prev_guess = [-1, -1, -1, -1]
    
    def check_game_over(self):
        # All players are eliminated. Return winner.
        # Otherwise game continues.
        if len(self.player_no_cards) == 1:
            self.game_over = min(self.player_no_cards)
            
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
        # Losing player gets another card. 
        # If it exceeds 6, the player is eliminated.
        self.player_no_cards[losing_player] += 1
        
        if self.player_no_cards[losing_player] > 6:
            del self.player_no_cards[losing_player]
        
        # Also when calling other player's guesses, 
        # x+1 calls x's guesses, and so on.
        
        # The player to the right of the losing player starts 
        # the next round.
        self.starting_player = (losing_player+1)%self.no_players
    
    def see_player_cards(self, player_no=0):
        print(self.this_round_cards_per_player_shown[player_no])
        
    def check_if_guess_true(self, this_guess):
        no1, rank1, no2, rank2 = this_guess
        
        # When a player's guess is called, check if the guess was true or not.
        # If there is no [no2, rank2], enter them as 0.
        this_round_cards = {rank1: 0, rank2: 0, 2: 0}
        
        for _, pCards in self.this_round_cards_per_player.items():
            for pCard in pCards:
                if pCard.rank in this_round_cards:
                    this_round_cards[pCard.rank] += 1
        
        # Wild Cards needed to reach to Success State.
        diff1 = max(0, no1-this_round_cards[rank1]) 
        diff2 = max(0, no2-this_round_cards[rank2])
        
        if (diff1+diff2) <= this_round_cards[2]:
            return True
        else:
            return False
    
    def check_valid_guess(self, this_round_guess):
        # Check if the guess is valid.
        no_pair = [this_round_guess[0], this_round_guess[2]]
        
        # [0, 0, 0, 0] calls previous guess.
        # Valid if previous guess wasn't the starting guess.
        if ((this_round_guess == [0, 0, 0, 0]
             ) and (self.prev_guess != [-1, -1, -1, -1])):
            return True
        
        # If they guessed '2' as rank, it is invalid 
        # b/c '2' is Wild Card.
        # Also, maximum rank is 14 for Ace.
        # There is no '1'. 
        # '0' is allowed for no guess for second slot.
        elif ((~this_round_guess[1] in range(3, 15)
               ) or (~this_round_guess[3] in ([0] + list(range(3, 15))))):
            return False
        
        # The number guesses have to be one of the below.
        elif no_pair not in [[2, 0], [3, 0], [3, 2], [4, 0], [5, 0], 
                             [5, 3], [6, 0], [7, 0], [8, 0], [8, 4]]:
            return False
        
        # If they increased the first number of cards guessed vs
        # previous guess, it is a valid guess.
        elif this_round_guess[0] > self.prev_guess[0]:
            return True
        
        # If they increased the second number of cards guessed vs
        # previous guess while first number is same, it is a valid guess.
        elif ((this_round_guess[0] == self.prev_guess[0]
              ) and (this_round_guess[2] > self.prev_guess[2])):
            return True
        
        # If both first and second numbers are the same, 
        # if the first rank is higher, it is a valid guess.
        elif ((this_round_guess[0] == self.prev_guess[0]
              ) and (this_round_guess[2] == self.prev_guess[2]
                     ) and (this_round_guess[1] > self.prev_guess[1])):
            return True
        
        # If both first and second numbers, and the first ranks are the same, 
        # if the second rank is higher, it is a valid guess.
        elif ((this_round_guess[0] == self.prev_guess[0]
              ) and (this_round_guess[2] == self.prev_guess[2]
                     ) and (this_round_guess[1] == self.prev_guess[1]
                            ) and (this_round_guess[3] > self.prev_guess[3])):
            return True
        
        # Otherwise, it is invalid.
        else:
            return False
    
    def play_round(self, this_round_guess):
        # Check for valid guess.
        if self.check_valid_guess(this_round_guess):
            # Update current player and previous guess.
            self.current_player = (self.current_player+1)%self.no_players
            self.prev_guess = this_round_guess[:]
        else:
            raise InvalidGuess('Invalid Guess. Check the rules.')
    
        
if __name__ == "__main__":
    L = Liars(3)
    
    L.start_round()
    
    print(L.this_round_cards_per_player_shown)