import numpy as np
import time

from Card import Card

class Deck():
    def __init__(self, set_seed=None):
        self.reset_deck()
                
        if set_seed:
            np.random.seed = set_seed
        else:
            # For reproducibility.
            self.__seed = time.time_ns()
            # print(f'\nSeed: {self.__seed}\n')
            np.random.seed = self.__seed
    
    
    def reset_deck(self):
        self.cards = []
        
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
    
    def draw_cards(self, no_draw, with_replacement=False):
        cards_drawn = []
        
        for _ in range(no_draw):
            draw_idx = np.random.randint(0, len(self.cards)+1)
            
            if not with_replacement:
                draw = self.cards.pop(draw_idx)
                cards_drawn.append(draw)
            
            else:
                cards_drawn.append(self.cards[draw_idx])
                
        return cards_drawn
            
                

if __name__ == "__main__":
    D = Deck(set_seed=5)
    
    x = D.draw_cards(2)