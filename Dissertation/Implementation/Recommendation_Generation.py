import pickle,sqlite3,random,pathlib,os,datetime
from Essential_Functions import Spacing,CalculateSpacing,PickleLoad,PickleDump,ConnectDatabase,ConvertTupleList,GetRandomPlayerID,NormaliseList,NormaliseListReverse,GetTankCategories,ConvertVPPString,CreateVPPDictionary,CalculatePercentage,GetSpecificGroupedPlayerTanks,CalculateSimilarity,GetCurrentTime,CalculateTime

import tkinter,urllib.request,io
from PIL import Image,ImageTk


# Function to get all PlayerStatistics from the dataset
def GetPlayerStatistics(cr,db):
    print("Getting PlayerStatistics...")
    Spacing(1)
    cr.execute("""SELECT * FROM PlayerStatistics""")
    PlayerStatistics = cr.fetchall()
    return PlayerStatistics


# Function to get the PlayerID of the target player as input from the user
def GetTargetPlayer(cr,db):
    # While loop the input to ensure valid input, if the input does not mean requirements then the loop runs again
    Choosing = True
    while Choosing == True:
        # Try to get an input and perform required processes
        try:
            # Get user choice
            print("Generating a recommendation requires a target player.")
            print("Please input either a PlayerID or 'random' to get a random PlayerID: ")
            Choice = str(input())

            # If choice is random, get a random player ID
            if Choice.upper() == "RANDOM":
                PlayerID = GetRandomPlayerID(cr,db)
                print("Randomly Selected PlayerID: {0}".format(PlayerID))
            # Else, the choice represents the player ID and therefore is converted to an integer
            else:
                PlayerID = int(Choice)
            Spacing(1)
            
            # Stop the loop
            Choosing = False

        # If an error is found, output error message
        except:
            print("Error! Please provide a valid input.")
            Spacing(1)

    return PlayerID


# Function to get input from the user to determine if the recommendations should include special vehicles
def GetSpecialVehicleChoice():
    print("Would you like to include Special vehicles in the recommendations?")
    SpecialVehicleChoice = input("Please input Yes (Y) or No (N): ")
    Spacing(1)
    return SpecialVehicleChoice


# Function to get the special status of every vehicle
def GetSpecialStatus(cr,db):
    # Get the special status of all tanks in the dataset
    cr.execute("""SELECT tank_id,special_status FROM GameTanks""")
    GameTanks_SQL = cr.fetchall()
    # Group the special statuses by tank IDs in a dictionary to make lookup easier and faster
    GameTanks_SpecialStatus = {}
    for GameTank in GameTanks_SQL:
        GameTanks_SpecialStatus[GameTank[0]] = GameTank[1]
    return GameTanks_SpecialStatus


# Function to remove special vehicles from the given list of vehicles
def RemoveSpecialVehicles(cr,db,VehicleList):
    GameTanks_SpecialStatus = GetSpecialStatus(cr,db)
    OutputVehicleList = []
    # Loop through each vehicle in the list
    for Vehicle in VehicleList:
        # Position of the tank ID depends on the data type of each tank value
        if type(Vehicle) in [list, tuple]:
            TankID = Vehicle[0]
        else:
            TankID = Vehicle

        # If the tank is not a special vehicle, append it to the new list
        if GameTanks_SpecialStatus[TankID] != 1:
            OutputVehicleList.append(Vehicle)

    return OutputVehicleList


# Function to remove unowned vehicles from the given list of vehicles
def GetUnownedVehiclesData(cr,db,TargetPlayer_UnownedTankIDs,VehicleList):
    OutputVehicleList = []
    # Loop through the list of all tanks in the dataset
    for Vehicle in VehicleList:
        # Position of the tank ID depends on the data type of each tank value
        if type(Vehicle) in [list, tuple]:
            TankID = Vehicle[0]
        else:
            TankID = Vehicle

        # If the current tank is unowned, append it to the new list
        if TankID in TargetPlayer_UnownedTankIDs:
            OutputVehicleList.append(Vehicle)

    return OutputVehicleList


# Function to extract the target player from the list of PlayerStatistics
def ExtractPlayerStatistic(Target_PlayerID,PlayerStatistics):
    # Loop through all players within the player statistics
    for Position in range(len(PlayerStatistics)):
        # If the target player is found, pop the record from the overall list and stop the loop
        if PlayerStatistics[Position][0] == Target_PlayerID:
            Target_PlayerStatistics = PlayerStatistics.pop(Position)
            break
    return PlayerStatistics,Target_PlayerStatistics


# Function to calculate which vehicles the target player does not own
def GetUnownedVehicleIDs(cr,db,Target_PlayerID):
    # Get all of the target player's played vehicles
    cr.execute("""SELECT tank_id FROM PlayerTanks WHERE account_id = ?""", (Target_PlayerID,))
    PlayerTanks = cr.fetchall()
    PlayerTanks = ConvertTupleList(PlayerTanks)

    # Get a list of all of the tanks in the dataset
    cr.execute("""SELECT tank_id FROM GameTanks""")
    GameTanks = cr.fetchall()
    GameTanks = ConvertTupleList(GameTanks)

    TargetPlayer_UnownedTankIDs = []
    # Loop through each of the tanks in the dataset
    for GameTank in GameTanks:
        # If the tank is notowned by the player, append it to a list
        if GameTank not in PlayerTanks:
            TargetPlayer_UnownedTankIDs.append(GameTank)

    return TargetPlayer_UnownedTankIDs


