import pickle,sqlite3,pathlib,os,random,datetime

# Function to print a number of empty lines to create spacing
def Spacing(Lines):
    for x in range(Lines):
        print()


# Add spaces to the end of a string to make the string a specified length
# This is used to output table style data
def CalculateSpacing(Value,LengthRequired):
    String = str(Value)
    Space = LengthRequired - len(String)
    Spacing = " " * Space
    return String + Spacing


# Save data to a pickle file
def PickleDump(Filename,Data):
    # The file path corresponds to the dataset folder withhin the project directory
    FilePath = os.path.join(str(pathlib.Path().resolve())[:-15], "Dataset", Filename)
    File = open(FilePath,"wb")
    pickle.dump(Data,File)
    File.close()


# Load data from a pickle file
def PickleLoad(Filename):
    #print("Loading " + Filename + "...")
    # The file path corresponds to the dataset folder withhin the project directory
    FilePath = os.path.join(str(pathlib.Path().resolve())[:-15], "Dataset", Filename)
    File = open(FilePath,"rb")
    Data = pickle.load(File)
    File.close()
    #print("Loaded " + Filename + ".")
    #Spacing(1)
    return Data


# Function to connect to a database file with a given name
# Returns cr and db as SQL functions to reference the database
def ConnectDatabase(DBName):
    # The file path corresponds to the dataset folder withhin the project directory
    FilePath = os.path.join(str(pathlib.Path().resolve())[:-15], "Dataset", DBName)
    with sqlite3.connect(FilePath) as db:
        cr = db.cursor()
    print("Connected to " + DBName + " Successfully.")
    Spacing(1)
    return cr,db


# Convert a list of tuples with length 1 to a standard array
def ConvertTupleList(List):
    NewList = []
    for Tuple in List:
        NewList.append(Tuple[0])
    return NewList


# Function to output athe information of a specified table in the database
def GetTableInfo(cr, db, Table):
    SQL = """pragma table_info('""" + Table + """');"""
    cr.execute(SQL)
    return cr.fetchall()


# Function to select all the records from a specified table in the database
def SelectAllRecords(cr,db,Table):
    SQL = """SELECT * FROM """ + Table
    cr.execute(SQL)
    return cr.fetchall()


# Function to select a record by a given PlayerID
def SelectRecord(cr,db,Table,PlayerID):
    SQL = """SELECT * FROM """ + Table + """ WHERE account_id = ?"""
    cr.execute(SQL,(PlayerID,))
    return cr.fetchall()


# Function to get 1 return value from an SQL query
def SQLSelectOne(cr,db,SQLString):
    cr.execute(SQLString)
    return cr.fetchone()[0]


# Function to calculate the sum of a given column in a specified table in the database
def CalculateColumnSum(cr,db,Table,Column):
    cr.execute("""SELECT SUM(""" + str(Column) + """) FROM """ + str(Table))
    return cr.fetchone()[0]


# Function to calculate the average of a given column in a specified table in the database
def CalculateColumnAverage(cr,db,Table,Column):
    cr.execute("""SELECT AVG(""" + str(Column) + """) FROM """ + str(Table))
    return cr.fetchone()[0]


# Function to calculate and retreive basic information about the dataset
def GetDataSetInfo(cr,db):
    # Calculate the number of player statistic records
    cr.execute("""SELECT COUNT() FROM PlayerStatistics""")
    PlayerStatisticsCount = cr.fetchone()[0]

    # Calculate the number of player tank records
    cr.execute("""SELECT COUNT() FROM PlayerTanks""")
    PlayerTanksCount = cr.fetchone()[0]

    # Try to load the last player ID retreived from the API
    try:
        CurrentID = PickleLoad("CurrentID")

    # If it fails, due to the file not existing, then create the file with the minimum ID value
    except:
        print("No Data found. Creating default values.")
        Spacing(1)
        CurrentID = 500000000
        PickleDump("CurrentID", CurrentID)
    return PlayerStatisticsCount, PlayerTanksCount, CurrentID


# Function to output the basic information about the dataset
def OutputDataSetInfo(PlayerStatisticsCount, PlayerTanksCount, CurrentID):
    print("          ----------          Information for WoTData          ----------")
    print("CurrentID: " + str(CurrentID))
    print("Number of Records in Player Statistics DataSet: " + str(PlayerStatisticsCount))
    print("Number of Records in Player Tanks DataSet: " + str(PlayerTanksCount))


# Function to calculate and output the basic information about the dataset
def ShowDataSetInfo(cr,db):
    PlayerStatisticsCount, PlayerTanksCount, CurrentID = GetDataSetInfo(cr,db)
    OutputDataSetInfo(PlayerStatisticsCount, PlayerTanksCount, CurrentID)


