import sqlite3,pathlib,os
from Essential_Functions import ConnectDatabase,CalculateColumnSum,CalculateColumnAverage


# Function to calculate the popularity (total battles) of each tank in the dataset
def CalculatePopularity(cr,db):
    # Calculate the total battles played by all players within each tank
    cr.execute("""SELECT tank_id,SUM(battles) FROM PlayerTanks GROUP BY tank_id""")
    Pairs = cr.fetchall()
    # Save each of the results into the database file
    for Pair in Pairs:
        cr.execute("""UPDATE GameTanks SET total_battles = ? WHERE tank_id = ?""", (Pair[1], Pair[0]))
        
    db.commit()




def Main():
    cr,db = ConnectDatabase("WoTData.db")
    
    #CalculatePopularity(cr,db)

    print(CalculateColumnSum(cr,db,"GameTanks","total_battles"))



if __name__ == "__main__":
    Main()