# Function to calculate the most similar 50 players to the target player
def CalculateTopSimilarityPlayers(cr,db,PlayerStatistics,Target_PlayerStatistics):
    # Define variable names for specific values to make code easier to read
    Compare_Target_PlayerStatistics = Target_PlayerStatistics[1:]
    # Convert the vehicle personality preference of the target player from a string to a list
    Target_VPPString = Compare_Target_PlayerStatistics[43]
    Target_VPPList = Target_VPPString.split("$")
    Target_VPPList = list(map(float, Target_VPPList))
    TotalVPPValues = len(Target_VPPList)
    TotalPlayerStatistics = len(PlayerStatistics)

    # Define the weighting for specific attributes when calculating the similarity ratings
    # Vehicle personality preference and clan ID are weighted differently to other attributes
    VPP_Weight = 0.05
    Clan_Weight = 0.05
    # Define the weighting for each value within the vehicle personality preference
    IndividualVPPValueWeight = 1 / TotalVPPValues
    # Define the weighting values for all remaining player attributes
    IndividualPlayerStatisticValues = len(Compare_Target_PlayerStatistics)
    IndividualPlayerStatisticWeight = (1 - VPP_Weight - Clan_Weight) / (IndividualPlayerStatisticValues - 2)

    # Array of arrays, each inner array consists of the Player ID and the percentage similarity to the target play
    PlayerSimilarties = []
    # Loop through the position within the list of player statistics
    for Position in range(TotalPlayerStatistics):
        # Define the current player statistics to compare
        Current_PlayerStatistics = PlayerStatistics[Position]
        Compare_Current_PlayerStatistics = Current_PlayerStatistics[1:]

        CurrentSimilarity = 0
        # Loop through each attribute of the current player
        for Position in range(IndividualPlayerStatisticValues):

            # If 25 attributes of the current player have been compared and resulted in a similarity below 20%, stop comparing as they are considered irrelevant
            if Position == 25 and CurrentSimilarity < 0.2:
                break
            
            # If the position is 4 which corresponds to the position of the clan ID, calculate similarity differently
            elif Position == 4:
                # If the target and current player are in the same clan, similarity is 100% for clan ID and is added to the similarity of the current player after being multiplied by its weighting value
                if Compare_Target_PlayerStatistics[Position] == Compare_Current_PlayerStatistics[Position]:
                    CurrentSimilarity = CurrentSimilarity + (1 * Clan_Weight)
                # Else, if the target and current player are both not in a clan, similarity is 50% for clan ID and is added to the similarity of the current player after being multiplied by its weighting value
                elif Compare_Target_PlayerStatistics[Position] != "None" and Compare_Current_PlayerStatistics[Position] != "None":
                    CurrentSimilarity = CurrentSimilarity + (0.5 * Clan_Weight)
                    
            # If the position is 4 which corresponds to the position of the vehicle personality preference, calculate similarity differently  
            elif Position == 43:

                # If the Player's current similarity is above 50%, continue calculating their values
                if CurrentSimilarity > 0.5:

                    # Convert the current players vehicle personality preference into a list
                    Current_VPPString = Compare_Current_PlayerStatistics[Position]
                    Current_VPPList = Current_VPPString.split("$")
                    Current_VPPList = list(map(float, Current_VPPList))
                    VPPSimilarity = 0
                    # Loop through each value within the vehicle personality preference
                    for VPP_Position in range(TotalVPPValues):
                        # Calculate the similarity between the target and current player vehicle personality preference attribute, multiply it by the weight and add it to the vehicle personality preference similarity
                        VPPSimilarity = VPPSimilarity + (CalculateSimilarity(Target_VPPList[VPP_Position], Current_VPPList[VPP_Position]) * IndividualVPPValueWeight)
                    # Multiply the overall vehicle personality preference similarity by its weighting and add it to the current player similarity
                    CurrentSimilarity = CurrentSimilarity + (VPPSimilarity * VPP_Weight)

                # Else, stop comparing similarity as they are considered irrelevant
                else:
                    break

            # Else, if values are in the specified positions, their values must be equal or they are considered to have 0% similarity
            elif Position in [13, 19, 23]:
                # If the attribute of the target and current player is the same, the attribute similarity is 100% and is multipled by weighting before being adding to the current player similarity
                if Compare_Target_PlayerStatistics[Position] == Compare_Current_PlayerStatistics[Position]:
                    CurrentSimilarity = CurrentSimilarity + (1 * IndividualPlayerStatisticWeight)
                    
            # Else, the same similarity calculations are run on all other fields as they are either floats or integers with respective weighting applied before being added to the current player similarity
            else:
                CurrentSimilarity = CurrentSimilarity + (CalculateSimilarity(Compare_Target_PlayerStatistics[Position], Compare_Current_PlayerStatistics[Position]) * IndividualPlayerStatisticWeight)

        # Create a list containing the current player ID and their calculated similarity to the target player
        # Add this list to the overall list of player similarities
        CurrentPair = [Current_PlayerStatistics[0], CurrentSimilarity]
        PlayerSimilarties.append(CurrentPair)

    # Sort the list of player similarities in descending order and keep only the top 50 results
    PlayerSimilarties.sort(key = lambda ComparisonValue: ComparisonValue[1], reverse = True)
    TopPlayerSimilarities = PlayerSimilarties[:50]
    return TopPlayerSimilarities