# Function to get a random PlayerID from the dataset
def GetRandomPlayerID(cr,db):
    cr.execute("""SELECT account_id FROM PlayerStatistics""")
    PlayerIDs = cr.fetchall()
    PlayerIDs = ConvertTupleList(PlayerIDs)
    Random_PlayerID = random.randint(0,len(PlayerIDs) - 1)
    return PlayerIDs[Random_PlayerID]


# Function to normalise a list of values
def NormaliseList(List):
    if len(List) == 1:
        return [1]
    MaxValue = max(List)
    MinValue = min(List)
    NormalisedList = []

    # Try to normalise the list
    try:
        for Value in List:
            NormalisedValue = (Value - MinValue) / (MaxValue - MinValue)
            NormalisedList.append(NormalisedValue)

    # If it fails, output the list and the error
    except Exception as Error:
        print("Current List:")
        print(List)
        Spacing(1)
        print(Error)
        input()

    return NormalisedList


# Function to normalise a list of values in reverse
# This means that the minimum value of the input list becomes 1 and the maximum value of the input list becomes 0
def NormaliseListReverse(List):
    if len(List) == 1:
        return [1]
    MaxValue = max(List)
    MinValue = min(List)
    NormalisedList = []

    # Try to normalise the list in reverse order
    try:
        for Value in List:
            NormalisedValue = abs(MaxValue - Value) / (MaxValue - MinValue)
            NormalisedList.append(NormalisedValue)

    # If it fails, output the list and the error
    except Exception as Error:
        print("Current List:")
        print(List)
        Spacing(1)
        print(Error)
        input()

    return NormalisedList


# Function to get a list of all the tank categories in the dataset
def GetTankCategories(cr,db):
    cr.execute("""SELECT tank_id,tier,nation,type,special_status FROM GameTanks""")
    GameTanks = cr.fetchall()

    TierList = []
    NationList = []
    TypeList = []

    # For each tank in the dataset, if its tier, nation or type is not currently within its respective category list, append it to the list
    for GameTank in GameTanks:
        Tier = GameTank[1]
        Nation = GameTank[2]
        Type = GameTank[3]
        
        if Tier not in TierList:
            TierList.append(Tier)
            
        if Nation not in NationList:
            NationList.append(Nation)
            
        if Type not in TypeList:
            TypeList.append(Type)

    # Sort all of the category lists
    TierList.sort()
    NationList.sort()
    TypeList.sort()

    return TierList, NationList, TypeList


# Function to create the vehicle personality preference dictionary to store the vehicle personality preference of a player
def CreateVPPDictionary(cr,db,DefaultValue):
    TierList, NationList, TypeList = GetTankCategories(cr,db)

    VPPDictionary = {"tiers" : {},
                     "nations": {},
                     "types" : {}}

    # Assign a given default value for each tank category within the dictionary
    for Tier in TierList:
        VPPDictionary["tiers"][Tier] = DefaultValue

    for Nation in NationList:
        VPPDictionary["nations"][Nation] = DefaultValue

    for Type in TypeList:
        VPPDictionary["types"][Type] = DefaultValue

    return VPPDictionary


# Function to convert a vehicle personality preference string into a dictionary
def ConvertVPPString(cr,db,VPPString):
    # Create an empty vehicle personality preference dictionary to store the values from the vehicle personality preference string
    VPPDictionary = CreateVPPDictionary(cr,db,0)
    # Values within the string are seperated using a $ symbol
    VPPStringList = VPPString.split("$")

    # Values are stored in order of all tiers, all nations then all types
    # For each value, convert it to a float and add it to the dictionary
    for Tier in VPPDictionary["tiers"]:
        VPPDictionary["tiers"][Tier] = float(VPPStringList[0])
        VPPStringList = VPPStringList[1:]

    for Nation in VPPDictionary["nations"]:
        VPPDictionary["nations"][Nation] = float(VPPStringList[0])
        VPPStringList = VPPStringList[1:]

    for Type in VPPDictionary["types"]:
        VPPDictionary["types"][Type] = float(VPPStringList[0])
        VPPStringList = VPPStringList[1:]

    return VPPDictionary


# Function to calculate and return a percentage to a given number of decimal places
def CalculatePercentage(Value, DecimalPlaces):
    # If the value is a list, then divide one value by the other to calculate the percentage integer
    # Then apply string formatting for output
    if type(Value) == list:
        return str(round((Value[0] / Value[1]) * 100, DecimalPlaces)) + "%"
    # If the value is not a list then apply string formatting for output
    else:
        return str(round(Value * 100, DecimalPlaces)) + "%"


