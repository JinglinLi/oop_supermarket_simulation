"""Customer Class"""


import random
import pandas as pd


class Customer:
    """a single customer that moves through the supermarket in a MCMC simulation."""


    STATES = ['checkout', 'dairy', 'drinks', 'entrance', 'fruit', 'spices']
    TPM = pd.read_csv('tpm.csv', index_col=[0])


    def __init__(self, name, state, budget=100):
        self.name = name
        self.state = state
        self.budget = budget


    def __repr__(self):
        return f'<Customer {self.name} in {self.state}>'


    def is_active(self):
        """returns True if the customer has not reached the checkout yet."""
        return self.state != 'checkout'


    def next_state(self):
        """propagates the customer to the next state."""
        transition_probs = Customer.TPM.loc[Customer.TPM.index==self.state].values[0]
        self.state = random.choices(Customer.STATES, weights=transition_probs)[0]
