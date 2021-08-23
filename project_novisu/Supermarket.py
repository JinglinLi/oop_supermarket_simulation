"""Supermarket Class"""


import numpy as np
import pandas as pd
from Customer import Customer


CUSTOMER_PER_MINUTE = 1 # Poisson distribution
T_RESOLUTION = '1 min'


class Supermarket:
    """manages multiple Customer instances that are currently in the market."""

    def __init__(self):
        self.customers = [] # a list of Customer objects
        self.minutes = 0
        self.last_id = 0


    def __repr__(self):
        return f'It is {self.minutes} now, and there are {len(self.customers)} customers in the supermarket.'
    

    def set_time(self, current_time):
        """update current time"""
        self.minutes = current_time


    def print_customers(self):
        """print all customers with the current time and id in CSV format."""
        for one_customer in self.customers:
            print(f'{self.minutes}, {one_customer.name}, {one_customer.state}')


    def next_minute(self):
        """propagates all customers to the next state."""
        for one_customer in self.customers:
            one_customer.next_state()


    def add_new_customers(self):
        """randomly creates new customers."""
        n_add = np.random.poisson(lam=CUSTOMER_PER_MINUTE)
        for i in range(n_add):
            c = Customer(str(self.last_id), 'entrance')
            self.customers.append(c)
            self.last_id += 1


    def remove_exitsting_customers(self):
        """removes every customer that is not active any more."""
        self.customers=[c for c in self.customers if c.is_active()]


    def simulate(self, t_start, t_end):
        for t in pd.date_range(t_start, t_end, freq=T_RESOLUTION):
            self.set_time(t)
            self.add_new_customers()
            self.remove_exitsting_customers()
            self.next_minute()
            self.print_customers()


if __name__ == "__main__":
    rewe = Supermarket()
    rewe.simulate('2021-09-17 07:00:00', '2021-09-17 07:15:00')
    print(rewe)
