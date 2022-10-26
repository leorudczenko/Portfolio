import numpy as np
import datetime
from Essential_Functions import Spacing,CalculateSpacing,PickleLoad,PickleDump,ConnectDatabase,ConvertTupleList,GetGroupedPlayerTanks,CalculatePercentage,GetCurrentTime,CalculateTime,GetRandomPlayerID


# Function to get a list of all PlayerTank records and group them by account_id with inner dictionaries
def GetGroupedPlayerTankDictionaries(cr,db,SelectString):
    print("Getting PlayerTanks Records...")
    Spacing(1)

    # Get the selected attributes and the account ID for all player tank records
    cr.execute("""SELECT account_id,tank_id,artificial_rating FROM PlayerTanks""")
    SQL_PlayerTanks = cr.fetchall()
    Grouped_PlayerTanks = {}
    Total = len(SQL_PlayerTanks)
    Current = 0

    print("Grouping PlayerTanks...")
    # Go through each player tank within the list in reverse order
    for PlayerTank in reversed(SQL_PlayerTanks):
        PlayerID = PlayerTank[0]

        # If the found player ID is not currently in the dictionary, add it to the dictionary with an empty dictionary
        if PlayerID not in Grouped_PlayerTanks:
            Grouped_PlayerTanks[PlayerID] = {}

        # Get the saved player tanks for the given player ID and add the current tank record to the dictionary
        CurrentDictionary = Grouped_PlayerTanks[PlayerID]
        CurrentDictionary[PlayerTank[1]] = PlayerTank[2]
        Grouped_PlayerTanks[PlayerID] = CurrentDictionary
        # Pop a player tank record from the list once saved to the dictionary to reduce memory usage
        SQL_PlayerTanks.pop()

        # Output the progress of the process
        Current += 1
        if Current % 1000000 == 0:
            print("Grouping Progress: " + str(round((Current / Total) * 100, 5)) + "%")
    print("Grouping Progress: 100%")
    Spacing(1)
    
    return Grouped_PlayerTanks


# Function to create a matrix from the ratings assigned to each player's own tanks
def GetRatingMatrix(cr,db):
    GroupedPlayerTankDictionaries = GetGroupedPlayerTankDictionaries(cr,db,"tank_id,artificial_rating")

    # Get all of the tank IDs from the dataset
    cr.execute("""SELECT tank_id FROM GameTanks""")
    GameTanks = cr.fetchall()
    GameTanks = ConvertTupleList(GameTanks)

    RatingMatrix = []
    # Loop through each player in the dictionary, obtain their tanks and respective ratings
    for PlayerID in GroupedPlayerTankDictionaries:
        CurrentPlayerTankList = []
        CurrentPlayerTankDictionary = GroupedPlayerTankDictionaries[PlayerID]

        # Loop through all tanks in the dataset by ID
        for TankID in GameTanks:
            # If the current players has played the current tank, add their rating to the list
            if TankID in CurrentPlayerTankDictionary:
                # Add 1 to all played tank ratings so that none are equal to 0
                CurrentPlayerTankList.append(CurrentPlayerTankDictionary[TankID] + 1)
            # Else, add 0 to the list to represent the fact they have not played it
            else:
                CurrentPlayerTankList.append(0)

        # Add the list of current player tanks to the matrix list as a row
        RatingMatrix.append(CurrentPlayerTankList)
    
    return RatingMatrix


# Below is the reference for the MF class source code which uses Object Oriented Programming methods.
# Everything within the MF class, including sourcecode, documentation strings and comments, belongs to the referenced author.
#******************************
#
# Title: Implementation of Matrix Factorization in Python
# Author: Yeung A.A.
# Date: 2017
# Code Version: 1.0
# Availability: https://github.com/albertauyeung/matrix-factorization-in-python
#
#******************************


