from datetime import datetime
from datetime import timedelta
import math
import re

# Reads blood glucose levels (manually input)
def getGlucose() :
    while(1) :
        try :
            print("Enter in blood glucose level: ")
            glucose = int(input())

            # Verifies glucose input
            if ((glucose < 0) | (glucose > 9999)):
                raise InputError()
            else :
                break
        except :
            print("Value is not an acceptable glucose level. Try again.")

    return glucose

# Calculates the required insulin amount
def getInsulin() :
    insulin = 0
    glucose = getGlucose()  # manually input glucose
    dosage = calcDosage()   # checks if user is resistant, normal or senstive (to insulin)

    # Sets insulin amount
    if (glucose >= 349) :
        print("Your glucose levels are dangerously high. Call your doctor immediately.")
        insulin = 8
    elif (glucose >= 300) :
        insulin = 7
    elif (glucose >= 250) :
        insulin = 5
    elif (glucose >= 200) :
        insulin = 3
    elif (glucose >= 150) :
        insulin = 1
    elif (glucose <= 50) :
        print("Your glucose levels are dangerously low. Call your doctor immediately.")

    # Calculating insulin-sensitivity or resistance
    if (dosage == "sensitive") :
        insulin -= math.floor(insulin * 1.45 - insulin)
    elif (dosage == "resistant") :
        insulin = math.floor(insulin * 1.33) + 1
        if (insulin == 11) : # only method I've found that follows the chart atm
            insulin = 12
        elif (insulin == 1) :
            insulin = 0

    # Logging glucose and insulin amounts
    log(glucose, insulin)

    return insulin

# Logs the information in a text file
def log(glucose, insulin) :
    date = datetime.now() # sets current date and time
    date += timedelta(days=1) #*****************************************************************************************FOR TESTING (changes date)
    try :
        file = open("insulin_log.txt", 'a')

        # Allows up to 100 lines to be logged
        checkLog(100)

        file.write("Glucose Level: " + str(glucose).zfill(1).rjust(4) + " | Insulin Given: " + str(insulin).zfill(1).rjust(2) + " | Date Administered: " + str(date) + '\n')
        file.close()
    except :
        print("An error occured while writing to the log.")

# Makes sure log doesn't exceed the line limit
def checkLog(limit) :
    try :
        file = open("insulin_log.txt", 'r')
        while (len(file.readlines()) >= limit) :
            file = open("insulin_log.txt", 'r') # moving cursor back up

            # Deletes oldest lines first
            with open("insulin_log.txt", 'r') as check :
                data = check.read().splitlines(True)
            with open("insulin_log.txt", 'w') as delete :
                delete.writelines(data[1:])
        file.close()
    except :
        print("An error occured while limiting lines in the log.")

# Prints the log information
def readLog() :
    print() # new line for formatting
    print("Log: ")
    try :
        file = open("insulin_log.txt", 'r')
        print(file.read())
        file.close()
    except :
        print("An error occured while reading the log.")

# Deletes all log contents (Just useful for testing)
def deleteLog() :
    file = open("insulin_log.txt", "w")
    file.write("")
    file.close()

# Uses the log to decipher the patient's insulin dosage (only works if dates are in order)
# Does not calculate last day (is consider incomplete until new day arrives)
def calcDosage() :
    try :
        date = []       # array of dates
        insulin = []    # array of insulin amounts given
        logArray = []   # array of all lines in log
        dailyTotal = 0  # total insulin in a day
        totals = []     # array of daily totals
        average = -1    # average of all totals

        file = open("insulin_log.txt", 'r')
        logArray = file.readlines()
        file.close()

        # Gets all the insulin pump amounts and their dates given
        for i in range(len(logArray)) :
            line = logArray[i]
            insulin.append(int(line[37:39]))
            date.append(line[61:71])
            i += 1

        # This adds up the insulin amounts until a new date appears
        for i in range(len(logArray) - 1) :
            if (date[i] == date[i + 1]) :
                dailyTotal += insulin[i]
            else : # new date appears:
                dailyTotal += insulin[i]
                totals.append(dailyTotal)
                average += dailyTotal
                dailyTotal = 0

        # Calculates the average to see if user is insulin-sensitive or resistant (or neither)
        if (average == -1) :
            average = 40 # not enough results (normal is default)
        else :
            average = average / (len(totals))
        if (average > 80) :
            return "resistant"
        elif (average > 40) :
            return "normal"
        else :
            return "sensitive"
    except :
        print("An error occured while calculating dosage from log info.")

# TO RUN: You will enter in 10 doses at a time, then you should change the date in log()

#deleteLog() #********************************************************************************************************** use this if log gets too big (or just find the .txt file and delete its contents)

# Entering in glucose levels 10 at a time:
for i in range(10) :
    #print("Insulin Amount Given: " + str(getInsulin()) + " units") #*************************************************** use if you want to actively see results as amounts are entered
    #getInsulin() #***************************************************************************************************** use if you want to just enter results asap
    i += 1


# Showing off log results:
readLog()