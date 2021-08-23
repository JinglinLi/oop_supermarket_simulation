"""
Supermarket Class including visualization.
"""


import cv2
import time
import pandas as pd
import numpy as np
from SupermarketMapClass import SupermarketMap
from CustomerClass import Customer


CUSTOMER_PER_MINUTE = 1 # Poisson distribution
MAX_N_CUSTOMERS = 6 # restrict maximal number of customers in supermarket
T_RESOLUTION = '1 min'


class Supermarket:
    """manages multiple Customer instances that are currently in the market including."""


    def __init__(self):
        self.customers = [] # a list of Customer objects
        self.minutes = 0
        self.last_id = 0


    def __repr__(self):
        return f'It is {self.minutes} now, and there are {len(self.customers)} customers in the supermarket.'


    def update_time(self, current_time):
        """update current time : pandas datetime."""
        self.minutes = current_time
        return self.minutes


    def add_new_customers(self):
        """add new customers."""
        if len(self.customers) < MAX_N_CUSTOMERS: # retrict maximal n customers in supermarket
            n_add = np.random.poisson(lam=CUSTOMER_PER_MINUTE) 
            for i in range(n_add):
                customer_id = self.last_id # last customer id
                one_customer = Customer(str(customer_id), 'entrance', self) # instanciate one customer
                self.customers.append(one_customer) # add one customer
                self.last_id += 1 # update last customer id


    def remove_existing_customers(self):
        """removes every customer that is not active any more."""
        for one_customer in self.customers:
            if one_customer.is_active() is False:
                self.customers.remove(one_customer)


    def next_minute(self):
        """propagates all customers to the next state."""
        for one_customer in self.customers:
            one_customer.next_state_rowcol() # propagates state and location
            one_customer.path_between_states() # calculate path
            # resample path into 1s resolution
            t_all = pd.date_range(self.minutes, self.minutes + pd.Timedelta('1 min'),
                periods=len(one_customer.path))
            path_orig = pd.DataFrame(one_customer.path, index=t_all, columns=['row','col'])
            path_resample = path_orig.resample('s').ffill()
            one_customer.path_row_col = path_resample.values # [[row, col], [row, col], ...]


    def draw_one_min(self):
        """draw the movements of all customers within one minute in 1 second resolution."""
        background = np.zeros((500, 700, 3), np.uint8) # black background
        frame = background.copy()
        marketmap = SupermarketMap() # instanciate supermarket map

        for i_sec in range(60):
            marketmap.draw(frame) # draw supermarket
            for customer in self.customers:
                customer.draw_sec(frame, i_sec)
            cv2.imshow("frame", frame)
            key = cv2.waitKey(50) # ms


    def print_customers(self):
        """print all customers : current time, customer_id, state."""
        for one_customer in self.customers:
            print(self.minutes, ',', one_customer.name, ',', one_customer.state_after)


    def simulate(self, t_start, t_end):
        for t in pd.date_range(t_start, t_end, freq=T_RESOLUTION):
            self.update_time(t)
            self.add_new_customers()
            self.next_minute()
            self.draw_one_min()
            self.print_customers() # print : time, id, state
            print(self) # print : time and number of customers in supermarket
            self.remove_existing_customers()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rewe = Supermarket()
    rewe.simulate('2021-09-17 07:00:00', '2021-09-17 07:15:00')

