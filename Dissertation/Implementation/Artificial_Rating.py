import pickle,sqlite3,random,pathlib,os
from Essential_Functions import Spacing,CalculateSpacing,PickleLoad,ConnectDatabase,ConvertTupleList,GetRandomPlayerID,NormaliseList,GetGroupedPlayerTanks


# Function to test a variety of artificial rating formulae
def ArtificialRatingTesting(cr,db,GameTanks):
    # Get a random player record
    PlayerID = GetRandomPlayerID(cr,db)
    print("Player ID: " + str(PlayerID))
    cr.execute("""SELECT statistics$all$battles,statistics$all$wins FROM PlayerStatistics WHERE account_id = """ + str(PlayerID))
    PlayerStatistics = list(cr.fetchone())
    
    # Calculate the overall win rate of the player and append it to their statistic list
    PlayerStatistics.append(round((PlayerStatistics[1] / PlayerStatistics[0]), 7))
    print("Battles: " + str(PlayerStatistics[0]) + "    Wins: " + str(PlayerStatistics[1]))
    Spacing(1)

    # Get the corresponding players tanks
    cr.execute("""SELECT tank_id,battles,wins FROM PlayerTanks WHERE account_id = """ + str(PlayerID))
    SQLSelectPlayerTanks = cr.fetchall()
    PlayerTanks = []

    # Output a list of the players tanks and statistics within each tank in a table style format
    print(CalculateSpacing("Tank Name", 30) + CalculateSpacing("Battles",10) + CalculateSpacing("Winrate",12) + "Artificial Rating")
    print("-" * 75)
    # Loop through each tank owned by the player
    for Position in range(len(SQLSelectPlayerTanks)):
        Tank = list(SQLSelectPlayerTanks[Position])
        Tank.append(round((Tank[2] / Tank[1]), 7))
        PlayerTanks.append(Tank)


    # Below is a list of all of the formulae which were tested for the artificial rating generation

##        # Method 1: Percentage of overall battles played in the vehicle (Weighted at 70%) + Vehicle Winrate (Weighted at 30%)
##        ArtificialRating = ((Tank[1] / PlayerStatistics[0]) * 0.7) + (Tank[3] * 0.3)
##        ArtificialRating = round(ArtificialRating * 100, 5)

##        # Method 2: Percentage of overall battles played in the vehicle (Weighted at 50%) + Percentage of overall wins played in the vehicle (Weighted at 50%)
##        ArtificialRating = ((Tank[1] / PlayerStatistics[0]) * 0.5) + ((Tank[2] / PlayerStatistics[1]) * 0.5)
##        ArtificialRating = round(ArtificialRating * 100, 5)

##        # Method 3: Number of wins in the vehicle / Overall wins
##        ArtificialRating = Tank[2] / PlayerStatistics[1]
##        ArtificialRating = round(ArtificialRating * 100, 5)

##        # Method 4: (Overall battles / Number of battles in the vehicle) (Weighted at 50%) * Vehicle winrate
##        ArtificialRating = ((PlayerStatistics[0] / Tank[1]) / 2) * Tank[3]
##        ArtificialRating = round(ArtificialRating, 5)

##        # Method 5: (Number of battles in the vehicle / Overall battles) (Weighted at 50%) * Vehicle winrate
##        ArtificialRating = ((Tank[1] / PlayerStatistics[0]) / 2) * Tank[3]
##        ArtificialRating = round(ArtificialRating * 100, 5)

##        # Method 6: (Number of battles in the vehicle / Overall battles) (Weighted at 35%) * Vehicle winrate (Weighted at 65%)
##        # OR (Percentage of overall games played in the vehicle) (Weighted at 35%) * Vehicle winrate (Weighted at 65%)
##        ArtificialRating = ((Tank[1] / PlayerStatistics[0]) * 0.35) + (Tank[3] * 0.65)
##        ArtificialRating = round(ArtificialRating * 100, 5)

