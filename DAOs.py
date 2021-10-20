# Data Access Objects:
# All of these are meant to be singletons
import sqlite3
from DTOs import *


# should the classes be private?

class logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, new_logistic):
        self._conn.execute("""
               INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ? ,?)
           """, [new_logistic.id, new_logistic.name, new_logistic.count_sent, new_logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, count_sent, count_receive FROM logistics WHERE id = ?
        """, [logistic_id])

        return logistic(*c.fetchone())

    def update_receive(self, logistic_id, amount):
        c = self._conn.cursor()
        last_amount = c.execute("SELECT count_received FROM logistics WHERE id=?", [logistic_id]).fetchone()[0]
        c.execute("""UPDATE logistics
                     SET count_received = (?)
                     WHERE id = (?)""", [int(last_amount) + int(amount), logistic_id])

    def update_send(self, logistic_id, amount):
        c = self._conn.cursor()
        last_amount = c.execute("SELECT count_sent FROM logistics WHERE id=?", [logistic_id]).fetchone()[0]
        c.execute("""UPDATE logistics
                     SET count_sent = (?)
                     WHERE id = (?)""", [int(last_amount) + int(amount), logistic_id])

class clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, new_clinic):
        self._conn.execute("""
               INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ? ,?)
           """, [new_clinic.id, new_clinic.location, new_clinic.demand, new_clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, demand, logistic FROM clinics WHERE id = ?
        """, [clinic_id])

        return clinic(*c.fetchone())

    def update(self, location, demand):
        c = self._conn.cursor()
        c.execute("""UPDATE clinics
                     SET demand = (?)
                     WHERE location = (?)""", [demand, location])


class suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, new_supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [new_supplier.id, new_supplier.name, new_supplier.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, logistic FROM suppliers WHERE id = ?
        """, [supplier_id])

        return supplier(*c.fetchone())


class vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, new_vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id,date ,supplier,quantity) VALUES (?, ?, ?, ?)
           """, [new_vaccine.id, new_vaccine.date, new_vaccine.supplier, new_vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, date, supplier, quantity FROM vaccines WHERE id = ?
        """, [vaccine_id])

        return vaccine(*c.fetchone())

    def remove(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("DELETE FROM vaccines WHERE id = ?", [vaccine_id])

    def update(self, vaccine_id, new_quantity):
        c = self._conn.cursor()
        c.execute("""UPDATE vaccines
                     SET quantity = (?)
                     WHERE id = (?)""", [new_quantity, vaccine_id])


