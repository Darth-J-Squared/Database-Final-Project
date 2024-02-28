# PURPOSE: Contains scripts that execute the specified queries based on user input
from types import prepare_class
import pyodbc
import os
DEBUGGING = True
import randDbGenerator


"""
        Q U E R Y    F U N C T I O N S
"""


"""
PURPOSE: Function finds the ship in the database with the specificed 'id'
INPUT  : id - the unique ShipID assigned to all ships at the time of purchasing.
         connectionString - string that establishes connection to SQLServer database for querying.
OUTPUT : Results stored in a .csv file in the "Query results" folder.
"""
def get_ship_by_id(id, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = "SELECT * FROM Ship WHERE Ship.ShipID = " + str(id)

    rows = cursor.execute(sql)
    get_formatted_rows(rows, f"Search for ShipID {id}", get_field_names_to_csv(cursor.description))

    print("Data successfully retrieved. .csv file created in Query results folder.")

"""
PURPOSE: Finds all ships wth a bounty in the range [bounty_lower, bounty_upper]
INPUT  : bounty_lower - the lower bound of the bounty range
         bounty_upper - the upper bound of the bounty range
         connectionString - establishes connection to the SQLServer database.
OUTPUT : Results stored in a .csv file in the "Query results" folder.
"""
def get_ship_by_bounty(bounty_lower, bounty_upper, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"SELECT * FROM Ship WHERE Ship.ShipBounty > {bounty_lower} AND Ship.ShipBounty < {bounty_upper}"

    rows = cursor.execute(sql)
    field_names = get_field_names_to_csv(cursor.description)

    get_formatted_rows(rows, f"Search by bounty {str([bounty_lower, bounty_upper])}", field_names)

    print("Data successfully retrieved. .csv file created in Query results folder.")
"""
PURPOSE: Finds ship associated with the target ShipID
INPUT  : id - ShipID in question
OUTPUT : Results stored in a .csv file in the "Query results" folder.
"""
def get_pilot_by_id(id, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"SELECT * FROM Pilot WHERE Pilot.PilotID = {id}"

    rows = cursor.execute(sql)
    field_names = get_field_names_to_csv(cursor.description)
    get_formatted_rows(rows, f"Search by PilotID {id}", field_names)

    print("Data successfully retrieved. .csv file created in Query results folder.")

"""
PURPOSE: Finds all pilot wth a reputation value in the range [rep_lower, rep_higher]
INPUT  : rep_lower - the lower bound of the reputation range
         rep_higher - the upper bound of the reputation range
         connectionString - establishes connection to the SQLServer database.
OUTPUT : Results stored in a .csv file in the "Query results" folder.
"""
def get_pilots_within_reputation(rep_lower, rep_higher, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"SELECT * FROM PILOT WHERE Pilot.PilotReputation >= {rep_lower} AND Pilot.PilotReputation <= {rep_higher}"

    rows = cursor.execute(sql)
    field_names = get_field_names_to_csv(rows.description)
    get_formatted_rows(rows, f"Search by PilotReputation {str([rep_lower, rep_higher])}", field_names)
    print("Data successfully retrieved. .csv file created in Query results folder.")

"""
PURPOSE: Finds station associated with the target StationID
INPUT  : id - StationID in question
OUTPUT : Results stored in a .csv file in the "Query results" folder.
"""
def get_station_by_id(id, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"SELECT Station.*, Station_Model.ModelName, Station_Model.Operational FROM Station, Station_Model, IsModelRel WHERE IsModelRel.StationID = Station.StationID AND IsModelRel.ModelID = Station_Model.ModelID AND Station.StationID = {id}"

    rows = cursor.execute(sql)
    field_names = get_field_names_to_csv(rows.description)
    get_formatted_rows(rows, f"Search by StationID {id}", field_names)
    print("Data successfully retrieved. .csv file created in Query results folder.")
"""
PURPOSE: Finds stations that are operational or damaged, dependent on parameter.
INPUT  : operational - if "1" is passed, function returns stations that are operational.
                       if "0" is passed, function returns stations that are severely damaged.
OUTPUT : Results stored in a .csv file in the "Query results" folder.
"""
def get_station_by_operational_status(operational, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"SELECT * FROM Station WHERE StationOperational = {operational}"

    rows = cursor.execute(sql)
    field_names = get_field_names_to_csv(rows.description)
    get_formatted_rows(rows, f"Search by StationOperational {str(operational)}", field_names)
    print("Data successfully retrieved. .csv file created in Query results folder.")

"""
PURPOSE: Retrieves a list of pilot ownership relationships.
"""
def get_pilot_ship_relations(connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = f"SELECT P.PilotName, P.PilotLastName, S.ShipName FROM Pilot as P, Ship as S, PilotOwns as PO WHERE PO.PilotID = P.PilotID AND PO.ShipID = S.ShipID"

    rows = cursor.execute(sql)
    field_names = get_field_names_to_csv(rows.description)
    get_formatted_rows(rows, f"Search for all pilot owned ships", field_names)
    print("Data successfully retrieved. .csv file created in Query results folder.")

"""
            U P D A T E   F U N C T I O N S                                           
"""


def update_new_ship(shipName, shipState, shipBounty, connection_string) :
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = "SELECT MAX(shipID) AS ShipID FROM SHIP"
    rows = cursor.execute(sql)
    for row in rows:
        current_ID = (row.ShipID)
    current_ID += 1

    sql = f"INSERT INTO Ship (ShipID, ShipName, ShipState, ShipBounty) VALUES ('{current_ID}', '{shipName}', '{shipState}', '{shipBounty}');"
    cursor.execute(sql)
    connection.commit()

def update_new_station(StationName, StationSystem, StationOrbitPlanet, StationOperational, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = "SELECT MAX(StationID) AS StationID FROM STATION"
    rows = cursor.execute(sql)
    for row in rows:
        current_ID = (row.StationID)
    current_ID += 1

    sql = f"INSERT INTO Station (StationID, StationName, StationSystem, StationOrbitPlanet, StationOperational) VALUES ('{current_ID}', '{StationName}', '{StationSystem}', '{StationOrbitPlanet}', '{StationOperational}');"
    cursor.execute(sql)
    connection.commit()



def update_pilot_table(PilotFName, PilotLname, lDate, bDate, PilotNationality, PilotReputation, connection_string):

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = "SELECT MAX(PilotID) AS PilotID FROM Pilot"
    rows = cursor.execute(sql)
    for row in rows:
        current_ID = (row.PilotID)
    current_ID += 1

    sql = f"INSERT INTO Pilot (PilotID, PilotName, PilotLicenseAcqDate, PilotBirthDate, PilotNationality, PilotReputation, PilotLastName) VALUES ('{current_ID}', '{PilotFName}', '{lDate}', '{bDate}', '{PilotNationality}', '{PilotReputation}', '{PilotLname}');"
    cursor.execute(sql)
    connection.commit()

def link_pilot_ship(PilotID, ShipID, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    sql = "SELECT MAX(ID) AS ID FROM PilotOwns"
    rows = cursor.execute(sql)
    for row in rows:
        current_ID = (row.ID)
    current_ID += 1

    sql = f"INSERT INTO PilotOwns (ID, PilotID, ShipID) VALUES ('{current_ID}', {PilotID}', '{ShipID}');"
    cursor.execute(sql)
    connection.commit()

"""
            S U P P O R T I N G   F U N C T I O N S                                           
"""


"""
PURPOSE: This function processes rows obtained from a cursor.execute() statement into csv format. 
INPUT: rows - the rows object obtained from cursor.execute()
       name - name of the csv file. Included in the parameter list so that the function write_row_to_csv() can name the
       .csv file, since the name of the file depends on what kind of query is done, which is information available from
       query functions themselves.
"""
def get_formatted_rows(rows, name, field_names):
    write_row_to_csv(field_names, name)
    for row in rows:
        formatted_string = ""
        for i in range(len(row) - 1):
            formatted_string += str(row[i]) + ", "
        formatted_string += str(row[len(row) - 1])

        write_row_to_csv(formatted_string, name)
"""
PURPOSE: Takes a string in .csv format and writes it to a .csv file.
INPUT  : formatted_string -  the .csv-formatted string produced by get_formatted_rows()
OUTPUT : file_name - name of the .csv file acquired from the query execution functions, passed through get_formatted_rows(),
         and finally into this function, write_row_to_csv().
"""
def write_row_to_csv(formatted_string, file_name):
    if not os.path.exists("Query results"):
        os.makedirs("Query results")
    file = open(f"Query results/{file_name}.csv", "a")
    file.write(formatted_string + "\r")
    file.close()
"""
PURPOSE: Function acquires field names from rows.description and produces a string of field names in .csv format
INPUT  : rows_description - the return value of the pyodbc attribute .description, detailing metadata on the results of queries.
"""
def get_field_names_to_csv(rows_description):
    field_string_csv = ""
    for field in rows_description:
        field_string_csv += field[0] + ", "
    return field_string_csv

"""
PURPOSE: This function displays the top level instructions of the menu.
INPUT  : None
OUTPUT : None
"""
def display_menu_start():
    print("////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("//                                                                                                    //")
    print("//                          Spaceport Intragalactic Management Protocol                               //")
    print("//                                           v0.1                                                     //")
    print("//                                                                                                    //")
    print("////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("//                                                                                                    //")
    print("//    What would you like to do today,                                                                //")
    print("//    Administrator?                                                                                  //")
    print("//        [1] Query                                                                                   //")
    print("//        [2] Update                                                                                  //")
    print("//        [Q] Exit                                                                                    //")
    print("//                                                                                                    //")
    print("////////////////////////////////////////////////////////////////////////////////////////////////////////")


"""
PURPOSE: This function displays the query selection level of the menu.
INPUT  : None
OUTPUT : None
"""
def display_menu_queries():
    print("//                                                                                                    //")
    print("//    Which queries would like to execute?                                                            //")
    print("//        Ship-related queries                                                                        //")
    print("//            [1] Find all ship info based on ShipID.                                                  //")
    print("//            [2] Find ships with bounties.                                                            //")
    print("//        Station-related queries                                                                     //")
    print("//            [3] Find a station based on StationID.                                                   //")
    print("//            [4] Find stations based on condition.                                                    //")
    print("//        Pilot-related queries                                                                       //")
    print("//            [5] Find a pilot based on PilotID.                                                       //")
    print("//            [6] Find pilots within a reputation range.                                              //")
    print("//            [7] Find all pilot-owned ships.                                                         //")
    print("//            [Q] Return to main menu                                                                 //")
    print("//                                                                                                    //")
    print("////////////////////////////////////////////////////////////////////////////////////////////////////////")

def display_menu_update():
    print("//     Which table would you like to update?                                                          //")
    print("//        [1] Add a ship record.                                                                       //")
    print("//        [2] Add a station record.                                                                    //")
    print("//        [3] Add a pilot record.                                                                      //")
    print("//        [4] Link a pilot to a ship.                                                                  //")
    print("//        [5] Add a docking record.                                                                    //")


if __name__ == "__main__":
    #TODO: Add a delay between query completion and switch to main menu.
    #TODO: On query completion, return to query menu, not main.
    username, password = "",""
    if not DEBUGGING:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
    else:
        username = "adang24x"
        password = "2333867"

    connectionString = r'DRIVER={SQL Server};Server=CS1;Database=SpaceTrafficManager;uid=' + username + ';pwd=' + password + ';'

    program_terminate = False

    display_menu_start()

    while not program_terminate:
        display_menu_start()
        user_input = input("Press the keyboard button corresponding to the number of the desired option: ")
        match user_input.lower():
            # Main menu input processing cases
            case "1":
                display_menu_queries()
                user_input = input("Select the desired query: ")
                match user_input.lower():
                    # Query select menu input processing cases
                    case "1":
                        input_ShipID = input("Enter ShipID: ")
                        get_ship_by_id(input_ShipID, connectionString)
                    case "2":
                        lower_bounty, upper_bounty = input("Enter the lower bound of the bounty range: "), input("Enter the upper bound of the bounty range: ")
                        get_ship_by_bounty(lower_bounty, upper_bounty, connectionString)
                    case "3":
                        input_StationID = input("Enter StationID: ")
                        get_station_by_id(input_StationID, connectionString)
                    case "4":
                        input_StationOperational = input("Search for stations that are [Operational (1)/Damaged (0)]: ")
                        get_station_by_operational_status(input_StationOperational, connectionString)
                    case "5":
                        pilotID = input("Enter PilotID for search: ")
                        get_pilot_by_id(pilotID, connectionString)
                    case "6":
                        rep_lower = input("Enter the lower bound of your reputation threshold: ")
                        rep_higher = input("Enter the higher bound of your reputation threshold: ")
                        get_pilots_within_reputation(rep_lower, rep_higher, connectionString)
                    case "7":
                        get_pilot_ship_relations(connectionString)
                    case "q":
                        display_menu_start()
                        continue
            case "2":
                display_menu_update()
                user_input = input("Select your an update operation: ")
                match user_input:
                    case "1":
                        print ("We will need to collect some data to continue:")
                        shipName = input("Enter ShipName           ")
                        user_input = input("Select ShipState:\n1:PRISTINE\n2.DAMAGED               ")
                        match user_input:
                            case "1": shipState = "PRISTINE"
                            case "2": shipState = "DAMAGED"
                        while True:
                            try:
                                shipBounty = int(input("Enter any known bounty:            "))
                                break
                            except:
                                print("Please enter a number:")

                        update_new_ship(shipName, shipState, shipBounty, connectionString)
                        pass
                    case "2":
                        print ("We will need to collect some data to continue:")
                        stationName = input("Enter StationName:           ")
                        stationSystem = input("Enter StationSystem:               ")
                        stationOrbitPlanet = input("Enter StationOrbitPlanet:               ")
                        stationOperational = input("Select StationOperation State:\n1:OPERATIONAL\n2.NON-OPERATIONAL               ")
                        match user_input:
                            case "1": stationOperational = 1
                            case "2": stationOperational = 0
            

                        update_new_station(stationName, stationSystem, stationOrbitPlanet, stationOperational, connectionString)
                        pass

                    case "3":
                        print ("We will need to collect some data to continue:")

                        PilotFName = input("Enter Pilot's first name:           ")
                        PilotLname = input("Enter Pilot's last name:            ")
                        lDate = input("Enter Pilot's date of license acquired (form YYYY-MM-DD):        ")
                        bDate = input("Enter Pilot's Date of birth (form YYYY-MM-DD):            ")
                        PilotNationality = input("Enter Pilot's nationality:         ")
                        PilotReputation = input("Enter Pilot's reputation (between 0-1):         ")

                        update_pilot_table(PilotFName, PilotLname, lDate, bDate, PilotNationality, PilotReputation, connectionString)
                        pass
                    
                    case "4":
#                        print ("We will need to collect some data to continue:")
#
#                        PilotID = input("Enter Pilot's ID:           ")
#                        ShipID = input("Enter Ship ID:              ")
# 
#                        link_pilot_ship(PilotID, ShipID, connectionString)
                        pass
                    case "q":
                        print("(Placeholder exit message)")
                program_terminate = True
