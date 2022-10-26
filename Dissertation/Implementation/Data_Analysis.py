import pickle,sqlite3,pathlib,os,random
from Essential_Functions import Spacing,CalculateSpacing,PickleLoad,ConnectDatabase,ConvertTupleList,GetTableInfo,SelectAllRecords,SelectRecord,SQLSelectOne,GetDataSetInfo,OutputDataSetInfo,ShowDataSetInfo,GetRandomPlayerID,CalculateColumnSum,CalculateColumnAverage,GetTankCategories,CreateVPPDictionary,ConvertVPPString,CalculatePercentage


# Function to calculate how many records are usable from the dataset according to given threshold parameters and output the results
def CalculateUsableRecords(cr,db,PlayerThreshold):
    cr.execute("""SELECT COUNT() FROM PlayerStatistics""")
    PlayerStatisticsCount = cr.fetchone()[0]

    # Get the ID values of unusable player records from the players according to a given threshold
    # ID values are required to perform deletion
    SQLString = """SELECT account_id FROM PlayerStatistics WHERE statistics$all$battles < """ + str(PlayerThreshold) + """ ORDER BY account_id"""
    cr.execute(SQLString)
    UnusablePlayerIDs = ConvertTupleList(cr.fetchall())
    UnusablePlayers = len(UnusablePlayerIDs)
    print("Found Unusable Players.")
    Spacing(1)

    # Get the number of usable player records from the players according to a given threshold
    SQLString = """SELECT COUNT() FROM PlayerStatistics WHERE statistics$all$battles >= """ + str(PlayerThreshold) + """ ORDER BY account_id"""
    cr.execute(SQLString)
    UsablePlayers = cr.fetchone()[0]
    print("Found Usable Players.")
    Spacing(1)

    # Output information regarding how many records are usable according to the given threshold values
    print("     -----     Threshold " + str(PlayerThreshold) + "+ Battles     -----")
    print("Total Players: " + str(PlayerStatisticsCount))
    print("Number of Usable Records: " + str(UsablePlayers))
    print("Number of Unusable Records: " + str(UnusablePlayers))
    print("Percentage of Dataset Usable: " + str(round((UsablePlayers / PlayerStatisticsCount) * 100, 2)) + "%")
    print("Percentage of Dataset Unusable: " + str(round((UnusablePlayers / PlayerStatisticsCount) * 100, 2)) + "%")

    return UnusablePlayerIDs


# Function to calculate an average of a column within the dataset
def CalculateAverage(cr,db,Table,Column):
    cr.execute("""SELECT """ + str(Column) + """ FROM """ + str(Table))
    AllValues = ConvertTupleList(cr.fetchall())
    return sum(AllValues) / len(AllValues)


# Function to output the list of tanks a given player has played with their basic statistics
def OutputPlayerOverview(cr,db,PlayerID):
    # Get the statistics and tanks of the target player
    print("Getting " + str(PlayerID) + " Statistics and Tanks...")
    Spacing(1)
    cr.execute("""SELECT statistics$all$battles, statistics$all$wins, vehicle_personality_preference FROM PlayerStatistics WHERE account_id = """ + str(PlayerID))
    PlayerStatistic = cr.fetchone()
    cr.execute("""SELECT tank_id,wins,battles,artificial_rating FROM PlayerTanks WHERE account_id = """ + str(PlayerID))
    PlayerTanks = cr.fetchall()

    # Output basic statistics of the target player
    print("   ---   PlayerStatistics for Player: " + str(PlayerID) + "   ---")
    Spacing(1)
    print("Overall Battles: " + str(PlayerStatistic[0]))
    print("Overall Wins:    " + str(PlayerStatistic[1]))
    print("Overall Winrate: " + CalculatePercentage([PlayerStatistic[1], PlayerStatistic[0]], 2))
    Spacing(2)
                                    

    # Output the list of vehicles owned by the target player and their statistics
    print("   ---   PlayerTanks for Player: " + str(PlayerID) + "   ---")
    Spacing(1)

    # Values are outputted in a table style, SpacingValues represents the number of spaces between each column
    SpacingValues = [18, 8, 12, 15, 8, 10, 11, 20]
    Titles = ["Tank Name:", "Tier:", "Nation:", "Type:", "Wins:", "Battles:", "Winrate:", "Artificial Rating:"]
    TableTitle = ""

    # Output the column titles of the table
    for Position in range(len(SpacingValues)):
        TableTitle += CalculateSpacing(Titles[Position], SpacingValues[Position])
    print(TableTitle)

    # Loop through each of the target player's tanks
    for PlayerTank in PlayerTanks:

        # Get the statistics of the tank itself
        cr.execute("""SELECT short_name,tier,nation,type FROM GameTanks WHERE tank_id = """ + str(PlayerTank[0]))
        TankCategories = cr.fetchone()

        # Create a string to represent the row of data and output it
        CurrentTankString = ""
        TankDetails = [TankCategories[0], TankCategories[1], TankCategories[2], TankCategories[3], PlayerTank[1], PlayerTank[2], CalculatePercentage([PlayerTank[1], PlayerTank[2]], 2), CalculatePercentage(PlayerTank[3], 2)]
        for Position in range(len(SpacingValues)):
            CurrentTankString += CalculateSpacing(TankDetails[Position], SpacingValues[Position])
        print(CurrentTankString)




# Empty function created to test isolated lines of code without making the Main function messy
def Testing(cr,db):
    print()
    



def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    #Testing(cr,db)

    #CalculateUsableRecords(cr,db,1000)

    #CalculateUsableGraph(cr,db)

    ShowDataSetInfo(cr,db)

##    PlayerID = 
##    OutputPlayerOverview(cr,db,PlayerID)



if __name__ == "__main__":  
    Main()






