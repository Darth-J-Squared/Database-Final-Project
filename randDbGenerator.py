import random

import pyodbc

"""
        I N D E P E N D E N T    U P D A T E    F U N C T I O N S 
"""


def add_pilot_record(id, name, license_acq_date, nationality, reputation, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"INSERT INTO Pilot VALUES ({id}, {name}, {license_acq_date}, {nationality}, {reputation})"
    cursor.execute(sql)
"""
        R A N D O M    R E C O R D    G E N E R A T O R    F U N C T I O N S
"""

def generate_pilot(drop, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    if drop:
        sql = "DROP TABLE Pilot"
        cursor.execute(sql)
    name_bank = ["Michael", "Richard", "Larry", "Amy", "Jasmine", "Minh", "Nguyen", "Jake", "Henry", "Khoi", "Jonathan"]

"""
Generate a random date between an lower and upper bound in years
"""
def random_date(lower, upper):
    random.seed()
    year = random.randrange(int(lower), int(upper))
    month = random.randrange(1, 12)

    date_string = f"{year}-{month}-"
    print(date_string)
    """
    date = ""
    if month % 2 == 0 and month != 2:
        date = random.randrange(1,30)
    elif month % 2 != 0:
        date = random.randrange(1,31)
    else:
        #TODO: check leap year
        date = random.randrange(1,28)
    date_string += date
    return date_string
    """

"""
Function to generate names
"""