# Function to get a list of all PlayerTank records and group them by account_id within a dictionary
def GetGroupedPlayerTanks(cr,db,SelectString):
    print("Getting PlayerTanks Records...")
    Spacing(1)

    # Get the selected attributes and the account ID for all player tank records
    cr.execute("""SELECT account_id,""" + SelectString + """ FROM PlayerTanks""")
    SQL_PlayerTanks = cr.fetchall()
    Grouped_PlayerTanks = {}
    
    Total = len(SQL_PlayerTanks)
    Current = 0
    print("Grouping PlayerTanks...")
    # Go through each player tank within the list in reverse order
    for PlayerTank in reversed(SQL_PlayerTanks):
        PlayerID = PlayerTank[0]

        # If the found player ID is not currently in the dictionary, add it to the dictionary with an empty list
        if PlayerID not in Grouped_PlayerTanks:
            Grouped_PlayerTanks[PlayerID] = []

        # Get the saved player tanks for the given player ID and add the current tank record to the list
        CurrentList = Grouped_PlayerTanks[PlayerID]
        CurrentList.append(PlayerTank[1:])
        Grouped_PlayerTanks[PlayerID] = CurrentList
        # Pop a player tank record from the list once saved to the dictionary to reduce memory usage
        SQL_PlayerTanks.pop()

        # Output the progress of the process
        Current += 1
        if Current % 1000000 == 0:
            print("Grouping Progress: " + str(round((Current / Total) * 100, 5)) + "%")
    print("Grouping Progress: 100%")

    return Grouped_PlayerTanks


# Function to get a list of specific PlayerTank records according to a given list of account IDs and group them by account_id within a dictionary
def GetSpecificGroupedPlayerTanks(cr,db,SelectString,PlayerIDs,Target_PlayerID):
##    print("Grouping PlayerTanks...")
##    Spacing(1)

    # Get the selected attributes and the account ID for the player tank records of the given players
    PlayerIDs.append(Target_PlayerID)
    PlayerIDs_String = ""
    for PlayerID in PlayerIDs:
        PlayerIDs_String = PlayerIDs_String + str(PlayerID) + ","
    PlayerIDs_String = PlayerIDs_String[:-1]
    cr.execute("""SELECT account_id,""" + SelectString + """ FROM PlayerTanks WHERE account_id IN (""" + PlayerIDs_String + """)""")
    SQL_PlayerTanks = cr.fetchall()

    Grouped_PlayerTanks = {}
    Target_PlayerTanks = []
    # Go through each player tank within the list in reverse order
    for PlayerTank in reversed(SQL_PlayerTanks):
        PlayerID = PlayerTank[0]

        # If the tank record belongs to the target player, pop the record and save it to a seperate list
        if PlayerID == Target_PlayerID:
            CurrentPlayerTank = SQL_PlayerTanks.pop()
            Target_PlayerTanks.append(CurrentPlayerTank[1:])

        else:
            # If the found player ID is not currently in the dictionary, add it to the dictionary with an empty list
            if PlayerID not in Grouped_PlayerTanks:
                Grouped_PlayerTanks[PlayerID] = []

            # Get the saved player tanks for the given player ID and add the current tank record to the list
            CurrentList = Grouped_PlayerTanks[PlayerID]
            CurrentList.append(PlayerTank[1:])
            Grouped_PlayerTanks[PlayerID] = CurrentList
            # Pop a player tank record from the list once saved to the dictionary to reduce memory usage
            SQL_PlayerTanks.pop()

    return Grouped_PlayerTanks,Target_PlayerTanks


# Function to calculate the similarity of two values
def CalculateSimilarity(TargetValue, TestValue):
    # Sort the values within a list
    Values = [TargetValue, TestValue]
    Values.sort()

    # If both values are 0, then they are given a similarity rating of 100%
    if float(TargetValue) == 0.0 and float(TestValue) == 0.0:
        return 1
    # Else, if either of the values are 0 then they are given a similarity rating of 0%
    elif 0 in Values or 0.0 in Values:
        return 0
    # Else, divide the smaller value by the larger value to calculate the similarity rating
    else:
        Similarity = Values[0] / Values[1]
        return Similarity


# Function to return the current UTC time.
def GetCurrentTime():
    return str(datetime.datetime.utcnow())[11:]


# Function to calculate the difference between the current time and the start time in seconds
def CalculateTime(StartTime):
    FinishTime = GetCurrentTime()
    # Calculate the number of seconds, minutes and hours since the start time
    # These may result in negative numbers if either a minute or an hour has gone by
    Seconds = float(FinishTime[6:]) - float(StartTime[6:])
    Minutes = float(FinishTime[3:5]) - float(StartTime[3:5])
    Hours = float(FinishTime[:2]) - float(StartTime[:2])
    # Convert all of the values to seconds, mitigating the issue of negatives
    Minutes += (Hours * 60)
    Seconds += (Minutes * 60)
    return Seconds


