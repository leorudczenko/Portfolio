import sqlite3,pathlib,os
from Essential_Functions import ConvertTupleList,ConnectDatabase,GetTableInfo


# Function to create a table to store the tank statistics in the database
def CreateGameTanksTable(cr,db):
    CreateSQL = """CREATE TABLE GameTanks(
    tank_id INTEGER PRIMARY KEY,
    name VARCHAR,
    short_name VARCHAR,
    tag VARCHAR,
    description VARCHAR,
    images$big_icon VARCHAR,
    images$contour_icon VARCHAR,
    images$small_icon VARCHAR,
    tier INTEGER,
    nation VARCHAR,
    type VARCHAR,
    special_status INTEGER
    );"""
    cr.execute(CreateSQL)
    db.commit()
    

# Function to create a table to store the player statistics in the database
def CreatePlayerStatisticsTable(cr,db):
    CreateSQL = """CREATE TABLE PlayerStatistics(
    account_id INTEGER PRIMARY KEY,
    last_battle_time INTEGER,
    created_at INTEGER,
    updated_at INTEGER,
    global_rating INTEGER,
    clan_id VARCHAR,
    statistics$all$spotted INTEGER,
    statistics$all$battles_on_stunning_vehicles INTEGER,
    statistics$all$max_xp INTEGER,
    statistics$all$avg_damage_blocked REAL,
    statistics$all$direct_hits_received INTEGER,
    statistics$all$explosion_hits INTEGER,
    statistics$all$piercings_received INTEGER,
    statistics$all$piercings INTEGER,
    statistics$all$max_damage_tank_id INTEGER,
    statistics$all$xp INTEGER,
    statistics$all$survived_battles INTEGER,
    statistics$all$dropped_capture_points INTEGER,
    statistics$all$hits_percents INTEGER,
    statistics$all$draws INTEGER,
    statistics$all$max_xp_tank_id INTEGER,
    statistics$all$battles INTEGER,
    statistics$all$damage_received INTEGER,
    statistics$all$avg_damage_assisted REAL,
    statistics$all$max_frags_tank_id INTEGER,
    statistics$all$avg_damage_assisted_track REAL,
    statistics$all$frags INTEGER,
    statistics$all$stun_number INTEGER,
    statistics$all$avg_damage_assisted_radio REAL,
    statistics$all$capture_points INTEGER,
    statistics$all$stun_assisted_damage INTEGER,
    statistics$all$max_damage INTEGER,
    statistics$all$hits INTEGER,
    statistics$all$battle_avg_xp INTEGER,
    statistics$all$wins INTEGER,
    statistics$all$losses INTEGER,
    statistics$all$damage_dealt INTEGER,
    statistics$all$no_damage_direct_hits_received INTEGER,
    statistics$all$max_frags INTEGER,
    statistics$all$shots INTEGER,
    statistics$all$explosion_hits_received INTEGER,
    statistics$all$tanking_factor REAL,
    statistics$trees_cut INTEGER,
    logout_at INTEGER
    );"""
    cr.execute(CreateSQL)
    db.commit()
    

# Function to create a table to store the player's tanks in the database
def CreatePlayerTanksTable(cr,db):
    CreateSQL = """CREATE TABLE PlayerTanks(
    Record_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    tank_id INTEGER,
    wins INTEGER,
    battles INTEGER,
    mark_of_mastery INTEGER,
    FOREIGN KEY (account_id) REFERENCES PlayerStatistics (account_id)
    );"""
    cr.execute(CreateSQL)
    db.commit()


# Function to create the tables required for the database
# Output information about the tables to confirm success
def SetupDatabase(cr,db):
    CreatePlayerStatisticsTable(cr,db)
    CreatePlayerTanksTable(cr,db)
    print("Columns in PlayerStatistics: " + str(len(GetTableInfo(cr, db, "PlayerStatistics"))))
    print("Columns in PlayerTanks: " + str(len(GetTableInfo(cr, db, "PlayerTanks"))))
    print("Database setup successfully.")
    Spacing(1)


# Function to add a new column to the PlayerTanks table for the Artificial Rating
def Add_AR_Column(cr,db):
    SQL = """ALTER TABLE PlayerTanks ADD COLUMN artificial_rating REAL"""
    cr.execute(SQL)
    db.commit()


# Function to add a new column to the PlayerStatistics table for the Vehicle Personality Preference
def Add_VPP_Column(cr,db):
    SQL = """ALTER TABLE PlayerStatistics ADD COLUMN vehicle_personality_preference VARCHAR"""
    cr.execute(SQL)
    db.commit()


# Function to add a new column to the GameTanks table for the popularity of the vehicle (total battles)
def Add_Popularity_Column(cr,db):
    SQL = """ALTER TABLE GameTanks ADD COLUMN total_battles INTEGER"""
    cr.execute(SQL)
    db.commit()


# Function to add a new column to the PlayerStatistics table for the PCA results
def Add_PCA_Column(cr,db):
    SQL = """ALTER TABLE PlayerStatistics ADD COLUMN pca_rating REAL"""
    cr.execute(SQL)
    db.commit()


# Function to create a table to store the player's tank recommendations in the database
def CreatePlayerRecommendationsTable(cr,db):
    CreateSQL = """CREATE TABLE PlayerRecommendations(
    Recommendation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    tank_id INTEGER,
    similarity REAL,
    FOREIGN KEY (account_id) REFERENCES PlayerStatistics (account_id),
    FOREIGN KEY (tank_id) REFERENCES GameTanks (tank_id)
    );"""
    cr.execute(CreateSQL)
    db.commit()


def Main():
    cr,db = ConnectDatabase("WoTData.db")

    #CreatePlayerRecommendationsTable(cr,db)

##    TableInfo = GetTableInfo(cr,db,"PlayerRecommendations")
##    for Info in TableInfo:
##        print(Info)



if __name__ == "__main__":
    Main()
