# The Repository
import atexit
import sqlite3
import sys

from DAOs import logistics, clinics, suppliers, vaccines
from DTOs import *


def write_output(line):
    file = open(sys.argv[3], "a", encoding="utf-8")  # "output.txt" = sys.argv[3]
    file.write(line + "\n")
    file.close()


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.logistics = logistics(self._conn)
        self.clinics = clinics(self._conn)
        self.suppliers = suppliers(self._conn)
        self.vaccines = vaccines(self._conn)
        self.total_inventory = 0
        self.total_demand = 0
        self.total_received = 0
        self.total_sent = 0

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE logistics (
            id      INTEGER       PRIMARY KEY,
            name    STRING        NOT NULL,
            count_sent INTEGER    NOT NULL,
            count_received INTEGER    NOT NULL
        );
    
        CREATE TABLE clinics (
            id      INTEGER       PRIMARY KEY,
            location    STRING        NOT NULL,
            demand INTEGER    NOT NULL,
            logistic INTEGER    REFERENCES  logistics(id)
        );
        
        CREATE TABLE suppliers (
            id      INTEGER       PRIMARY KEY,
            name   STRING        NOT NULL,
            logistic INTEGER    REFERENCES  logistics(id)
        );
        
        CREATE TABLE vaccines (
            id      INTEGER       PRIMARY KEY,
            date    DATE       NOT NULL,
            supplier INTEGER    REFERENCES suppliers(id),
            quantity INTEGER    NOT NULL 
        );
    
        
    """)

    def receive(self, supplier_name, amount, date):
        vaccines_max_id = self._conn.execute("SELECT MAX(ID) FROM vaccines").fetchone()[0]
        supplier_id = self._conn.execute("SELECT ID FROM suppliers WHERE name = ?", [supplier_name]).fetchone()[0]
        self.vaccines.insert(vaccine(vaccines_max_id + 1, date, supplier_id, amount))
        logistic_id = self._conn.execute("SELECT logistic FROM suppliers WHERE name = ?", [supplier_name]).fetchone()[0]
        self.logistics.update_receive(logistic_id, amount)
        self.total_inventory = self.total_inventory + int(amount)
        self.total_received = self.total_received + int(amount)
        write_output(f"{self.total_inventory},{self.total_demand},{self.total_received},{self.total_sent}")

    def send(self, location, amount):
        amount = int(amount)
        clinics_data = self._conn.execute("SELECT * FROM clinics WHERE location = ?", [location]).fetchone()
        demand = clinics_data[2]
        demand = int(demand) - amount
        self.clinics.update(location, demand)
        logistic_id = clinics_data[3]
        self.logistics.update_send(logistic_id, amount)

        # Remove The sum of amount from the inventory
        self.total_inventory = self.total_inventory - amount
        self.total_demand = self.total_demand - amount
        self.total_sent = self.total_sent + amount
        while amount > 0:
            vaccine_data = self._conn.execute("""SELECT * FROM vaccines
                                               ORDER BY date ASC ;""").fetchone()
            vaccine_id = vaccine_data[0]
            vaccine_quantity = int(vaccine_data[3])
            if amount >= vaccine_quantity:
                amount = amount - vaccine_quantity
                self.vaccines.remove(vaccine_id)
            else:
                new_quantity = vaccine_quantity - amount
                self.vaccines.update(vaccine_id, new_quantity)
                amount = 0

        write_output(f"{self.total_inventory},{self.total_demand},{self.total_received},{self.total_sent}")


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
