import sqlite3


# Data Transfer Objects:

class logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


class clinic:
    def __init__(self, id, location, demand, r_logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = r_logistic


class supplier:
    def __init__(self, id, name, r_logistic):
        self.id = id
        self.name = name
        self.logistic = r_logistic


class vaccine:
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity
