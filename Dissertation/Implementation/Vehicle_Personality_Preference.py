import pickle,sqlite3,random,pathlib,os
from Essential_Functions import Spacing,CalculateSpacing,PickleLoad,ConnectDatabase,ConvertTupleList,GetRandomPlayerID,NormaliseList,GetTankCategories,ConvertVPPString,CreateVPPDictionary,GetGroupedPlayerTanks


# Function to convert a VPP dictionary into a string to be stored in a database
def ConvertVPPDictionary(VPPDictionary):
    VPPString = ""
    for Tier in VPPDictionary["tiers"]:
        VPPString = VPPString + str(VPPDictionary["tiers"][Tier]) + "$"
    for Nation in VPPDictionary["nations"]:
        VPPString = VPPString + str(VPPDictionary["nations"][Nation]) + "$"
    for Type in VPPDictionary["types"]:
        VPPString = VPPString + str(VPPDictionary["types"][Type]) + "$"
    # Remove the additional $ symbol at the end of the string
    return VPPString[:-1]


# Function to insert the vehicle personality preference for each record in the PlayerStatistics table
def InsertVPP(cr,db):
    print("Getting PlayerStatistics Records...")
    Spacing(1)
    # Get all of the player statistics from the dataset
    cr.execute("""SELECT account_id,statistics$all$battles,statistics$all$wins FROM PlayerStatistics""")
    PlayerStatistics = cr.fetchall()

    # Group the players tanks into a dictionary via their player ID
    Grouped_PlayerTanks = (GetGroupedPlayerTanks(cr,db,"tank_id,wins,battles"))
    Spacing(1)

    Current = 0
    Total = len(PlayerStatistics)

    # Loop through each player statistic in the dataset
    print("Calculating Vehicle Personality Preferences...")
    Spacing(1)
    for PlayerStatistic in PlayerStatistics:
        # Define variable names for specific values to make code easier to read
        PlayerID = PlayerStatistic[0]
        PlayerBattles = PlayerStatistic[1]
        PlayerWins = PlayerStatistic[2]
        PlayerWinrate = PlayerWins / PlayerBattles
        PlayerTanks = Grouped_PlayerTanks[PlayerID]

        # Create an empty vehicle personality preference dictionary
        VPPDictionary = CreateVPPDictionary(cr,db,[0,0])
        # Loop through each tank of the current player
        for PlayerTank in PlayerTanks:
            TankID = PlayerTank[0]
            TankWins = PlayerTank[1]
            TankBattles = PlayerTank[2]

            # Get the category attributes of the current tank
            cr.execute("""SELECT tier,nation,type FROM GameTanks WHERE tank_id = """ + str(TankID))
            GameTank = cr.fetchone()
            
            TankTier = GameTank[0]
            TankNation = GameTank[1]
            TankType = GameTank[2]

            # Get the current data of the current tank's categories from the vehicle personality preference dictionary
            TierCurrnetWins = VPPDictionary["tiers"][TankTier][0]
            TierCurrnetBattles = VPPDictionary["tiers"][TankTier][1]
            NationCurrentWins = VPPDictionary["nations"][TankNation][0]
            NationCurrentBattles = VPPDictionary["nations"][TankNation][1]
            TypeCurrentWins = VPPDictionary["types"][TankType][0]
            TypeCurrentBattles = VPPDictionary["types"][TankType][1]

            # Add the current tank's statistics from the current player to the player's vehicle personality preference dictionary
            VPPDictionary["tiers"][TankTier] = [TierCurrnetWins + TankWins, TierCurrnetBattles + TankBattles]
            VPPDictionary["nations"][TankNation] = [NationCurrentWins + TankWins, NationCurrentBattles + TankBattles]
            VPPDictionary["types"][TankType] = [TypeCurrentWins + TankWins, TypeCurrentBattles + TankBattles]
            

        # Calculate the artificial rating for each category within the player's vehicle personality preference
        # Repeat the process for each tier, nation and type
        # If the player has no battles in the category, the artificial rating becomes 0
        VPPTierList = []
        for Tier in VPPDictionary["tiers"]:
            TierWins = VPPDictionary["tiers"][Tier][0]
            TierBattles = VPPDictionary["tiers"][Tier][1]
            if TierBattles == 0:
                ArtificialRating = 0
            else:
                TierWinrate = TierWins / TierBattles
                ArtificialRating = ((TierBattles / PlayerBattles) * 0.4) * ((TierWinrate / PlayerWinrate) * 0.6)
            VPPDictionary["tiers"][Tier] = ArtificialRating
            VPPTierList.append(ArtificialRating)

        VPPNationList = []
        for Nation in VPPDictionary["nations"]:
            NationWins = VPPDictionary["nations"][Nation][0]
            NationBattles = VPPDictionary["nations"][Nation][1]
            if NationBattles == 0:
                ArtificialRating = 0
            else:
                NationWinrate = NationWins / NationBattles
                ArtificialRating = ((NationBattles / PlayerBattles) * 0.4) * ((NationWinrate / PlayerWinrate) * 0.6)
            VPPDictionary["nations"][Nation] = ArtificialRating
            VPPNationList.append(ArtificialRating)

        VPPTypeList = []
        for Type in VPPDictionary["types"]:
            TypeWins = VPPDictionary["types"][Type][0]
            TypeBattles = VPPDictionary["types"][Type][1]
            if TypeBattles == 0:
                ArtificialRating = 0
            else:
                TypeWinrate = TypeWins / TypeBattles
                ArtificialRating = ((TypeBattles / PlayerBattles) * 0.4) * ((TypeWinrate / PlayerWinrate) * 0.6)
            VPPDictionary["types"][Type] = ArtificialRating
            VPPTypeList.append(ArtificialRating)


        # Normalise the list of artificial ratings for the list of tiers, nations and types
        VPPMinTier = min(VPPTierList)
        VPPMaxTier = max(VPPTierList)
        for Tier in VPPDictionary["tiers"]:
            ArtificialRating = VPPDictionary["tiers"][Tier]
            NormalisedRating = (ArtificialRating - VPPMinTier) / (VPPMaxTier - VPPMinTier)
            VPPDictionary["tiers"][Tier] = NormalisedRating

        VPPMinNation = min(VPPNationList)
        VPPMaxNation = max(VPPNationList)
        for Nation in VPPDictionary["nations"]:
            ArtificialRating = VPPDictionary["nations"][Nation]
            NormalisedRating = (ArtificialRating - VPPMinNation) / (VPPMaxNation - VPPMinNation)
            VPPDictionary["nations"][Nation] = NormalisedRating

        VPPMinType = min(VPPTypeList)
        VPPMaxType = max(VPPTypeList)
        for Type in VPPDictionary["types"]:
            ArtificialRating = VPPDictionary["types"][Type]
            NormalisedRating = (ArtificialRating - VPPMinType) / (VPPMaxType - VPPMinType)
            VPPDictionary["types"][Type] = NormalisedRating


        # Convert the VPPDictionary into a VPPString to store in the database
        VPPString = ConvertVPPDictionary(VPPDictionary)
        cr.execute("""UPDATE PlayerStatistics SET vehicle_personality_preference = ? WHERE account_id = ?""", (VPPString, PlayerID))
        db.commit()
        
        # Output the current progress of the process
        if Current % 10000 == 0:
            print("Rating Progress: " + str(round((Current / Total) * 100, 5)) + "%")
        Current += 1

    Spacing(1)
    print("Vehicle Personality Preference Calculation Complete.")





# Empty function created to test isolated lines of code without making the Main function messy
def Testing(cr,db):
    print()



def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    Testing(cr,db)

    #InsertVPP(cr,db)



if __name__ == "__main__":
    Main()
