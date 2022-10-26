import requests,json,pickle,sqlite3,time,pathlib,os,random
from Essential_Functions import Spacing,CalculateSpacing,PickleDump,PickleLoad,ConnectDatabase,ConvertTupleList,GetTableInfo,SelectAllRecords,SelectRecord,SQLSelectOne,GetDataSetInfo,OutputDataSetInfo,ShowDataSetInfo


# Get a list of all the tanks in the game from the API
def GetGameTanks(ApplicationID):
    WGResponse = requests.get("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/", params = {"application_id":ApplicationID})
    WGResponseJSON = WGResponse.json()
    GameTanks = WGResponseJSON["data"]
    return GameTanks


# Get the player's overall statistics from their account_id, this can also be a list of player IDs
def GetPlayerStatistics(ApplicationID,PlayerID):
    WGResponse = requests.get("https://api.worldoftanks.eu/wot/account/info/", params = {"application_id":ApplicationID,"account_id":str(PlayerID)})
    WGResponseJSON = WGResponse.json()
    PlayerData = WGResponseJSON["data"]
    return PlayerData

# Get the player's tanks from their account_id, this can also be a list of player IDs
def GetPlayerTanks(ApplicationID,PlayerID):
    WGResponse = requests.get("https://api.worldoftanks.eu/wot/account/tanks/", params = {"application_id":ApplicationID,"account_id":str(PlayerID)})
    WGResponseJSON = WGResponse.json()
    PlayerTankData = WGResponseJSON["data"]
    return PlayerTankData


# Function to get a set of 100 player records from a defined section of the API
def GetDataSegment(ApplicationID,BaseID,Count,Type):
    # Add the set of 100 player IDS into a string to add as a paramter to the API request
    AccountIDList = ""
    for PlayerID in range(BaseID, BaseID + Count):
        AccountIDList += str(PlayerID) + "%2C"
    # Remove the final comma in the list
    AccountIDList = AccountIDList[:len(AccountIDList) - 3]

    # If the function call specifies PlayerStatistics then retreive these from the API
    if Type == "PlayerStatistics":
        APISource = "https://api.worldoftanks.eu/wot/account/info/?account_id="
        Parameters = {"application_id":ApplicationID, "fields":"-account_id,-client_language,-nickname,-private,-statistics.clan,-statistics.company,-statistics.epic,-statistics.fallout,-statistics.globalmap_absolute,-statistics.globalmap_champion,-statistics.globalmap_middle,-statistics.historical,-statistics.ranked_10x10,-statistics.ranked_15x15,-statistics.ranked_battles,-statistics.ranked_battles_current,-statistics.ranked_battles_previous,-statistics.ranked_season_1,-statistics.ranked_season_2,-statistics.ranked_season_3,-statistics.regular_team,-statistics.stronghold_defense,-statistics.stronghold_skirmish,-statistics.team,-statistics.frags"}
    # Else, if the function call specifies PlayerTanks then retreive these from the API
    elif Type == "PlayerTanks":
        APISource = "https://api.worldoftanks.eu/wot/account/tanks/?account_id="
        Parameters = Parameters = {"application_id":ApplicationID}

    # Processing the API request is done within a while loop to prevent an API error causing issues for the dataset
    Trying = True
    TryingNo = 0
    while Trying == True:
        TryingNo += 1
        # Attempt to retreive the data from the API
        WGResponse = requests.get(APISource + AccountIDList, params = Parameters)
        WGResponseJSON = WGResponse.json()

        # If the response returns a status of ok then do not repeat the attempt
        if WGResponseJSON["status"] == "ok":
            Trying = False
        else:
            # If the API call has failed 50 times in a row, wait for 20 seconds before trying again
            if TryingNo == 50:
                time.sleep(20)
            # Else, if the API call has failed 100 times in a row, request input to determine if the program should continue
            elif TryingNo == 100:
                Spacing(1)
                print("Tried " + str(TryingNo) + " times and failed. Keep trying? (Y/N)")
                Input = input().upper()
                if Input == "N":
                    Trying = False
                    return {}
            # Else, output the error code from the API
            else:
                Spacing(1)
                print("Error code " + str(WGResponseJSON["error"]["code"]) + " with message: " + WGResponseJSON["error"]["message"])
                print("RETRYING...")
                Spacing(1)

    # Loop through the currently pulled player records
    for PlayerID in range(BaseID, BaseID + Count):
        # If the current player record is empty or has 0 overall battles then delete it
        if Type == "PlayerStatistics":
            if WGResponseJSON["data"][str(PlayerID)] == None or WGResponseJSON["data"][str(PlayerID)]["statistics"]["all"]["battles"] == 0 or len(WGResponseJSON["data"][str(PlayerID)]) == 0:
                del WGResponseJSON["data"][str(PlayerID)]

        # If the current player record is empty or provides an empty list then delete it
        elif Type == "PlayerTanks":
            if WGResponseJSON["data"][str(PlayerID)] == None or len(WGResponseJSON["data"][str(PlayerID)]) == 0:
                del WGResponseJSON["data"][str(PlayerID)]

    return WGResponseJSON["data"]


