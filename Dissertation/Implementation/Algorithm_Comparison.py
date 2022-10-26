import pickle,sqlite3,random,pathlib,os

from Essential_Functions import Spacing,CalculateSpacing,PickleDump,PickleLoad,ConnectDatabase,ConvertTupleList,NormaliseList,GetTankCategories,ConvertVPPString,CreateVPPDictionary,GetGroupedPlayerTanks,CalculateSimilarity,CalculatePercentage


# Function to calculate the unweighted vehicle personality preference for each record in the PlayerStatistics table
def Calculate_Unweighted_VPP(cr,db):
    Grouped_PlayerTanks = (GetGroupedPlayerTanks(cr,db,"tank_id,battles"))
    Spacing(1)

    Current = 0
    Total = len(Grouped_PlayerTanks)
    Unweighted_VPP_Dictionaries =  {}
    # Loop through each player and calculate their unweighted vehicle personality preference
    for PlayerID in Grouped_PlayerTanks:
        PlayerTanks = Grouped_PlayerTanks[PlayerID]

        # Get the totals wins and battles for each vehicle category
        VPPDictionary = CreateVPPDictionary(cr,db,0)
        for PlayerTank in PlayerTanks:
            TankID = PlayerTank[0]
            TankBattles = PlayerTank[1]
            
            cr.execute("""SELECT tier,nation,type FROM GameTanks WHERE tank_id = """ + str(TankID))
            GameTank = cr.fetchone()
            
            TankTier = GameTank[0]
            TankNation = GameTank[1]
            TankType = GameTank[2]

            TierCurrnetBattles = VPPDictionary["tiers"][TankTier]
            NationCurrentBattles = VPPDictionary["nations"][TankNation]
            TypeCurrentBattles = VPPDictionary["types"][TankType]

            VPPDictionary["tiers"][TankTier] = TierCurrnetBattles + TankBattles
            VPPDictionary["nations"][TankNation] = NationCurrentBattles + TankBattles
            VPPDictionary["types"][TankType] = TypeCurrentBattles + TankBattles


        Unweighted_VPP_Dictionaries[PlayerID] = VPPDictionary

        # Output the progress of the process
        if Current % 10000 == 0:
            print("Rating Progress: " + str(round((Current / Total) * 100, 5)) + "%")
        Current += 1

    print("Rating Progress: 100%")
    # Save the resulting unweighted vehicle personality preferences to a file using pickle
    PickleDump("Unweighted_VPPs",Unweighted_VPP_Dictionaries)


# Function to get the resulting recommendations for the WoT RS and MF model with the unweighted vehicle personality preferences
def GetResults(cr,db):
    cr.execute("""SELECT account_id,tank_id,similarity FROM PlayerRecommendations""")
    RS_Recommendations_SQL = cr.fetchall()
    MF_Recommendations = PickleLoad("MatrixFactorization_Recommendations")
    Unweighted_VPP_Dictionaries = PickleLoad("Unweighted_VPPs")
    
    RS_Recommendations = {}
    for Record in RS_Recommendations_SQL:
        PlayerID = Record[0]
        RecommendationAttributes = Record[1:]

        if PlayerID not in RS_Recommendations:
            RS_Recommendations[PlayerID] = []

        CurrentRecommendations = RS_Recommendations[PlayerID]
        CurrentRecommendations.append(RecommendationAttributes)
        RS_Recommendations[PlayerID] = CurrentRecommendations

    return RS_Recommendations, MF_Recommendations, Unweighted_VPP_Dictionaries


# Function to get the list of categories each vehicle in the game belongs to
def GetTankCategories(cr,db):
    cr.execute("""SELECT tank_id,tier,nation,type FROM GameTanks""")
    GameTanks = cr.fetchall()
    TankCategories = {}
    for Record in GameTanks:
        TankCategories[Record[0]] =  Record[1:]
    return TankCategories