# Function to calculate the average artificial rating of the most similar players to the target player for each unowned vehicle of the target player
def CalculatePlayerSimilarityVehicles(cr,db,Target_PlayerID,TargetPlayer_UnownedTankIDs,TopPlayerSimilarities):
    # Extract the player IDs from the top 50 similarities
    TopPlayerSimilarityIDs = [Pair[0] for Pair in TopPlayerSimilarities]
    # Get the player tanks of the most similar players and the target player in a dictionary format
    PlayerTanks,Target_PlayerTanks = GetSpecificGroupedPlayerTanks(cr,db,"tank_id,wins,battles,artificial_rating",TopPlayerSimilarityIDs,Target_PlayerID)
    
    # Dictionary, for each unowned vehicle ID, calculate the average AR of the most similar players for that vehicle
    TopPlayerVehicleSimilarities = {}
    TotalSimilarPlayers = len(TopPlayerSimilarities)
    # Loop through each unowned tank of the target player
    for UnownedTankID in TargetPlayer_UnownedTankIDs:
        TopPlayerVehicleSimilarities[UnownedTankID] = []

    # Loop through each most similar player to the target player
    # For each similar player, calculate their AR * their percentage similarity for each unowned vehicle
    for PlayerSet in TopPlayerSimilarities:
        # Define variable names for specific values to make code easier to read
        CurrentPlayerID = PlayerSet[0]
        CurrentPlayerSimilarity = PlayerSet[1]
        CurrentPlayerTanks = PlayerTanks[CurrentPlayerID]

        # Loop through each tank of the current player
        for CurrentPlayerTank in CurrentPlayerTanks:
            CurrentTankID = CurrentPlayerTank[0]

            # If the current tank is unowned by the target player, multiply the current player's artificial rating for the current tank by their similarity to the target player
            # Then add the resulting value to the list of weighted artificial ratings for the current tank
            if CurrentTankID in TargetPlayer_UnownedTankIDs:
                CurrentPlayerTankAR = CurrentPlayerTank[3]
                CurrentARList = TopPlayerVehicleSimilarities[CurrentTankID]
                CurrentARList.append(CurrentPlayerTankAR * CurrentPlayerSimilarity)
                TopPlayerVehicleSimilarities[CurrentTankID] = CurrentARList

    # Calcualte the average percentage of each unowned tank
    # Loop through each unowned tank ID through the newly created dictionary which contains the artificial rating values from similar players
    for TankID in TopPlayerVehicleSimilarities:
        # Calculate the average artificial rating of each tank in the dictionary
        PercentageList = TopPlayerVehicleSimilarities[TankID]
        CurrentTotalPercentages = len(PercentageList)
        # If none of the most similar players to the target player have played the current tank, it's average artificial rating becomes 0
        if CurrentTotalPercentages == 0:
            CurrentAveragePercentage = 0
        # Else, calculate the average artificial rating
        else:
            CurrentAveragePercentage = sum(PercentageList) / CurrentTotalPercentages

        # Calculate the number of most similar players to the target player which have not played the current tank
        MissingPercentages = TotalSimilarPlayers - CurrentTotalPercentages
        # For each most similar player which has not played the current tank, fill in their empty artificial rating in the list with half of the current average artificial rating
        PercentagesInsert = [CurrentAveragePercentage * 0.5] * MissingPercentages
        PercentageList.extend(PercentagesInsert)
        # Calculate the new average artificial rating for the current tank and save the value
        NewAveragePercentage = sum(PercentageList) / len(PercentageList)
        TopPlayerVehicleSimilarities[TankID] = NewAveragePercentage

    TankIDs = []
    AllPlayerVehicleSimilarities = []
    # Seperate the dictionary of artificial ratings into two lists, one for tank IDs and one for average artificial ratings
    for TankID in TopPlayerVehicleSimilarities:
        TankIDs.append(TankID)
        AllPlayerVehicleSimilarities.append(TopPlayerVehicleSimilarities[TankID])
        
    # Normalise the list of average artificial ratings 
    NormalisedPlayerVehicleSimilarities = NormaliseList(AllPlayerVehicleSimilarities)

    TopPlayerVehicleSimilarities = {}
    # Combine the two lists, tank IDs and average artificial ratings, into a dictionary
    for Position in range(len(TankIDs)):
        TopPlayerVehicleSimilarities[TankIDs[Position]] = NormalisedPlayerVehicleSimilarities[Position]

    return TopPlayerVehicleSimilarities,Target_PlayerTanks

            
# Function to calculate how similar each unowned vehicle is to each owned vehicle of the target player
def CalculateVehicleSimilarity(cr,db,Target_PlayerTanks,TargetPlayer_UnownedTankIDs):
    # Get a list of all of the tanks in the dataset with the specified attributes
    cr.execute("""SELECT tank_id,tier,nation,type FROM GameTanks""")
    SQL_GameTanks = cr.fetchall()

    # Convert the list of tanks into a dictionary
    GameTanks = {}
    for GameTank in SQL_GameTanks:
        GameTank_ID = GameTank[0]
        Values = GameTank[1:]
        GameTanks[GameTank_ID] = Values
    
    VehicleSimilarities = {}
    TotalCurrentTanks = len(Target_PlayerTanks)
    # Define a default list to be used for each unowned tank, 0s will be replaced with the unowned tank's similarity to the owned tanks of the target player
    DefaultSimilarityList = [0] * TotalCurrentTanks

    # Loop through each unowned tank of the target player
    for UnownedTankID in TargetPlayer_UnownedTankIDs:
        VehicleSimilarities[UnownedTankID] = []

        # Define variable names for specific values to make code easier to read
        UnownedTank_Tier = GameTanks[UnownedTankID][0]
        UnownedTank_Nation = GameTanks[UnownedTankID][1]
        UnownedTank_Type = GameTanks[UnownedTankID][2]

        # Loop through each tank owned by the target player
        for PlayerTank in Target_PlayerTanks:
            
            # Define variable names for specific values to make code easier to read
            PlayerTank_ID = PlayerTank[0]
            PlayerTank_AR = PlayerTank[3]
            PlayerTank_Tier = GameTanks[PlayerTank_ID][0]
            PlayerTank_Nation = GameTanks[PlayerTank_ID][1]
            PlayerTank_Type = GameTanks[PlayerTank_ID][2]

            # If the current unowned tank tier is equal to the current owned tank tier, their similarity is set to 30% to begin with
            if UnownedTank_Tier == PlayerTank_Tier:
                VehicleSimilarity = 0.3
            # Else, their similarity is set to 0% to begin with
            else:
                VehicleSimilarity = 0

            # If the current unowned tank nation is equal to the current owned tank nation, their similarity is increased by 35%
            if UnownedTank_Nation == PlayerTank_Nation:
                VehicleSimilarity += 0.35

            # If the current unowned tank type is equal to the current owned tank type, their similarity is increased by 35%
            if UnownedTank_Type == PlayerTank_Type:
                VehicleSimilarity += 0.35

            # If the current unowned tank similarity is above 0%, multiply the similarity by the current owned tank artificial rating as a weight
            if VehicleSimilarity > 0:
                # Weight the vehicle similarity
                VehicleSimilarity = VehicleSimilarity * PlayerTank_AR

            # Add the weighted similarity of the unowned vehicle to its respective list in the dictionary
            CurrentUnownedSimilarityList = VehicleSimilarities[UnownedTankID]
            CurrentUnownedSimilarityList.append(VehicleSimilarity)
            VehicleSimilarities[UnownedTankID] = CurrentUnownedSimilarityList

    # Loop through each unowned tank in the dictionary of weighted similarities
    for TankID in VehicleSimilarities:
        # Calculate the average weighted vehicle similarity of each unowned tank in the dictionary
        PercentageList = VehicleSimilarities[TankID]
        AveragePercentage = sum(PercentageList) / len(PercentageList)
        VehicleSimilarities[TankID] = AveragePercentage

    # Normalise the similarities for each vehicle
    TankIDs = []
    AllVehicleSimilarities = []
    # Seperate the dictionary of average weighted similarities into two lists, one for tank IDs and one for average weighted similarities
    for TankID in VehicleSimilarities:
        TankIDs.append(TankID)
        AllVehicleSimilarities.append(VehicleSimilarities[TankID])

    # Normalise the list of average weighted similarities
    NormalisedVehicleSimilarities = NormaliseList(AllVehicleSimilarities)

    VehicleSimilarities = {}
    # Combine the two lists, tank IDs and average weighted similarities, into a dictionary
    for Position in range(len(TankIDs)):
        VehicleSimilarities[TankIDs[Position]] = NormalisedVehicleSimilarities[Position]

    return VehicleSimilarities


