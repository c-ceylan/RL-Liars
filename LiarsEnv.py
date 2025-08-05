''' Liars Game Environment for RL. '''

import numpy as np
import gymnasium as gym

from Card import Card
from Deck import Deck
from Liars import Liars

class LiarsEnv(gym.Env):
    def __init__(self):
        # The Suits of the cards are irrelevant, 
        # so they don't need to be included in the 
        self.observation_space = gym.spaces.Box(low=-1, high=13, 
                                                shape=(2, 8, 6), dtype=int)
        
        # Action Space:
            # 4 Numbers
            # First is the number, second is the rank.
            # If all 0, call previous player.
            # Otherwise, raises.
        self.action_space = gym.spaces.Box(low=0, high=13, shape=(4, ), dtype=int)
        
        
        # Keeping history of player moves.
        # Previous Player's Calls.
        self.prev_player_calls = [0, 0, 0, 0]
        
    def start_game(self):
        pass
    
    def encode_game(self, player_no=0):
        # Encode game from the perspective of Player #.
        pass
    
    def get_other_player_move_EV(self):
        # Other players make 
        pass
    
    def get_other_player_move_Rnd(self):
        pass
    
    def get_other_player_move_Agent(self, other_agent):
        pass
    
    def _get_obs(self):
        pass
    
    def _get_info(self):
        pass
    
    def render(self):
        pass
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    
    def step(self, action):
        no1, rank1, no2, rank2 = action[0], action[1], action[2], action[3]
        
        # Called the previous player. Open up.
        if [no1, rank1, no2, rank2] == [0, 0, 0, 0]:
            pass
        
        # Raising the other player.
        else:
            if no1 > self.prev_player_call[0]:
                
            pass
        
        # Invalid action. Punish.
        
        terminated = False
        truncated = False
        reward = 0.001
        observation = self._get_obs()
        info = self._get_info()
                
        return observation, reward, terminated, truncated, info