# Function to calculate the similarity between given recommendations and unweighted vehicle personality preferences of each player
def CalculateVPPSimilarity(Recommendations,Unweighted_VPP_Dictionaries,TankCategories):
    PlayerAccuracies = []
    TankRatings = []
    for PlayerID in Recommendations:
        # Calculate which categories the current player has the most battles in
        CategoryMaxes = [0,0,0]
        CategoryPosition = 0
        for Category in Unweighted_VPP_Dictionaries[PlayerID]:
            for Value in Unweighted_VPP_Dictionaries[PlayerID][Category]:
                if Unweighted_VPP_Dictionaries[PlayerID][Category][Value] > CategoryMaxes[CategoryPosition]:
                    CategoryMaxes[CategoryPosition] = Unweighted_VPP_Dictionaries[PlayerID][Category][Value]
            CategoryPosition += 1

        # MaxBattlesPerTank represents the number of battles in the most played tier, nation and type for the player
        MaxBattlesPerTank = sum(CategoryMaxes) / len(CategoryMaxes)

        # Find how many batttles the current player has played in each of the recommended tanks categories
        CategoryMatchBattles = []
        for Tank in Recommendations[PlayerID]:
            TankID = Tank[0]
            TankRating = Tank[1]
            CurrentTankTier = TankCategories[TankID][0]
            CurrentTankNation = TankCategories[TankID][1]
            CurrentTankType = TankCategories[TankID][2]
            CategoryMatchBattles.append(sum([Unweighted_VPP_Dictionaries[PlayerID]["tiers"][CurrentTankTier], Unweighted_VPP_Dictionaries[PlayerID]["nations"][CurrentTankNation], Unweighted_VPP_Dictionaries[PlayerID]["types"][CurrentTankType]]) / 3)
            TankRatings.append(TankRating)

        # Calculate the similarity between the recommendations and vehicle personality preference of each player and append the values to a list
        Accuracies = []
        for Value in CategoryMatchBattles:
            Accuracies.append(CalculateSimilarity(MaxBattlesPerTank,Value))

        # Calculate the average similarity for the player and append it to the list of overall player accuracy
        AveragePlayerAccuracy = sum(Accuracies) / len(Accuracies)
        PlayerAccuracies.append(AveragePlayerAccuracy)
        
    return PlayerAccuracies, TankRatings


# Function to calculate a set of metrics for a given list of ratings
def CalculateMetrics(RatingsList):
    # Calculate the min, max and range values
    MinValue = min(RatingsList)
    MaxValue = max(RatingsList)
    Range = CalculatePercentage(MaxValue - MinValue, 2)

    # Calculate the mode and its number of occurences
    MostOccurrence = 0
    MostCommonValue = RatingsList[0]
    for Value in RatingsList:
        CurrentOccurrence = RatingsList.count(Value)
        if CurrentOccurrence > MostOccurrence:
            MostOccurrence = CurrentOccurrence
            MostCommonValue = Value
    MostCommonValue = CalculatePercentage(MostCommonValue, 2)

    # Calculate the median and average values
    RatingsList.sort()
    Median = CalculatePercentage(RatingsList[round(len(RatingsList) / 2)], 2)
    Average = CalculatePercentage(sum(RatingsList) / len(RatingsList), 2)

    return [CalculatePercentage(MinValue, 2), CalculatePercentage(MaxValue, 2), Range, MostCommonValue, MostOccurrence, Median, Average]


# Function to output a set of given metrics
def OutputMetrics(Metrics):
    print("Min Value: " + str(Metrics[0]))
    print("Max Value: " + str(Metrics[1]))
    print("Range of Values: " + str(Metrics[2]))
    print("Mode Value: " + str(Metrics[3]))
    print("Mode Occurrences: " + str(Metrics[4]))
    print("Median Value: " + str(Metrics[5]))
    print("Average Value: " + str(Metrics[6]))


# Function to apply similarity and metric calculations to both the WoT RS and the MF model
def CompareAlgorithms(cr,db):
    # Get the required data to make comparisons
    RS_Recommendations, MF_Recommendations, Unweighted_VPP_Dictionaries = GetResults(cr,db)
    TankCategories = GetTankCategories(cr,db)

    # Run the comparison on the WoT RS and the MF model
    EvaluationSets = [[RS_Recommendations, "RS"], [MF_Recommendations, "MF"]]
    for EvaluationSet in EvaluationSets:
        PlayerAccuracies, TankRatings = CalculateVPPSimilarity(EvaluationSet[0],Unweighted_VPP_Dictionaries,TankCategories)

        # Save the individual player accuracy ratigns and the predicted vehicle ratings
        #PickleDump(EvaluationSet[1] + "_ComparisonResults", [PlayerAccuracies, TankRatings])

        # Calculate and display the metrics for the similarity between recommendations and player vehicle personality preferences
        PlayerAccuracy_Metrics = CalculateMetrics(PlayerAccuracies)
        print("   ---   " + EvaluationSet[1] + " Similarity Metrics   ---")
        OutputMetrics(PlayerAccuracy_Metrics)
        
        Spacing(1)

        # Calculate and display the metrics for predicted vehicle ratings
        TankRatings_Metrics = CalculateMetrics(NormaliseList(TankRatings))
        print("   ---   " + EvaluationSet[1] + " Tank Rating Metrics   ---")
        OutputMetrics(TankRatings_Metrics)

        Spacing(1)

    

    

def Main():
    cr,db = ConnectDatabase("WoTData.db")

    CompareAlgorithms(cr,db)



if __name__ == "__main__":
    Main()
