import pickle,sqlite3,pathlib,os
from Essential_Functions import Spacing,CalculateSpacing,PickleDump,PickleLoad,ConnectDatabase,ConvertTupleList
from WG_API import CalculateMissingTankRecords

# Function to delete the records from tables which cause issues
def DeleteRedundantRecords(cr,db,GameTanks):
    # Calculate the records which contain foreign key references with no corresponding primary key
    TankIDs_NotInGameTanks,TankIDs_NotInWoTDB,DeletePlayerIDs = CalculateMissingTankRecords(cr,db,GameTanks)
    Spacing(1)

    # Delete the redundant records within the player tanks and player statistics tables
    print("Deleting " + str(len(DeletePlayerIDs)) + " Player Records...")
    DeletePlayerIDs = tuple(DeletePlayerIDs)
    print("Deleting records from PlayerTanks...")
    SQLString = """DELETE FROM PlayerTanks WHERE account_id IN """ + str(DeletePlayerIDs)
    cr.execute(SQLString)
    print("Deleting records from PlayerStatistics...")
    SQLString = """DELETE FROM PlayerStatistics WHERE account_id IN """ + str(DeletePlayerIDs)
    cr.execute(SQLString)
    db.commit()

    # Delete the redundant game tanks records
    print("Deleting " + str(len(TankIDs_NotInWoTDB)) + " Tank Records...")
    for TankID in TankIDs_NotInWoTDB:
        del GameTanks[str(TankID)]
    PickleDump("GameTanks",GameTanks)
    
    print("Deletion Completed.")


# Function to delete player records which are below the minimum threshold (100)
def DeleteThresholdRecords(cr,db):
    # Getting the ID values of the players with under 100 battles
    PlayerThreshold = 100
    SQLString = """SELECT account_id FROM PlayerStatistics WHERE statistics$all$battles < """ + str(PlayerThreshold) + """ ORDER BY account_id"""
    cr.execute(SQLString)
    
    # Calculate the number of players which will be deleted
    UnusablePlayerIDs = tuple(ConvertTupleList(cr.fetchall()))
    UnusablePlayers = len(UnusablePlayerIDs)
    print("Found " + str(UnusablePlayers) + " Unusable Players.")
    Spacing(1)

    # Deleting the unusable players tank and statistic records
    print("Deleting records from PlayerTanks...")
    SQLString = """DELETE FROM PlayerTanks WHERE account_id IN """ + str(UnusablePlayerIDs)
    cr.execute(SQLString)
    print("Deleting records from PlayerStatistics...")
    SQLString = """DELETE FROM PlayerStatistics WHERE account_id IN """ + str(UnusablePlayerIDs)
    cr.execute(SQLString)
    db.commit()


# Function to calculate remaining records pre-deletion and then perform the deletion
def ReduceDataSet(cr,db):
    # Get the number of all players within the dataset
    cr.execute("""SELECT COUNT() FROM PlayerStatistics""")
    PlayerStatisticsCount = cr.fetchone()[0]

    # Get the number of players which are above the threshold
    PlayerIDThreshold = #
    cr.execute("""SELECT COUNT() FROM PlayerStatistics WHERE account_id >= """ + str(PlayerIDThreshold))
    DeletionRecords = cr.fetchone()[0]

    # Output relevant information regarding the threshold and player counts
    print("Total Player Records: " + str(PlayerStatisticsCount))
    print("Player ID Threshold: " + str(PlayerIDThreshold))
    print("Remaining Records: " + str(PlayerStatisticsCount - DeletionRecords))

    # Get input which dictates if the deletion should continue
    Choice = input("Delete Records (Y/N)? : ").upper()
    # If yes, delete the player records from the player statistics and player tanks tables
    if Choice == "Y":
        Spacing(1)
        print("Deleting PlayerStatistics...")
        cr.execute("""DELETE FROM PlayerStatistics WHERE account_id >= """ + str(PlayerIDThreshold))
        print("Deleting PlayerTanks...")
        cr.execute("""DELETE FROM PlayerTanks WHERE account_id >= """ + str(PlayerIDThreshold))
        db.commit()

    Spacing(1)
    # Get the input which dictates if the vacuum should be applied after the deletion
    Choice = input("Perform Vacuum (Y/N)? : ").upper()
    # If yes, apply the vacuum
    if Choice == "Y":
        cr.execute("VACUUM")

    # Commit the changes and close the database
    db.commit()
    cr.close()
        

def Main():
    cr,db = ConnectDatabase("WoTData.db")

    #GameTanks = PickleLoad("GameTanks")

    ReduceDataSet(cr,db)    


Main()
