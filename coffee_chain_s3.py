import numpy as np
from scipy.stats import poisson, uniform, norm, expon
import datetime as dt
from dataclasses import dataclass, field


import queue, threading
import random
import unittest
import json



class DataGen:
    def __init__(self) -> None:
        pass


    def get_timestamp(self,start_time:dt.datetime,mu:float= 3,size:int=100)->list:
        """
        generates arrival times of customers to the shop 
        start_time : datetime_object. the simulation will anchor this time as start
        mu : mu parameter for exponential distribution
        """
        arrival_secs = np.cumsum(expon.rvs(loc = 1/mu , size= size))
        timestamps = [start_time+dt.timedelta(minutes=x) for x in arrival_secs]
        str_time = [timestamps for x in timestamps]
        return timestamps


    def generate_menu(self,names:list)->dict:
        pass






class Customer:
    def __init__(self,arrival_time:dt.datetime)->None:
        self.arrival_time = arrival_time
    

    def get_order(self, menu):
        idx = random.choices(menu)
        return idx


class Barista:
    def __init__(self,name,score,menu):
        self.name = name
        self.score = score
        self.menu = menu
        self.processing_time = dt.timedelta(minutes=0)
        self.wait_time = dt.timedelta(minutes=0)
        self.latest_served_at = dt.datetime(1970,1,1)
        
    def assign(self, customer):
        order_data = {}
        order = customer.get_order(self.menu)
        order_size = random.choices(["small","medium","large"])[0]
        arrival_time = customer.arrival_time
        processing_time = dt.timedelta(minutes = order["processing_time"])
        
        # if customer arrived earlier than latest order finish time
        if self.latest_served_at > arrival_time:
            # customer has to wait until the earlier order is ready
            self.wait_time = self.latest_served_at - arrival_time
        else:
            self.wait_time = dt.timedelta(minutes=0)
            
        order_begin_time = arrival_time + self.wait_time
        order_end_time = order_begin_time + processing_time
        self.latest_served_at = order_end_time
            
        
        # update current processing time
        self.processing_time = dt.timedelta(minutes=order["processing_time"])
        

        order_price = order.get(order_size)
        order_data["barista_name"] = self.name
        order_data["arrival_time"] = str(arrival_time)
        order_data["begin_time"] = str(order_begin_time)
        order_data["processing_time"] = self.processing_time.seconds
        order_data["end_time"] = str(order_end_time)
        order_data["wait_time"] = self.wait_time.seconds
        order_data["item_name"] = order["Name"]
        order_data["order_size"] = order_size
        order_data["order_price"] = order_price
        
        return order_data

class Barista:
    def __init__(self,name,score,menu):
        self.name = name
        self.score = score
        self.menu = menu
        self.processing_time = dt.timedelta(minutes=0)
        self.wait_time = dt.timedelta(minutes=0)
        self.latest_served_at = dt.datetime(1970,1,1)
        
    def assign(self, customer):
        order_data = {}
        order = customer.get_order(self.menu)
        order_size = random.choices(["small","medium","large"])[0]
        arrival_time = customer.arrival_time
        processing_time = dt.timedelta(minutes = order["processing_time"])
        
        # if customer arrived earlier than latest order finish time
        if self.latest_served_at > arrival_time:
            # customer has to wait until the earlier order is ready
            self.wait_time = self.latest_served_at - arrival_time
        else:
            self.wait_time = dt.timedelta(minutes=0)
            
        order_begin_time = arrival_time + self.wait_time
        order_end_time = order_begin_time + processing_time
        self.latest_served_at = order_end_time
            
        
        # update current processing time
        self.processing_time = dt.timedelta(minutes=order["processing_time"])
        

        order_price = order.get(order_size)
        order_data["barista_name"] = self.name
        order_data["arrival_time"] = str(arrival_time)
        order_data["begin_time"] = str(order_begin_time)
        order_data["processing_time"] = self.processing_time.seconds
        order_data["end_time"] = str(order_end_time)
        order_data["wait_time"] = self.wait_time.seconds
        order_data["item_name"] = order["Name"]
        order_data["order_size"] = order_size
        order_data["order_price"] = order_price
        
        return order_data
        
              
# the more barita a store employes
class Store:
    
    """
    Orchestrates overall activity of the coffee store
    """
    def __init__(self,baristas):
        self.baristas = baristas
        self.reset_barista_availability()
        
        
    def reset_barista_availability(self):
        for x in self.baristas:
            x.processing_time=0
        
    
    def next_barista(self,customer):
        processing_times = [(customer.arrival_time - x.latest_served_at).seconds for x in self.baristas]
        next_barista = self.baristas[np.argmin(processing_times)]
        return next_barista
    
    def get_inventory(self):
        # as customers order an item, inventory runs out
        pass
    

class Simulator:
    def __init__(self, begin_date):
        self.begin_date = begin_date
        
    

# barista1 = Barista("Dave",90,menu)
# barista2 = Barista("Lucy",100,menu)
# barista3 = Barista("Ella",100,menu)


# baristas = [barista1, barista2]
# customer = Customer(arrival_times[0])
# store = Store(baristas)



class TestDataGen(unittest.TestCase):
    
    def test_get_timestamp(self):
        datagen = DataGen()
        start_time = dt.datetime(2022,9,1)
        arrival_times = datagen.get_timestamp(start_time, mu=3,size=3)
        self.assertEqual(len(arrival_times),3)


    def test_customer(self):
        with open("menu.json") as f:
            menu = json.load(f)["menu"]

        arrival_time = dt.datetime(2022,10,1,9)
        customer = Customer(arrival_time)
        order = customer.get_order(menu=menu)
        print(order)
        


if __name__=="__main__":
    unittest.main()