# Function to calculate the overall unowned vehicle similarity based on the most similar players average weighted artificial rating and the direct vehicle similarity
def CalculateOverallVehicleSimilarity(cr,db,TargetPlayer_UnownedTankIDs,TopPlayerVehicleSimilarities,VehicleSimilarities,SpecialVehicleChoice):
    OverallSimilarities = []
    # Loop through each unowned tank of the target player
    for UnownedTankID in TargetPlayer_UnownedTankIDs:
        TopPlayerVehicleSimilarity = TopPlayerVehicleSimilarities[UnownedTankID]
        VehicleSimilarity = VehicleSimilarities[UnownedTankID]
        
        # Calculate the overall similarity of the unowned vehicle
        OverallSimilarity = (TopPlayerVehicleSimilarity * 0.5) + (VehicleSimilarity * 0.5)
        # Save the result to a list
        OverallSimilarities.append([UnownedTankID, OverallSimilarity])

    # Sort the list of all overall unowned vehicle similarities into descending order
    OverallSimilarities.sort(key = lambda ComparisonValue: ComparisonValue[1], reverse = True)

    # If the user has chosen to exclude special vehicles, remove the corresponding tanks from the list of overall vehicle similarities
    if SpecialVehicleChoice.upper() == "N":
        OutputOverallSimilarities = RemoveSpecialVehicles(cr,db,OverallSimilarities)
        # Return the top 5 overall similarity vehicles to form the main recommendations
        return OutputOverallSimilarities[:5]

    # Else, return the top 5 overall similarity vehicles to form the main recommendations
    else:
        return OverallSimilarities[:5]


# Function to calculate the wild card recommendation for the target player
def CalculateWildCard(cr,db,TargetPlayer_UnownedTankIDs,VehicleSimilarities,SpecialVehicleChoice,OverallSimilarities):
    # Get the list of tank IDs of the 5 main recommendations
    OverallSimilaritiesIDs = []
    for Pair in OverallSimilarities:
        OverallSimilaritiesIDs.append(Pair[0])

    # Get the list of tanks and their corresponding total battles from the dataset
    cr.execute("""SELECT tank_id,total_battles FROM GameTanks""")
    GameTanks = cr.fetchall()
    # Sort the list of tanks by their total battles in ascending order
    GameTanks.sort(key = lambda ComparisonValue: ComparisonValue[1])

    # If the user has chosen to exclude special tanks then remove them from the list
    if SpecialVehicleChoice.upper() == "N":
        GameTanks = RemoveSpecialVehicles(cr,db,GameTanks)

    # Get the data of the unowned vehicles of the target player
    GameTanks = GetUnownedVehiclesData(cr,db,TargetPlayer_UnownedTankIDs,GameTanks)

    TankIDValues = []
    PopularityValues = []
    SimilarityValues = []
    # Loop through each unowned tank of the target player
    # Seperate the ID, popularity and similarity values of each unowned tank into corresponding lists
    for Pair in GameTanks:
        TankIDValues.append(Pair[0])
        PopularityValues.append(Pair[1])
        SimilarityValues.append(VehicleSimilarities[Pair[0]])

    # Normalise the list of popularity values in reverse order
    PopularityValues = NormaliseListReverse(PopularityValues)
    # Normalise the list of similarity values
    SimilarityValues = NormaliseList(SimilarityValues)

    WildCard_Ratings = []
    # For each unowned tank, calculate the wild card rating and append the result to a list
    for Position in range(len(TankIDValues)):
        WildCard_Ratings.append([TankIDValues[Position], PopularityValues[Position] * SimilarityValues[Position]])

    # Sort the list of wild card ratings in descending order
    WildCard_Ratings.sort(key = lambda ComparisonValue: ComparisonValue[1], reverse = True)

    # Loop through each of the wild card rating values
    for WildCard_Rating in WildCard_Ratings:
        TankID = WildCard_Rating[0]
        # Return the first wild card rating in the sorted list that is not within the main 5 recommendations
        if TankID not in OverallSimilaritiesIDs:
            return WildCard_Rating

    return None
        