##        # Method 7: (Number of battles in the vehicle / Overall battles) (Weighted at 40%) * Vehicle winrate (Weighted at 60%)
##        # OR (Percentage of overall games played in the vehicle) (Weighted at 40%) * Vehicle winrate (Weighted at 60%)
##        ArtificialRating = ((Tank[1] / PlayerStatistics[0]) * 0.4) * (Tank[3] * 0.6)
##        ArtificialRating = round(ArtificialRating * 100, 5)

        # Method 8 is the final version used for the project

        # Method 8: (Number of battles in the vehicle / Overall battles) (Weighted at 40%) * (Vehicle winrate / Overall winrate) (Weighted at 60%)
        ArtificialRating = ((Tank[1] / PlayerStatistics[0]) * 0.4) * ((Tank[3] / (PlayerStatistics[1] / PlayerStatistics[0])) * 0.6)
        ArtificialRating = round(ArtificialRating * 100, 5)


        # Output the results of the artificial ratings test for the 20 most and least played tanks of the player
        #PlayerTanks[Position].append(ArtificialRating)
        if Position < 20 or Position > len(SQLSelectPlayerTanks) - 20:
            print(CalculateSpacing(GameTanks[str(Tank[0])]["name"],30) + CalculateSpacing(Tank[1],10) + CalculateSpacing(Tank[3], 12) + str(ArtificialRating))


# Function to insert the artifical rating for each record in the PlayerTanks table
def InsertArtificialRating(cr,db):

    # Get the required data for every player within the dataset
    print("Getting PlayerStatistics Records...")
    Spacing(1)
    cr.execute("""SELECT account_id,statistics$all$battles,statistics$all$wins FROM PlayerStatistics""")
    PlayerStatistics = cr.fetchall()

    Grouped_PlayerTanks = (GetGroupedPlayerTanks(cr,db,"Record_ID,account_id,wins,battles"))

    # Loop through every player
    Current = 0
    Total = len(PlayerStatistics)
    print("     -----     Processing     ------")
    for PlayerStatistic in PlayerStatistics:
        RecordIDs = []
        ArtificialRatings = []
        
        PlayerBattles = PlayerStatistic[1]
        PlayerWins = PlayerStatistic[2]
        PlayerWinrate = PlayerWins / PlayerBattles

        PlayerTanks = Grouped_PlayerTanks[PlayerStatistic[0]]

        # For each tank owned by the player, calculate their artificial rating for the tank and append to a list
        for PlayerTank in PlayerTanks:
            TankBattles = PlayerTank[2]
            TankWins = PlayerTank[1]
            TankWinrate = TankWins / TankBattles
            RecordID = PlayerTank[0]

            ArtificialRating = ((TankBattles / PlayerBattles) * 0.4) * ((TankWinrate / PlayerWinrate) * 0.6)

            RecordIDs.append(RecordID)
            ArtificialRatings.append(ArtificialRating)

        # Once all artificial ratings have been calculated for a single player, normalise the list of ratings
        NormalisedRatings = NormaliseList(ArtificialRatings)

        # Insert the artificial rating values into the database
        for Position in range(len(RecordIDs)):
            RecordID = RecordIDs[Position]
            NormalisedRating = NormalisedRatings[Position]
            #cr.execute("""UPDATE PlayerTanks SET artificial_rating = """ + str(NormalisedRating) + """ WHERE Record_ID = """ + str(RecordID))
    
        #db.commit()

        # Output the current progress
        if Current % 100000 == 0:
            print("Rating Progress: " + str(round((Current / Total) * 100, 5)) + "%")
        Current += 1
        
    Spacing(1)
    print("Artificial Ratings Calculation Complete.")


# Empty function created to test isolated lines of code without making the Main function messy
def Testing(cr,db,GameTanks):
    print()    
    


def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    GameTanks = PickleLoad("GameTanks")
    
    Testing(cr,db,GameTanks)

    #ArtificialRatingTesting(cr,db,GameTanks)

    #InsertArtificialRating(cr,db)



if __name__ == "__main__":
    Main()
