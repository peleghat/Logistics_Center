import sqlite3
from DAOs import *
from Repository import repo
import os
import sys


def file_parser():
    file = open(sys.argv[1], 'r', encoding="utf-8")  # 'config.txt' = sys.argv[1]
    lines = file.readlines()
    lines = [i.strip() for i in lines]
    file.close()
    ind = lines[0]
    arr = ind.split(",")
    ints = [int(i) for i in arr]

    log_list = lines[-ints[3]:]
    cli_list = lines[-ints[3] - ints[2]:-ints[3]]
    sup_list = lines[-ints[3] - ints[2] - ints[1]:-ints[3] - ints[2]]
    vac_list = lines[-ints[3] - ints[2] - ints[1] - ints[0]:-ints[3] - ints[2] - ints[1]]

    for line in log_list:
        members = tuple(line.split(","))
        repo.logistics.insert(logistic(*members))

    for line in cli_list:
        members = tuple(line.split(","))
        repo.clinics.insert(clinic(*members))
        repo.total_demand = repo.total_demand + int(members[2])

    for line in sup_list:
        members = tuple(line.split(","))
        repo.suppliers.insert(supplier(*members))

    for line in vac_list:
        members = tuple(line.split(","))
        repo.vaccines.insert(vaccine(*members))
        repo.total_inventory = repo.total_inventory + int(members[3])


def delete_tables():  # for debugging purposes
    repo._conn.execute("""DROP TABLE logistics;""")
    repo._conn.execute("""DROP TABLE clinics;""")
    repo._conn.execute("""DROP TABLE suppliers;""")
    repo._conn.execute("""DROP TABLE vaccines;""")
    os.remove("output.txt")


def orders_parser():
    file = open(sys.argv[2], 'r', encoding="utf-8")  # 'orders.txt' = sys.argv[2]
    lines = file.readlines()
    lines = [i.strip() for i in lines]
    file.close()
    for order in lines:
        members = tuple(order.split(","))
        if len(members) == 3:
            repo.receive(*members)
        if len(members) == 2:
            repo.send(*members)


def main():
    # delete_tables()
    open(sys.argv[3], "w").close()  # "output.txt"= sys.argv[3]
    repo.create_tables()
    file_parser()
    orders_parser()


if __name__ == '__main__':
    main()