# Function to output the recommendations for the target player
def OutputRecommendations(cr,db,Target_PlayerID,RecommendationList,WildCard):
##    print("Finalizing...")
##    Spacing(1)

    # Get the list of tanks in the dataset
    cr.execute("""SELECT tank_id,short_name,tier,nation,type FROM GameTanks""")
    SQL_GameTanks = cr.fetchall()
    # Convert the list of tanks to a dictionary grouped by tank ID
    GameTanks = {}
    for GameTank in SQL_GameTanks:
        GameTank_ID = GameTank[0]
        GameTanks[GameTank_ID] = GameTank[1:]

    # Output the table title
    Spacing(1)
    print("   ---   Recommendation Calculations Complete for Player: {0}   ---".format(Target_PlayerID))
    
    # Output each recommendation as a row within the table
    SpacingVariables = [18, 8, 12, 15, 20]
    SpacingValues = len(SpacingVariables)
    for Recommendation in RecommendationList:
        # For each recommendation, get the tanks category data
        TankID = Recommendation[0]
        TankSimilarity = Recommendation[1]
        GameTank = GameTanks[TankID]
        TankDetails = [GameTank[0], GameTank[1], GameTank[2], GameTank[3], CalculatePercentage(TankSimilarity, 2)]

        # Create a string to represent the row of data within the table
        CurrentTankString = ""
        for Position in range(SpacingValues):
            CurrentTankString += CalculateSpacing(TankDetails[Position], SpacingVariables[Position])
        print(CurrentTankString)

    # If a wild card is available for the target player, output it within single row table
    if WildCard != None:
        Spacing(1)
        print(" - Wild Card Recommendation -")
        
        #print(WildCardSimilarity)
        WildCardTankID = WildCard[0]
        WildCardGameTank = GameTanks[WildCardTankID]
        WildCardTankDetails = [WildCardGameTank[0], WildCardGameTank[1], WildCardGameTank[2], WildCardGameTank[3]]

        # Create a string to represent the row of data within the table
        WildCardTankString = ""
        for Position in range(len(WildCardTankDetails)):
            WildCardTankString += CalculateSpacing(WildCardTankDetails[Position], SpacingVariables[Position])
        print(WildCardTankString)
                 

# Function to create the home widgets and start the home window for the user interface
def StartHome(cr,db,Root,HomeWidgets_Positions,AllPlayerStatistics,PlayerStatistics,GameTanks):
    Root.geometry("300x140")
    HomeWidgets = []

    # Create the title widget
    Title = tkinter.Label(Root, text = "WoT Recommender", font = "Helvetica 16 bold", justify = "center")
    Title.pack()
    Title.place(x = HomeWidgets_Positions[0][0], y = HomeWidgets_Positions[0][1], anchor = "center")
    HomeWidgets.append(Title)

    # Create the player ID input box label
    PlayerID_Label = tkinter.Label(Root, text = "Player ID: ", font = "Helvetica 10", justify = "center")
    PlayerID_Label.pack()
    PlayerID_Label.place(x = HomeWidgets_Positions[1][0], y = HomeWidgets_Positions[1][1], anchor = "ne")
    HomeWidgets.append(PlayerID_Label)

    # Create the player ID input box
    PlayerID_Entry = tkinter.Entry(Root)
    PlayerID_Entry.pack()
    PlayerID_Entry.place(x = HomeWidgets_Positions[2][0], y = HomeWidgets_Positions[2][1], anchor = "nw")
    HomeWidgets.append(PlayerID_Entry)

    # Create the special vehicle choice tick box label
    SpecialVehicleChoice_Label = tkinter.Label(Root, text = "Special Vehicles: ", font = "Helvetica 10", justify = "center")
    SpecialVehicleChoice_Label.pack()
    SpecialVehicleChoice_Label.place(x = HomeWidgets_Positions[3][0], y = HomeWidgets_Positions[3][1], anchor = "ne")
    HomeWidgets.append(SpecialVehicleChoice_Label)

    # Create the special vehicle choice tick box
    SpecialVehicleChoice_Value = tkinter.IntVar()
    SpecialVehicleChoice_Button = tkinter.Checkbutton(Root, variable = SpecialVehicleChoice_Value, onvalue = 1, offvalue = 0)
    SpecialVehicleChoice_Button.pack()
    SpecialVehicleChoice_Button.place(x = HomeWidgets_Positions[4][0], y = HomeWidgets_Positions[4][1], anchor = "nw")
    HomeWidgets.append(SpecialVehicleChoice_Button)
    
    # Create the submit button
    ActionButton = tkinter.Button(Root, text = "Submit", command = lambda: SubmitRecommendationInput(cr,db,Root,PlayerID_Entry,SpecialVehicleChoice_Value,HomeWidgets,AllPlayerStatistics,PlayerStatistics,GameTanks))
    ActionButton.pack()
    ActionButton.place(x = HomeWidgets_Positions[5][0], y = HomeWidgets_Positions[5][1], anchor = "center")
    HomeWidgets.append(ActionButton)