# Function to add data from the API to the dataset
def AddData(cr,db,ApplicationID,CurrentID,NumberOfRecords):
    
    # Loop through player IDs, incrementing by 100 each time
    for PlayerID in range(CurrentID, CurrentID + NumberOfRecords, 100):

        # 100 player statistics and their repsective tanks played are pulled simultaneously to avoid inconsistency
        PlayerStatisticsSegment = GetDataSegment(ApplicationID,PlayerID,100,"PlayerStatistics")
        PlayerTanksSegment = GetDataSegment(ApplicationID,PlayerID,100,"PlayerTanks")

        # These records are then saved to the database and the CurrentID value before continuing
        # This acts as a backup, meaning if the script fails whilst pulling, currently pulled data is saved and not lost
        InsertPlayerStatistics(cr,db,PlayerStatisticsSegment)
        InsertPlayerTanks(cr,db,PlayerTanksSegment)
        PickleDump("CurrentID", PlayerID + 100)

        # Output the number of players in the currently pulled segment, allows for progress tracking
        print("PlayerStatistics: " + CalculateSpacing(len(PlayerStatisticsSegment),7) + "PlayerTanks: " + CalculateSpacing(len(PlayerTanksSegment),7) + "Progress: " + str(PlayerID + 100 - CurrentID) + " / " + str(NumberOfRecords) + "    Percentage: " + str(round(((PlayerID + 100 - CurrentID) / NumberOfRecords) * 100, 3)) + "%")


# Function to begin the process of pulling data for the dataset
def RunPull(cr,db,ApplicationID):
    print("Loading Database Info...")
    Spacing(1)

    # Calculate and output the information of the current dataset
    PlayerStatisticsCount, PlayerTanksCount, CurrentID = GetDataSetInfo(cr,db)
    OutputDataSetInfo(PlayerStatisticsCount, PlayerTanksCount, CurrentID)

    Spacing(1)

    # Get input which determines the number of records to pull
    print("How many records would you like to pull?")
    NumberOfRecords = int(input())

    print("          ----------          Pulling " + str(NumberOfRecords) + " Records          ----------")
    # Run the function to pull and save the specified number of players into the dataset
    AddData(cr,db,ApplicationID,CurrentID,NumberOfRecords)

    Spacing(3)
    print("          ----------          Finished Pulling Records          ----------")
    Spacing(3)

    # Calculate and output the new information of the dataset
    PlayerStatisticsCount, PlayerTanksCount, CurrentID = GetDataSetInfo(cr,db)
    OutputDataSetInfo(PlayerStatisticsCount, PlayerTanksCount, CurrentID)


