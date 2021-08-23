"""
Customer Class including visualization.
"""


import random
import pandas as pd
import numpy as np
from a_star import find_path
from SupermarketMapClass import SupermarketMap
import constants


class Customer:
    """ customer class including visualization."""

    # possible states of a customer
    STATES = ['checkout', 'dairy', 'drinks', 'entrance', 'fruit', 'spices']

    # transition probability matrix
    TPM = pd.read_csv('tpm.csv', index_col=[0])

    # row and col range of each state
    STATE_ROW_COL = {
        'entrance':[[10], [14, 15]],
        'fruit':[[2,3,4,5,6], [14, 15]],
        'spices':[[2,3,4,5,6], [10, 11]],
        'dairy':[[2,3,4,5,6], [6, 7]],
        'drinks':[[2,3,4,5,6], [2, 3]],
        'checkout':[[10], [2, 3]],
        }

    # grid of supermarket map for calculating customer path
    GRID = np.array([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])

    # possible moves of a customer
    POSSIBLE_MOVES = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]


    def __init__(self, name, state, supermarket):
        """
        name : str
        state : str : one of STATE
        supermarket : a supermarket object
        """
        self.name = name
        self.state_before = state # starting state
        self.state_after = state
        self.row_before = 10 # starting row
        self.col_before = 14 # starting column
        self.row_after = 10
        self.col_after = 14
        self.path = [] # path between start and after; row,col, calculated with a* algorithm
        self.path_row_col = [] # row, col on the path in 1second resolution

        self.supermarket = supermarket # Supermarket instance

        marketmap = SupermarketMap() # instanciate marketmap
        avatar = SupermarketMap().extract_tile(7, 2)
        self.supermarketmap = marketmap # SupermarketMap instance
        self.avatar = avatar # a numpy array containing a 32x32 tile image


    def __repr__(self):
        return f'<Customer {self.name} in {self.state}>'


    def is_active(self):
        """returns True if the customer has not reached the checkout yet."""
        return self.state_after != 'checkout'


    def next_state_rowcol(self):
        """update state, row, col before and after state transition.
        """
        # state before and after propagation
        self.state_before = self.state_after
        transition_probs = list(Customer.TPM.loc[Customer.TPM.index==self.state_before].values[0])
        self.state_after = random.choices(Customer.STATES, weights=transition_probs)[0]
        # row and col before and after propagation
        self.row_before = self.row_after
        self.col_before = self.col_after

        # randomly chose row_after, col_after depending on the state_after
        if self.state_after == 'fruit':
            self.row_after = random.choice(Customer.STATE_ROW_COL['fruit'][0])
            self.col_after = random.choice(Customer.STATE_ROW_COL['fruit'][1])
        elif self.state_after == 'spices':
            self.row_after = random.choice(Customer.STATE_ROW_COL['spices'][0])
            self.col_after = random.choice(Customer.STATE_ROW_COL['spices'][1])
        elif self.state_after == 'dairy':
            self.row_after = random.choice(Customer.STATE_ROW_COL['dairy'][0])
            self.col_after = random.choice(Customer.STATE_ROW_COL['dairy'][1])
        elif self.state_after == 'drinks':
            self.row_after = random.choice(Customer.STATE_ROW_COL['drinks'][0])
            self.col_after= random.choice(Customer.STATE_ROW_COL['drinks'][1])
        elif self.state_after == 'checkout':
            self.row_after = random.choice(Customer.STATE_ROW_COL['checkout'][0])
            self.col_after = random.choice(Customer.STATE_ROW_COL['checkout'][1])


    def path_between_states(self):
        """calculate path between row,col before and after state transition."""

        start_given = (self.row_before, self.col_before) # row, col before state transition
        finish_given = (self.row_after, self.col_after) # row, col after state transition

        # find_path based on a* algorithm
        path = find_path(Customer.GRID, start_given, finish_given, Customer.POSSIBLE_MOVES)

        # if empty path fillin values to enable next step interpolation into 1s resolution
        if start_given == finish_given:
            path = [(self.row_before, self.col_before), (self.row_after, self.col_after)]

        self.path = path


    def draw_sec(self, frame, i_sec):
        """draw customer on i-th second of the path"""
        if self in self.supermarket.customers:  
            row_i = self.path_row_col[i_sec,0]
            col_i = self.path_row_col[i_sec,1]
            if self.supermarketmap.contents[row_i][col_i] == '.':
                x = col_i * constants.TILE_SIZE
                y = row_i * constants.TILE_SIZE
                frame[y:y+constants.TILE_SIZE, x:x+constants.TILE_SIZE] = self.avatar
                # to do : avoide overlapping customer