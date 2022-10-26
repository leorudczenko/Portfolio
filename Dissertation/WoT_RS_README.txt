   ---   Dissertation README   ---    

This directory features the code files used for the World of Tanks (WoT) Recommender System (RS) project.
The project aimed to create a RS for the game WoT. The system would take a player's statistics, including their currently played tanks, and use the data to recommend new tanks for the player.
The dataset features 686 tanks records, 17,724 player records, 1,616,868 records of player owned tanks, and 88,620 recommendation records.

----------------------------------------------------------------------------------------------------------------------------

The dataset used for the project includes 4 tables:

	GameTanks
		For each tank in the game, it's vehicle characteristics are stored in this table.
	
	PlayerStatistics
		For each player in the dataset, their statistical performance (such as their win rate percentage or total games played) is stored in this table.
	
	PlayerTanks
		For each player in the dataset, the tanks they have played and their statistical performance in those tanks are stored in this table.
	
	PlayerRecommendations
		For each player in the dataset, the 5 tank recommendations with the best match percentage are saved to this table.

----------------------------------------------------------------------------------------------------------------------------

Each file of the project has a different purpose, as seen below:

The files below are used for data preprocessing:
	Database_Management.py
	Record_Deletion.py
	WG_API.py

The files below are used for data analysis:
	Algorithm_Comparison.py
	Data_Analysis.py
	Player_Analysis.ipynb
	Principle_Component_Analysis.ipynb
	Result_Analysis.ipynb
	Threshold_Analysis.ipynb

The following files are used for feature testing:
	Artificial_Rating.py
	Matrix_Factorization_Model.py
	Vehicle_Personality_Preference.py
	Vehicle_Popularity.py

The following files are used for the generation of recommendations:
	Essential_Functions.py
	Recommendation_Generation.py

----------------------------------------------------------------------------------------------------------------------------

The Recommendation_Generation.py file can be run with different function calls within the main function on line 922:

	CalculateAllRecommendations 
		Generates and saves recommendations for all players within the dataset.

	WhileLoopRecommendations 
		Provides a looped instance of the WoT RS, allowing for user input and a text display.

	CalculateAverageDuration
		Calculates the average time the WoT RS takes to generate recommendations.

	ProgramDisplay
		Provides a user interface for the WoT RS which was only made for concept understanding.

The function parameters are the same for all 4 functions calls.

----------------------------------------------------------------------------------------------------------------------------

For the purposes of this portfolio, private information such as personal Player ID numbers and API keys have been removed.
Any remaining Player ID values are newly assigned numbers to ensure anonymity.
The Recommendation_Generation.py file will still run with the removed private data. Other files may not.