# Function to execute when the submit button is clicked on the home window
def SubmitRecommendationInput(cr,db,Root,PlayerID_Entry,SpecialVehicleChoice_Value,HomeWidgets,AllPlayerStatistics,PlayerStatistics,GameTanks):
    # Get the values from the input boxes
    Target_PlayerID = PlayerID_Entry.get()
    SpecialVehicleChoice = SpecialVehicleChoice_Value.get()
    # Format the input values ready for the recommendation functions
    if SpecialVehicleChoice == 0:
        SpecialVehicleChoice = "N"
    elif SpecialVehicleChoice == 1:
        SpecialVehicleChoice = "Y"
    if Target_PlayerID == "":
        Target_PlayerID = GetRandomPlayerID(cr,db)
    else:
        Target_PlayerID = int(Target_PlayerID)

    # Move the home page widgets out of the window view
    for HomeWidget in HomeWidgets:
        HomeWidget.place(x = 3000, y = 3000)

    # Extract the target player statistics from all of the player statistics
    PlayerStatistics,Target_PlayerStatistics = ExtractPlayerStatistic(Target_PlayerID,PlayerStatistics)

    # Get the target player's unowned tanks
    TargetPlayer_UnownedTankIDs = GetUnownedVehicleIDs(cr,db,Target_PlayerID)

    # Calculate the most similar players to the target player
    TopPlayerSimilarities = CalculateTopSimilarityPlayers(cr,db,PlayerStatistics,Target_PlayerStatistics)

    # Calculate the average weighted artificial rating from the most similar players for each of the unowned tanks of the target player
    TopPlayerVehicleSimilarities,Target_PlayerTanks = CalculatePlayerSimilarityVehicles(cr,db,Target_PlayerID,TargetPlayer_UnownedTankIDs,TopPlayerSimilarities)

    # Calculate the direct vehicle similarity between the owned and unowned vehicles of the target player
    VehicleSimilarities = CalculateVehicleSimilarity(cr,db,Target_PlayerTanks,TargetPlayer_UnownedTankIDs)

    # Calculate the overall similarity of each unowned vehicle of the target player
    RecommendationList = CalculateOverallVehicleSimilarity(cr,db,TargetPlayer_UnownedTankIDs,TopPlayerVehicleSimilarities,VehicleSimilarities,SpecialVehicleChoice)

    # Calculate the wild card for the target player
    WildCard = CalculateWildCard(cr,db,TargetPlayer_UnownedTankIDs,VehicleSimilarities,SpecialVehicleChoice,RecommendationList)

    # Display the recommendations in the window
    RecommendationWidgets = ShowRecommendations(cr,db,Root,Target_PlayerID,RecommendationList,WildCard,GameTanks,AllPlayerStatistics)



# Function to create the recommendation widgets and show them in the user interface
def ShowRecommendations(cr,db,Root,Target_PlayerID,RecommendationList,WildCard,GameTanks,AllPlayerStatistics):
    # Change the window size
    Root.geometry("1000x300")
    RecommendationWidgets = []
    # Create a dictionary to transform the integer tier values in roman numerals, as seen in the game
    RomanNumerals = {1 : "I", 2 : "II", 3: "III", 4 : "IV", 5 : "V", 6 : "VI", 7 : "VII", 8 : "VIII", 9 : "IX", 10 : "X"}

    # Create the title of the window
    PlayerID_Label = tkinter.Label(Root, text = "Recommendations for Player ".format(Target_PlayerID), font = "Helvetica 16 bold")
    PlayerID_Label.grid(row = 0, column = 1, columnspan = 4)

    # Loop through each of the main recommendations for the target player
    for Position in range(len(RecommendationList)):

        TankID = RecommendationList[Position][0]
        # Load the icon image of the current tank from the URL saved in the database and apply formatting for display
        RawImage = urllib.request.urlopen(GameTanks[TankID][4]).read()
        OpenImage = Image.open(io.BytesIO(RawImage))
        VehicleImage = ImageTk.PhotoImage(OpenImage)
        ImageLabel = tkinter.Label(Root, image = VehicleImage)
        ImageLabel.image = VehicleImage
        RecommendationWidgets.append(ImageLabel)
        ImageLabel.grid(row = 1, column = Position)

        # Create the name label for the current tank
        NameLabel = tkinter.Label(Root, text = GameTanks[TankID][0], font = "Helvetica 14 bold")
        RecommendationWidgets.append(NameLabel)
        NameLabel.grid(row = 2, column = Position)

        # Create the tier label for the current tank
        TierLabel = tkinter.Label(Root, text = RomanNumerals[GameTanks[TankID][1]], font = "Helvetica 12")
        RecommendationWidgets.append(TierLabel)
        TierLabel.grid(row = 3, column = Position)

        # Create the class label for the current tank
        ClassLabel = tkinter.Label(Root, text = GameTanks[TankID][2].title(), font = "Helvetica 12")
        RecommendationWidgets.append(ClassLabel)
        ClassLabel.grid(row = 4, column = Position)

        # Create the nation label for the current tank
        NationLabel = tkinter.Label(Root, text = GameTanks[TankID][3].title(), font = "Helvetica 12")
        RecommendationWidgets.append(NationLabel)
        NationLabel.grid(row = 5, column = Position)

        # Create the predicted rating label for the current tank
        PercentageLabel = tkinter.Label(Root, text = CalculatePercentage(RecommendationList[Position][1], 3), font = "Helvetica 12")
        RecommendationWidgets.append(PercentageLabel)
        PercentageLabel.grid(row = 6, column = Position)

    # Define the position of the wild card recommendation in the grid of the window
    WildCard_Column = len(RecommendationList) + 1
    Spacing_Column = WildCard_Column - 1
    WildCard_TankID = WildCard[0]

    # Load the icon image of the current tank from the URL saved in the database and apply formatting for display
    WildCard_RawImage = urllib.request.urlopen(GameTanks[WildCard_TankID][4]).read()
    WildCard_OpenImage = Image.open(io.BytesIO(WildCard_RawImage))
    WildCard_VehicleImage = ImageTk.PhotoImage(WildCard_OpenImage)
    WildCard_ImageLabel = tkinter.Label(Root, image = WildCard_VehicleImage)
    WildCard_ImageLabel.image = WildCard_VehicleImage
    RecommendationWidgets.append(WildCard_ImageLabel)
    WildCard_ImageLabel.grid(row = 1, column = WildCard_Column)

    # Create the wild card name label
    WildCard_NameLabel = tkinter.Label(Root, text = GameTanks[WildCard_TankID][0], font = "Helvetica 14 bold")
    RecommendationWidgets.append(WildCard_NameLabel)
    WildCard_NameLabel.grid(row = 2, column = WildCard_Column)

    # Create the wild card tier label
    WildCard_TierLabel = tkinter.Label(Root, text = RomanNumerals[GameTanks[WildCard_TankID][1]], font = "Helvetica 12")
    RecommendationWidgets.append(WildCard_TierLabel)
    WildCard_TierLabel.grid(row = 3, column = WildCard_Column)

    # Create the wild card class label
    WildCard_ClassLabel = tkinter.Label(Root, text = GameTanks[WildCard_TankID][2].title(), font = "Helvetica 12")
    RecommendationWidgets.append(WildCard_ClassLabel)
    WildCard_ClassLabel.grid(row = 4, column = WildCard_Column)

    # Create the wild card nation label
    WildCard_NationLabel = tkinter.Label(Root, text = GameTanks[WildCard_TankID][3].title(), font = "Helvetica 12")
    RecommendationWidgets.append(WildCard_NationLabel)
    WildCard_NationLabel.grid(row = 5, column = WildCard_Column)

    # Create the wild card prediction label
    WildCard_PredictionLabel = tkinter.Label(Root, text = "Wild Card", font = "Helvetica 12")
    RecommendationWidgets.append(WildCard_PredictionLabel)
    WildCard_PredictionLabel.grid(row = 6, column = WildCard_Column)

    # Create the done button
    DoneButton = tkinter.Button(Root, text = "Done", command = lambda: ResetHome(cr,db,Root,AllPlayerStatistics))
    DoneButton.grid(row = 7, column = 2, columnspan = 2)
    