class MF():
    
    def __init__(self, R, K, alpha, beta, iterations):
        """
        Perform matrix factorization to predict empty
        entries in a matrix.
        
        Arguments
        - R (ndarray)   : user-item rating matrix
        - K (int)       : number of latent dimensions
        - alpha (float) : learning rate
        - beta (float)  : regularization parameter
        """
        
        self.R = R
        self.num_users, self.num_items = R.shape
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations

    def train(self):
        # Initialize user and item latent feature matrice
        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))

        # Initialize the biases
        self.b_u = np.zeros(self.num_users)
        self.b_i = np.zeros(self.num_items)
        self.b = np.mean(self.R[np.where(self.R != 0)])
        
        # Create a list of training samples
        self.samples = [
            (i, j, self.R[i, j])
            for i in range(self.num_users)
            for j in range(self.num_items)
            if self.R[i, j] > 0
        ]
        
        # Perform stochastic gradient descent for number of iterations
        training_process = []
        for i in range(self.iterations):
            np.random.shuffle(self.samples)
            self.sgd()
            mse = self.mse()
            training_process.append((i, mse))
            if (i+1) % 10 == 0:
                print("Iteration: %d ; error = %.4f" % (i+1, mse))
        
        return training_process

    def mse(self):
        """
        A function to compute the total mean square error
        """
        xs, ys = self.R.nonzero()
        predicted = self.full_matrix()
        error = 0
        for x, y in zip(xs, ys):
            error += pow(self.R[x, y] - predicted[x, y], 2)
        return np.sqrt(error)

    def sgd(self):
        """
        Perform stochastic graident descent
        """
        for i, j, r in self.samples:
            # Computer prediction and error
            prediction = self.get_rating(i, j)
            e = (r - prediction)
            
            # Update biases
            self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
            self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])
            
            # Create copy of row of P since we need to update it but use older values for update on Q
            P_i = self.P[i, :][:]
            
            # Update user and item latent feature matrices
            self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
            self.Q[j, :] += self.alpha * (e * P_i - self.beta * self.Q[j,:])

    def get_rating(self, i, j):
        """
        Get the predicted rating of user i and item j
        """
        prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
        return prediction
    
    def full_matrix(self):
        """
        Computer the full matrix using the resultant biases, P and Q
        """
        return self.b + self.b_u[:,np.newaxis] + self.b_i[np.newaxis:,] + self.P.dot(self.Q.T)


#******************************
#
# End of referenced code.
#
#******************************


# Function to apply a matrix factorization algorithm to the dataset to create a machine learning model
def MatrixFactorization(cr,db,RatingMatrix,Target_PlayerID):
    #print("Starting Matrix Factorization...")
    #Spacing(1)
    
    # Convert the matrix to a numpy array and train the model with the given parameters
    RatingMatrix = np.array(RatingMatrix)
    mf = MF(RatingMatrix, K = 75, alpha = 0.1, beta = 0.01, iterations = 250)
    training_process = mf.train()

    #Spacing(1)
    #print("Global bias:")
    #print(mf.b)
    #Spacing(1)

    # Time the process of generating the full matrix
    StartTime = GetCurrentTime()
    CompleteMatrix = mf.full_matrix()
    Duration = CalculateTime(StartTime)

    # Get a list of all tank IDs in the dataset
    cr.execute("""SELECT tank_id FROM GameTanks""")
    GameTanks = cr.fetchall()
    GameTanks = ConvertTupleList(GameTanks)

    # Group all player tank records exclusively with their tank ID
    GroupedPlayerTanks = GetGroupedPlayerTanks(cr,db,"tank_id")
    AllPlayerRecommendations = {}
    PlayerIDs = []
    PlayerTanks = []
    # Loop through each player in the dictionary, create a list of the player IDs and their respective tanks in a seperate list
    # Essentially, convert the dictionary into 2 lists
    for PlayerID in GroupedPlayerTanks:
        PlayerIDs.append(PlayerID)
        PlayerTanks.append(ConvertTupleList(GroupedPlayerTanks[PlayerID]))

    # Loop through each position within the list of player IDs
    for PlayerPosition in range(len(PlayerIDs)):
        # Get the current player's ID and tanks
        CurrentPlayerID = PlayerIDs[PlayerPosition]
        CurrentPlayerTanks = PlayerTanks[PlayerPosition]
        CurrentPlayerRecommendations = []

        # Loop through each position within the list of tanks in the dataset
        for TankPosition in range(len(GameTanks)):
            # Get the current tank's ID
            CurrentTankID = GameTanks[TankPosition]

            # If the current tank has not been played by the current player, get the predicted rating from the rating matrix
            if CurrentTankID not in CurrentPlayerTanks:
                # Save the rating to a list for the current player
                CurrentPlayerRecommendations.append([CurrentTankID, CompleteMatrix[PlayerPosition][TankPosition]])

        # Sort the list of predicted ratings for the current player in descending order
        CurrentPlayerRecommendations.sort(key = lambda ComparisonValue: ComparisonValue[1], reverse = True)
        AllPlayerRecommendations[CurrentPlayerID] = CurrentPlayerRecommendations

    # Extract the predicted ratings of the target player
    #Target_PlayerRecommendations = AllPlayerRecommendations[Target_PlayerID]

    # Loop through each player ID within the predicted ratings
    for PlayerID in AllPlayerRecommendations:
        # For each list of predicted ratings, keep the top 5 and remove all others
        # This forms the 5 recommendations for the player
        AllPlayerRecommendations[PlayerID] = AllPlayerRecommendations[PlayerID][:5]

    # Time the process of generating the matrix and the post processing stage
    Duration_Post = CalculateTime(StartTime)

    # Save the recommendations to a file
    #PickleDump("MatrixFactorization_Recommendations",AllPlayerRecommendations)

    # Output the recommendations for the target player
    #OutputRecommendations(cr,db,Target_PlayerID,Target_PlayerRecommendations)

    return Duration, Duration_Post