# Function to insert the players statistics into the database
def InsertPlayerStatistics(cr,db,PlayerStatisticsDataSet):
    # For each player within the list of player statistics, insert the player's statistics into the database
    for PlayerID in PlayerStatisticsDataSet:
        PlayerRecord = PlayerStatisticsDataSet[PlayerID]
        SQL = """INSERT INTO PlayerStatistics (account_id,last_battle_time,created_at,updated_at,global_rating,clan_id,statistics$all$spotted,statistics$all$battles_on_stunning_vehicles,statistics$all$max_xp,statistics$all$avg_damage_blocked,statistics$all$direct_hits_received,statistics$all$explosion_hits,statistics$all$piercings_received,statistics$all$piercings,statistics$all$max_damage_tank_id,statistics$all$xp,statistics$all$survived_battles,statistics$all$dropped_capture_points,statistics$all$hits_percents,statistics$all$draws,statistics$all$max_xp_tank_id,statistics$all$battles,statistics$all$damage_received,statistics$all$avg_damage_assisted,statistics$all$max_frags_tank_id,statistics$all$avg_damage_assisted_track,statistics$all$frags,statistics$all$stun_number,statistics$all$avg_damage_assisted_radio,statistics$all$capture_points,statistics$all$stun_assisted_damage,statistics$all$max_damage,statistics$all$hits,statistics$all$battle_avg_xp,statistics$all$wins,statistics$all$losses,statistics$all$damage_dealt,statistics$all$no_damage_direct_hits_received,statistics$all$max_frags,statistics$all$shots,statistics$all$explosion_hits_received,statistics$all$tanking_factor,statistics$trees_cut,logout_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        cr.execute(SQL, (PlayerID, PlayerRecord["last_battle_time"], PlayerRecord["created_at"], PlayerRecord["updated_at"], PlayerRecord["global_rating"], str(PlayerRecord["clan_id"]), PlayerRecord["statistics"]["all"]["spotted"], PlayerRecord["statistics"]["all"]["battles_on_stunning_vehicles"], PlayerRecord["statistics"]["all"]["max_xp"], PlayerRecord["statistics"]["all"]["avg_damage_blocked"], PlayerRecord["statistics"]["all"]["direct_hits_received"], PlayerRecord["statistics"]["all"]["explosion_hits"], PlayerRecord["statistics"]["all"]["piercings_received"], PlayerRecord["statistics"]["all"]["piercings"], PlayerRecord["statistics"]["all"]["max_damage_tank_id"], PlayerRecord["statistics"]["all"]["xp"], PlayerRecord["statistics"]["all"]["survived_battles"], PlayerRecord["statistics"]["all"]["dropped_capture_points"], PlayerRecord["statistics"]["all"]["hits_percents"], PlayerRecord["statistics"]["all"]["draws"], PlayerRecord["statistics"]["all"]["max_xp_tank_id"], PlayerRecord["statistics"]["all"]["battles"], PlayerRecord["statistics"]["all"]["damage_received"], PlayerRecord["statistics"]["all"]["avg_damage_assisted"], PlayerRecord["statistics"]["all"]["max_frags_tank_id"], PlayerRecord["statistics"]["all"]["avg_damage_assisted_track"], PlayerRecord["statistics"]["all"]["frags"], PlayerRecord["statistics"]["all"]["stun_number"], PlayerRecord["statistics"]["all"]["avg_damage_assisted_radio"], PlayerRecord["statistics"]["all"]["capture_points"], PlayerRecord["statistics"]["all"]["stun_assisted_damage"], PlayerRecord["statistics"]["all"]["max_damage"], PlayerRecord["statistics"]["all"]["hits"], PlayerRecord["statistics"]["all"]["battle_avg_xp"], PlayerRecord["statistics"]["all"]["wins"], PlayerRecord["statistics"]["all"]["losses"], PlayerRecord["statistics"]["all"]["damage_dealt"], PlayerRecord["statistics"]["all"]["no_damage_direct_hits_received"], PlayerRecord["statistics"]["all"]["max_frags"], PlayerRecord["statistics"]["all"]["shots"], PlayerRecord["statistics"]["all"]["explosion_hits_received"], PlayerRecord["statistics"]["all"]["tanking_factor"], PlayerRecord["statistics"]["trees_cut"], PlayerRecord["logout_at"]))
    db.commit()


# Function to insert the players tanks into the database
def InsertPlayerTanks(cr,db,PlayerTanksDataSet):
    # For each player within the list of player tanks, insert their individual tanks into the database one by one
    for PlayerID in PlayerTanksDataSet:
        for Position in range(len(PlayerTanksDataSet[PlayerID])):
            SQL = """INSERT INTO PlayerTanks(account_id,tank_id,wins,battles,mark_of_mastery) VALUES (?,?,?,?,?)"""
            cr.execute(SQL, (int(PlayerID), PlayerTanksDataSet[PlayerID][Position]["tank_id"], PlayerTanksDataSet[PlayerID][Position]["statistics"]["wins"], PlayerTanksDataSet[PlayerID][Position]["statistics"]["battles"], PlayerTanksDataSet[PlayerID][Position]["mark_of_mastery"]))
    db.commit()


# Function to calculate which records are missing corresponding primary keys from each table
def CalculateMissingTankRecords(cr,db,GameTanks):
    print(str(len(GameTanks)) + " Tanks found in GameTanks")
    
    Spacing(1)
    # Get the list of unique tank ID values from the player records
    print("Getting distinct values...")
    cr.execute("""SELECT DISTINCT tank_id FROM PlayerTanks ORDER BY tank_id""")
    TankIDs = cr.fetchall()
    print(str(len(TankIDs)) + " Tanks found in WoTDB")

    Spacing(1)
    print("Sorting ID values...")
    TankIDs_NotInGameTanks = []
    TankIDs_NotInWoTDB = []

    # Find vehicles which are present in player records but not in the list of vehicles
    for TankID in TankIDs:
        TankID = str(TankID[0])
        if TankID not in GameTanks:
            TankIDs_NotInGameTanks.append(int(TankID))
    print(str(len(TankIDs_NotInGameTanks)) + " present in WoTDB not present in GameTanks")

    # Find vehicles which are present in the list of vehicles but not in any player records
    for TankID in GameTanks:
        # Convert the tank ID into a tuple with a single value
        # This is how SQL returns values from different records
        TankID_Tuple = (int(TankID),)       # This is done because SQL returns each row's result as a tuple
        if TankID_Tuple not in TankIDs:
            TankIDs_NotInWoTDB.append(int(TankID))
    print(str(len(TankIDs_NotInWoTDB)) + " present in GameTanks are not present in WoTDB")

    # Find the list of players which have vehicles within their statistics that have no corresponding tank record in the game tanks table
    Spacing(1)
    DeletePlayerIDs = []
    SQLString = """SELECT DISTINCT account_id FROM PlayerTanks WHERE tank_id IN """ + str(tuple(TankIDs_NotInGameTanks))
    cr.execute(SQLString)
    DeletePlayerIDs = ConvertTupleList(cr.fetchall())

    # Output the information for redundant records
    print("Players with Problematic Tanks: " + str(len(DeletePlayerIDs)))
    if len(DeletePlayerIDs) > 0:
        print("First ID: " + str(DeletePlayerIDs[0]))
        print("Final ID: " + str(DeletePlayerIDs[len(DeletePlayerIDs) - 1]))

    return TankIDs_NotInGameTanks,TankIDs_NotInWoTDB,DeletePlayerIDs


# Function to insert the GameTanks into the database
def InsertGameTanks(cr,db,GameTanks):
    print("Inserting GameTanks...")
    Spacing(1)
    # Loop through each tank within the game tanks dictionary
    for TankID in GameTanks:
        # Define variable names for specific values to make code easier to read
        tank_id = int(TankID)
        name = GameTanks[TankID]["name"]
        short_name = GameTanks[TankID]["short_name"]
        tag = GameTanks[TankID]["tag"]
        description = GameTanks[TankID]["description"]
        images_big_icon = GameTanks[TankID]["images"]["big_icon"]
        images_contour_icon = GameTanks[TankID]["images"]["contour_icon"]
        images_small_icon = GameTanks[TankID]["images"]["small_icon"]
        tier = GameTanks[TankID]["tier"]
        nation = GameTanks[TankID]["nation"]
        vehicle_type = GameTanks[TankID]["type"]

        # If the current tank has any special status, switch the special status to 1, otherwise it is 0
        SpecialStatusTags = ["is_gift", "is_premium", "is_premium_igr"]
        special_status = 0
        for SpecialStatus in SpecialStatusTags:
            if GameTanks[TankID][SpecialStatus] == True:
                special_status = 1

        # Insert the tank record into the database
        SQL = """INSERT INTO GameTanks (tank_id,name,short_name,tag,description,images$big_icon,images$contour_icon,images$small_icon,tier,nation,type,special_status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cr.execute(SQL, (tank_id, name, short_name, tag, description, images_big_icon, images_contour_icon, images_small_icon, tier, nation, vehicle_type, special_status))
        print("Added " + name)
        
    db.commit()
    Spacing(1)
    print("GameTanks Insertion Completed.")


# Function to generate the random ID values for players to replace their genuine ID values
def GenerateRandomPlayerIDs(cr,db):
    # Get the list of all account IDs within the player statistics table
    cr.execute("""SELECT account_id FROM PlayerStatistics""")
    Results = cr.fetchall()
    CurrentPlayerIDs = ConvertTupleList(Results)
    # Create a list of integers which increment by 1 up to the number of existing player IDs
    NewPlayerIDs = [x for x in range(1, len(CurrentPlayerIDs) + 1)]
    
    RandomPlayerIDs = []
    # Loop through each player ID
    for CurrentPlayerID in CurrentPlayerIDs:
        # Get a random new ID value by generating a random positional value for the new ID list
        NewPlayerID_Position = random.randint(0,len(NewPlayerIDs) - 1)
        NewPlayerID = NewPlayerIDs[NewPlayerID_Position]
        # Save the newly assigned random ID to a list
        RandomPlayerIDs.append(NewPlayerID)
        # Remove the used ID from the list of new IDs
        NewPlayerIDs.pop(NewPlayerID_Position)

    return CurrentPlayerIDs, RandomPlayerIDs


# Function to generate the random ID values for players to replace their genuine ID values
def GenerateRandomClanIDs(cr,db):
    # Get the list of all clan IDs within the player statistics table
    cr.execute("""SELECT DISTINCT clan_id FROM PlayerStatistics""")
    Results = cr.fetchall()
    CurrentClanIDs = ConvertTupleList(Results)
    # Remove the value which is equal to none, meaning they are not in a clan
    CurrentClanIDs.pop(CurrentClanIDs.index("None"))
    # Create a list of integers which increment by 1 up to the number of existing clan IDs
    NewClanIDs = [x for x in range(1, len(CurrentClanIDs) + 1)]
    
    RandomClanIDs = []
    # Loop through each clan ID
    for CurrentClanID in CurrentClanIDs:
        # Get a random new ID value by generating a random positional value for the new ID list
        NewClanIDs_Position = random.randint(0,len(NewClanIDs) - 1)
        NewClanID = NewClanIDs[NewClanIDs_Position]
        # Save the newly assigned random ID to a list
        RandomClanIDs.append(NewClanID)
        # Remove the used ID from the list of new IDs
        NewClanIDs.pop(NewClanIDs_Position)

    return CurrentClanIDs, RandomClanIDs



# Empty function created to test isolated lines of code without making the Main function messy
def Testing(cr,db,ApplicationID):
    print()



def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    ApplicationID = #

    #GameTanks = PickleLoad("GameTanks")
    
    #Testing(cr,db,ApplicationID,GameTanks)

    #ShowDataSetInfo(cr,db)

    #print(GetPlayerStatistics(ApplicationID,))



if __name__ == "__main__":
    Main()
