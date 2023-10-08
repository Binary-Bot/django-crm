import pandas as pd
import numpy, random


# Reads and returns the CSV file as a Pandas Database
def getCasenumDB():
    return pd.read_csv("CaseNum.csv", sep=';')


# Generates a new casenum
def generateNewNum(db):
    currentNum = db['Client Num'].max()
    print("Generating New Num", currentNum)
    while True:
        currentNum += 1
        if currentNum not in db['Client Num']:
            break
    return currentNum


# Generates new matter number
def generateNewMatterNum(db):
    lastValue = db['Matter Num'].iloc[-1]
    while True:
        lastValue += 1
        if lastValue not in db['Matter Num']:
            break
    return lastValue


# Returns an existing client number
def getExistingClientNumber(db, clientName):
    print("Getting Client Number")
    return db[db['Client Description'] == clientName]['Client Num'].values[0]


def getClientNumber(db, clientName):
    # If the client already exists, then give the existing client number
    if clientName in db['Client Description'].values:
        return getExistingClientNumber(db, clientName)
    # Else return a new client number
    return generateNewNum(db)


# Saves the new data into the csv file
def saveInDB(db, year, attorney, clientDesc, matterDesc, matterOnly, clientNum, matterNum, time, user, a, b):
    try:
        # Validate input data (add more checks if needed)
        # if not isinstance(year, int) or not isinstance(clientNum, int) or not isinstance(matterNum, int):
        #     raise ValueError("Year, Client Num, and Matter Num must be integers.")

        # Create a new row as a dictionary
        new_data = {'Year': year, 'Attorney': attorney, 'Client Description': clientDesc,
                    'Matter Description': matterDesc, 'Matter only': matterOnly, 'Client Num': clientNum,
                    'Matter Num': matterNum, 'Timestamp': time, 'user': user, 'Unnamed: 9': a, 'Unnamed: 10': b}

        # Convert the new data to a DataFrame
        new_df = pd.DataFrame([new_data])

        # Concatenate the new row(s) with the existing DataFrame
        db = pd.concat([db, new_df], ignore_index=True)

        # Save the updated DataFrame to a CSV file
        db.to_csv("CaseNum.csv", index=False, sep=";")

        print("Data successfully added to the database.")
    except Exception as e:
        print(f"Error: {str(e)}")


# Main program
def main():
    while True:
        db = getCasenumDB()
        # Gets rid of null (empty) values in the Client Num column
        db['Client Num'] = pd.to_numeric(db['Client Num'], errors='coerce')
        db.dropna(subset=['Client Num'], inplace=True)
        db['Client Description'] = db['Client Description'].astype(str)
        clientName = input("Client Description: ")
        clientNum = getClientNumber(db, clientName)
        print("Your client number is: ", clientNum)
        saveInDB(db, 23, "", clientName, "", 0, clientNum, generateNewMatterNum(db),
                 0, "", 0, 0)


main()
