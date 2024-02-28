# Spaceflight Traffic Management System
This application is used to manage all space traffic within a region of space of any size.

## Table of Contents

## Description
### High-level description
Suppose it is 3300 years into the future, where humanity has perfected faster-than-light travel, resulting in spaceports
of variable sizes being built and put into orbit around planets of star systems.
This application aims to manage and track the status of all inbound and outbound space traffic of a certain region in
space, which can be a handful of star systems or a governmental territory of hundreds of systems.

The goal of this project is to produce an application capable of assisting space-age governmental parties by presenting cleanly
formatted data in a timely manner. Users can query for ships that have a bounty attached, pilots with certain reputations,
or pilots with certain illicit cargo, along with a variety of other administrative tasks, such as updating a pilot's reputation status,
or issuing a bounty on a ship.

This project is inspired by the 2015 space simulation video game *Elite: Dangerous*

### Code documentation
Package involves a SQLServer database `SpaceTrafficManager` and Python code to process user input and execute queries.

#### Basic use-case
1. Program start
2. Display menu
3. Select options
4. Execute queries
5. Repeat 2-4 until QUIT.

#### SQL Tables

- Station(_StationID_, StationName, StationSystem, StationOrbitPlanet, StationState)
  - _StationID_ - Primary Key, unique ID number of each station.
  - StationName - name of each station
  - StationSystem - the star system in which the station resides
  - StationOrbitPlanet - the planet around which the station orbits.
  - StationState - the operational state of the station. A True value indicates that the station is operating normally.
  a False value indicates severe structural damage, requiring rescue operations.
- Station_Model(ModelID, ModelMake, ModelName, ModelNumPads)
  - _ModelID_ - Primary key, unique ID number of the station model.
  - ModelMake - Company responsible for designing the station model.
  - ModelName - the name of the model.
  - ModelNumPads - the number of landing pads this station model has.
- Ship(_ShipID_, ShipName, ShipState, ShipBounty)
  - _ShipID_ - Primary key. The ship's license plate number.
  - ShipName - The name designated to the ship by its owner.
  - ShipState - The physical state of the ship, last seen by the station it last docked in.
  - ShipBounty - The current bounty placed on the ship by the user's affiliated faction.
- Ship_Model(_ModelID_, ModelMake, ModelName)
  - _ModelID_ - unique identifier
  - ModelMake - Company responsible for design of ship model.
  - ModelName - The name of the ship model.
- Pilot(_PilotID_, PilotName, PilotLicenseAcquisitionDate, PilotBirthDate, PilotNationality)
  - _PilotID_ - Primary key. The pilot's license number.
  - PilotName - The name of the pilot
  - PilotLicenseAcquisitionDate - the date on which the pilot was granted a license
  - PilotBirthDate - the birthdate of the pilot
  - PilotNationality - Pilot's state of origin

##### UML of object relationships.
![Database UML](https://github.com/mickle0629/CS-374-Final-Project/blob/master/uml_img.jpg?raw=true)

#### User functions
 ##### Query for ship information
 - Find a ship based on ShipID
 - Find a ships with bounties over x credits
 - Find a ship's location (station)
 - Find all ships owned by a pilot
 ##### Query for station information
 - Find stations based on StationID
 - Find damaged stations
 - Find stations that contain ships owned by a specific pilot
 ##### Query for pilot information
 - Find a pilot based on pilotID
 - Find a pilot whose reputation is within a threshold range
 ##### Update information
 - Add a pilot profile
 - Add a ship record
 - Add a station record
 - Add a docking record
 - Add a ship ownership record

#### Query functions
All query functions produces a .csv file in the Query Results folder. Additionally, 
since the function `input()` returns a string, all query functions take input as 
strings. Furthermore, the last positional argument in every function, `connection_string` 
stores the SQLServer access string.
- `get_ship_by_id(id, connection_string)`
  - Description
    - Given a `string` id, function finds a ship associated with this string 
- `get_ship_by_bounty(bounty_lower, bounty_upper, connection_string)`
  - Description
    - finds a list of ships with a bounty in the range [`bounty_lower`, `bounty_upper`]
- `get_pilot_by_id(id, connection_string)`
  - Description
    - finds a pilot based on their license identification number, represented by `string` 
    id.
- `get_pilots_within_reputation(rep_lower, rep_higher, connection_string)`
  - Description:
    - finds a list of all pilots with a reputation number within a range of [`rep_lower`,`rep_higher`].
- `get_station_by_id(id, connection_string)`
  - Description:
    - finds a station based on its associated identification number `string` id.
- `get_station_by_operational_status(operational, connection_string)`
  - Description:
    - if `operational` is passed as `1`, function produces a list of stations that are operational. Else if `operational` is set
    to `0`, function produces stations that are in a damaged status.
#### Updating functions
- `update_new_ship(shipName, shipState, shipBounty, connection_string)`
  - Description:
    - Creates a new ship record with ship data in parameter list.
- `update_new_station(StationName, StationSystem, StationOrbitPlanet, StationOperational, connection_string)
  - Description:
    - Creates a new station record with all station data in parameter list.
- `update_pilot_table(PilotFName, PilotLname, lDate, bDate, PilotNationality, PilotReputation, connection_string)`
  - Description:
    - Creates a new pilot record with all pilot data in paramter list.
- `link_pilot_ship(PilotID, ShipID, connection_string)`
  - Description:
    - Links a ShipID to a PilotID to represent an ownership relationship.
#### Supporting functions
 - `get_formatted_rows(rows, name, field_names)`
    - Description
      - Produces a .csv-formatted string of rows given the tuple of rows returned by `cursor.execute()`
 - `write_row_to_csv(formatted_string, file_name)`
   - Description:
     - Function simply writes a .csv-formatted string into a .csv file.
 - `get_field_names_to_csv(rows_description)`
   - Description:
     - Takes attribute information from the description value of cursor.execute(), converts it into a
     .csv-format string, and writes it into a .csv file. This operation is usually prior to writing data
     into csv files.
   
## System requirements
Single system using SQLServer and Python 3.10 with the pyodbc module installed.
- Install pyodbc: https://pypi.org/project/pyodbc/

## Acknowledgements
Authors
- An Dang, adang24@whitworth.edu
- Jonathan Hamstra, jhamstra24@whitworth.edu
- Jay Phillips, jayphillips23@whitworth.edu