# Function to output the list of recommendations for a given player
def OutputRecommendations(cr,db,Target_PlayerID,RecommendationList):
##    print("Finalizing...")
##    Spacing(1)

    # Get specified attributes of all tanks in the dataset
    cr.execute("""SELECT tank_id,short_name,tier,nation,type FROM GameTanks""")
    SQL_GameTanks = cr.fetchall()

    # Group tank data by its ID within a dictionary
    GameTanks = {}
    for GameTank in SQL_GameTanks:
        GameTank_ID = GameTank[0]
        GameTanks[GameTank_ID] = GameTank[1:]

    # Output the table title
    Spacing(1)
    print("   ---   Recommendation Calculations Complete for Player: " + str(Target_PlayerID) + "   ---")

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


# Function to calculate the average duration of the matrix factorization model
def CalculateAverageDuration(cr,db,RatingMatrix):
    Durations = []
    Durations_Post = []
    # Load the previously defined random player IDs
    Random_PlayerIDs = PickleLoad("Random_PlayerIDs")

    # Loop through each random player ID
    Iteration = 0
    for PlayerID in Random_PlayerIDs:
        print("Iteration Number: " + str(Iteration + 1))
        Spacing(1)
        
        # For each player, train the model and time it's duration
        Duration, Duration_Post = MatrixFactorization(cr,db,RatingMatrix,PlayerID)

        # If the duration returns a value less than 0, retry the current iteration
        if Duration < 0 or Duration_Post < 0:
            Duration, Duration_Post = MatrixFactorization(cr,db,RatingMatrix,PlayerID)

        # Append the duration and post duration to their respective lists
        Durations.append(Duration)
        Durations_Post.append(Duration_Post)
        Iteration += 1

    # Ouput the metrics calculated on the results of the duration tests for the matrix factorization model
    Spacing(3)
    print(" -- MF Speed Tests Complete --")
    Spacing(1)
    print("Min Duration: " + str(min(Durations)))
    print("Max Duration: " + str(max(Durations)))
    print("Avg Duration: " + str(sum(Durations) / len(Durations)))
    Spacing(1)
    print("Min Duration Post: " + str(min(Durations_Post)))
    print("Max Duration Post: " + str(max(Durations_Post)))
    print("Avg Duration Post: " + str(sum(Durations_Post) / len(Durations_Post)))
        



def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    RatingMatrix = GetRatingMatrix(cr,db)

    MatrixFactorization(cr,db,RatingMatrix,1)

##    AllPlayerRecommendations = PickleLoad("MatrixFactorization_Recommendations")
##    Target_PlayerID = 
##    OutputRecommendations(cr,db,Target_PlayerID,AllPlayerRecommendations[Target_PlayerID])

   
    
if __name__ == "__main__":
    Main()