# Function to move the home widgets back into their original potitions and reset the window
def ResetHome(cr,db,Root,AllPlayerStatistics):
    Root.destroy()
    ProgramDisplay(cr,db,AllPlayerStatistics)
    

# Function to begin the user interface of the recommender system
def ProgramDisplay(cr,db,AllPlayerStatistics):
    # Create a copy of the player statistics dictionary
    PlayerStatistics = AllPlayerStatistics.copy()

    # Initialise the window
    Root = tkinter.Tk()
    Root.title("WoT Recommender")
    
    # Get the list of all tanks from the dataset and place them into a dictionary grouped by tank ID
    cr.execute("""SELECT tank_id,short_name,tier,nation,type,images$big_icon,description FROM GameTanks""")
    SQL_GameTanks = cr.fetchall()
    GameTanks = {}
    for GameTank in SQL_GameTanks:
        GameTank_ID = GameTank[0]
        GameTanks[GameTank_ID] = GameTank[1:]

    # Define the positions of widgets on the home page
    HomeWidgets_Positions = [[150, 20], [120, 45], [120, 45], [163, 70], [163, 70], [150, 110]]
    VehicleImages = []

    # Start the window
    StartHome(cr,db,Root,HomeWidgets_Positions,AllPlayerStatistics,PlayerStatistics,GameTanks)
    
    Root.mainloop()


# Function to save the recommendations made for the target player into the database
def SaveRecommendations(cr,db,Target_PlayerID,OverallSimilarities):
    for Similarity in OverallSimilarities:
        cr.execute("""INSERT INTO PlayerRecommendations (account_id,tank_id,similarity) VALUES (?,?,?)""", (Target_PlayerID, Similarity[0], Similarity[1]))
    db.commit()


# Function to generate a recommendation for a given player
def GenerateRecommendation(cr,db,PlayerStatistics,Target_PlayerID,SpecialVehicleChoice):

    # Extract the target player statistics from all of the player statistics
    PlayerStatistics,Target_PlayerStatistics = ExtractPlayerStatistic(Target_PlayerID,PlayerStatistics)

    # Get the target player's unowned tanks
    TargetPlayer_UnownedTankIDs = GetUnownedVehicleIDs(cr,db,Target_PlayerID)

    # Calculate the most similar players to the target player
    TopPlayerSimilarities = CalculateTopSimilarityPlayers(cr,db,PlayerStatistics,Target_PlayerStatistics)

    # Calculate the average weighted artificial rating from the most similar players for each of the unowned tanks of the target player
    TopPlayerVehicleSimilarities,Target_PlayerTanks = CalculatePlayerSimilarityVehicles(cr,db,Target_PlayerID,TargetPlayer_UnownedTankIDs,TopPlayerSimilarities)

    # Calculate the direct vehicle similarity between the owned and unowned vehicles of the target player
    VehicleSimilarities = CalculateVehicleSimilarity(cr,db,Target_PlayerTanks,TargetPlayer_UnownedTankIDs)

    # Calculate the overall similarity of each unowned vehicle of the target player
    RecommendationList = CalculateOverallVehicleSimilarity(cr,db,TargetPlayer_UnownedTankIDs,TopPlayerVehicleSimilarities,VehicleSimilarities,SpecialVehicleChoice)

    # Calculate the wild card for the target player
    WildCard = CalculateWildCard(cr,db,TargetPlayer_UnownedTankIDs,VehicleSimilarities,SpecialVehicleChoice,RecommendationList)

    # Output the recommendations in a table style display
    OutputRecommendations(cr,db,Target_PlayerID,RecommendationList,WildCard)

    return RecommendationList


# Function to time and calculate the average duration of recommender system
def CalculateAverageDuration(cr,db,AllPlayerStatistics):
    Durations = []
    Durations_Post = []
    # Load the previously defined random player IDs
    Random_PlayerIDs = PickleLoad("Random_PlayerIDs")
    Iteration = 0
    # Loop through each random player ID
    for Target_PlayerID in Random_PlayerIDs:
        print("Iteration Number: {0}".format(Iteration + 1))
        Spacing(1)

        # Set the start time of the process
        StartTime = GetCurrentTime()
        
        PlayerStatistics = AllPlayerStatistics.copy()
        SpecialVehicleChoice = "Y"
        # Extract the target player statistics from all of the player statistics
        PlayerStatistics,Target_PlayerStatistics = ExtractPlayerStatistic(Target_PlayerID,PlayerStatistics)
        # Get the target player's unowned tanks
        TargetPlayer_UnownedTankIDs = GetUnownedVehicleIDs(cr,db,Target_PlayerID)
        # Calculate the most similar players to the target player
        TopPlayerSimilarities = CalculateTopSimilarityPlayers(cr,db,PlayerStatistics,Target_PlayerStatistics)
        # Calculate the average weighted artificial rating from the most similar players for each of the unowned tanks of the target player
        TopPlayerVehicleSimilarities,Target_PlayerTanks = CalculatePlayerSimilarityVehicles(cr,db,Target_PlayerID,TargetPlayer_UnownedTankIDs,TopPlayerSimilarities)
        # Calculate the direct vehicle similarity between the owned and unowned vehicles of the target player
        VehicleSimilarities = CalculateVehicleSimilarity(cr,db,Target_PlayerTanks,TargetPlayer_UnownedTankIDs)
        # Calculate the overall similarity of each unowned vehicle of the target player
        RecommendationList = CalculateOverallVehicleSimilarity(cr,db,TargetPlayer_UnownedTankIDs,TopPlayerVehicleSimilarities,VehicleSimilarities,SpecialVehicleChoice)

        # Set the end time of the process
        Duration = CalculateTime(StartTime)

        # Calculate the wild card for the target player
        WildCard = CalculateWildCard(cr,db,TargetPlayer_UnownedTankIDs,VehicleSimilarities,SpecialVehicleChoice,RecommendationList)

        # Set the end time of the process including the wild card post processing
        Duration_Post = CalculateTime(StartTime)

        # Append the duration and post duration to their respective lists
        Durations.append(Duration)
        Durations_Post.append(Duration_Post)
        Iteration += 1

    # Ouput the metrics calculated on the results of the duration tests for the world of tanks recommender system
    Spacing(3)
    print(" -- RS Speed Tests Complete --")
    Spacing(1)
    print("Min Duration: {0}".format(min(Durations)))
    print("Max Duration: {0}".format(max(Durations)))
    print("Avg Duration: {0}".format(sum(Durations) / len(Durations)))
    Spacing(1)
    print("Min Duration Post: {0}".format(min(Durations_Post)))
    print("Max Duration Post: {0}".format(max(Durations_Post)))
    print("Avg Duration Post: {0}".format(sum(Durations_Post) / len(Durations_Post)))
    

# Function to loop the recommendation generation function
def WhileLoopRecommendation(cr,db,AllPlayerStatistics):
    # Initialise the loop
    Recommending = True
    while Recommending == True:

        # Create a copy of the player statistics dictionary
        PlayerStatistics = AllPlayerStatistics.copy()

        # Get the target player ID as an input
        Target_PlayerID = GetTargetPlayer(cr,db)

        # Get the user's special vehicle choice as an input
        SpecialVehicleChoice = GetSpecialVehicleChoice()

        # Generate and output the list of recommendations
        GenerateRecommendation(cr,db,PlayerStatistics,Target_PlayerID,SpecialVehicleChoice)

        Spacing(2)
        # Get input which dictates if the loop should continue again for another recommendation set
        print("Would you like to calculate a new player recommendation (Y/N)?")
        Choice = input()
        if Choice.upper() == "N":
            # If not, close the database and end the loop
            db.close()
            Recommending = False
        else:
            # If yes, output a line of spacing
            Spacing(1)


# Function to calculate all recommendations for all players in the dataset
def CalculateAllRecommendations(cr,db,AllPlayerStatistics):
    for PlayerStatistic in AllPlayerStatistics:
        # Try to load the current player ID to generate a recommendation for from the file
        try:
            CurrentRecommendPlayerID = PickleLoad("CurrentRecommendPlayerID")
        # If it fails, set the ID to 0
        except:
            CurrentRecommendPlayerID = 0

        # Create a copy of the player statistics dictionary
        PlayerStatistics = AllPlayerStatistics.copy()

        # Get the target player ID
        Target_PlayerID = PlayerStatistic[0]

        # If the target player ID is larger than or equal to the current player ID, calculate their recommendations and save them
        if Target_PlayerID >= CurrentRecommendPlayerID:

            # Include special vehicles for all saved recommendations
            SpecialVehicleChoice = "Y"

            # Generate the recommendations for the current player
            RecommendationList = GenerateRecommendation(cr,db,PlayerStatistics,Target_PlayerID,SpecialVehicleChoice)

            # Save the generated recommendations for the current player
            SaveRecommendations(cr,db,Target_PlayerID,RecommendationList)

            # Save the current ID as the new current ID in the file
            PickleDump("CurrentRecommendPlayerID",Target_PlayerID)
    
    # Close the database file
    db.close()
            

# Empty function created to test isolated lines of code without making the Main function messy
def Testing(cr,db):
    print()

    # Below is all of the function calls which can be used to run the world of tanks recommender system with different uses

    CalculateAllRecommendations(cr,db,AllPlayerStatistics)

    WhileLoopRecommendation(cr,db,AllPlayerStatistics)

    CalculateAverageDuration(cr,db,AllPlayerStatistics)

    ProgramDisplay(cr,db,AllPlayerStatistics)

    
    

def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    #Testing(cr,db)

    AllPlayerStatistics = GetPlayerStatistics(cr,db)

    # Change the function call below depending on which option you would like to run the program with
    # See the README file for more information
    ProgramDisplay(cr,db,AllPlayerStatistics)



if __name__ == "__main__":
    Main()
