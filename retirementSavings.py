from functions import grabQuotes, displayQuote
from time import sleep
import csv
from datetime import date


currentDate = date.today()


def retirementSavings():
    """ Provides control flow for the retirement savings simulator."""

    # motivational quote integration
    quoteList = []
    grabQuotes(quoteList)
    lenList = len(quoteList)

    # welcome messages
    print("Welcome to the retirement savings simulator!\n")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)
    print("The purpose of this tool is to give you an idea of how much money you will have saved at ")
    print("specific time points in the future. This is based off of what type of retirement accounts you use,")
    print("how much you are saving in each account, employer match rate, along with other variables.\n")
    sleep(4)

    # querying for if they want to load account info or input new, and what the values are
    savedElements = loadStoredData()
    response = loadingQuery(savedElements[0][0], savedElements[0][1], "Traditional IRA")
    if response == "YES":
        tradAccountTotal, tradYearlyAddition = savedElements[0][0], savedElements[0][1]
    elif response == "NO":
        print("The annual contribution limit for Traditional and Roth IRA accounts combined is "
              "$6,000 under age 50 or $7,000 over age 50 (as of 2021).")
        tradAccountTotal, tradYearlyAddition = retirementType("Traditional IRA", "don't repeat")

    response = loadingQuery(savedElements[1][0], savedElements[1][1], "Roth IRA")
    if response == "YES":
        rothAccountTotal, rothYearlyAddition = savedElements[1][0], savedElements[1][1]
    elif response == "NO":
        rothAccountTotal, rothYearlyAddition = retirementType("Roth IRA", "don't repeat")

    response = loadingQuery(savedElements[2][0], savedElements[2][1], "HSA")
    if response == "YES":
        hsaAccountTotal, hsaYearlyAddition = savedElements[2][0], savedElements[2][1]
    elif response == "NO":
        hsaAccountTotal, hsaYearlyAddition = retirementType("Health Savings Account",
                                                            "3,600$ under age 55 or 4,600$ age 55+ (as of 2021).")

    response = loadingQuery(savedElements[3][0], savedElements[3][1], "Educational")
    if response == "YES":
        educationalAccountTotal, educationalYearlyAddition = savedElements[3][0], savedElements[3][1]
    elif response == "NO":
        print("\nThe two main types of educational savings accounts are the ESA and the 529")
        educationalAccountTotal, educationalYearlyAddition = retirementType("educational savings",
                                                                            "2,000$ for ESAs or 15,000$ for 529s "
                                                                            "(before paying gift tax) (as of 2021).")

    response = loadingQuery(savedElements[4][0], savedElements[4][1], "401k")
    if response == "YES":
        employmentAccountTotal, employmentYearlyAddition = savedElements[4][0], savedElements[4][1]
    elif response == "NO":
        employmentAccountTotal, employmentYearlyAddition = retirementType("401k",
                                                                          "19,500$ for under 50 or 26,000$ for 50+ "
                                                                          "(as of 2021).")
    employerMatch = validateNumberGreaterThanEqualToZero("What is the employer match rate for the 401k? "
                                                         "(Enter the rate as a whole number such as 50 for a 50% match "
                                                         "rate): ")

    returnRate = validateNumberGreaterThanEqualToZero("\nWhat annual rate of return would you like to use "
                                                      "(Enter the rate as a whole number such as 7 for a 7% return "
                                                      "rate): ")

    #saving data to csv file
    savingsArray = [(tradAccountTotal, tradYearlyAddition), (rothAccountTotal, rothYearlyAddition),
                    (hsaAccountTotal, hsaYearlyAddition), (educationalAccountTotal, educationalYearlyAddition),
                    (employmentAccountTotal, employmentYearlyAddition)]

    with open("savings.csv", mode='wt', newline="") as file1:

        csv_writer = csv.writer(file1)
        for element in savingsArray:
            csv_writer.writerow(element)

    #runs the simulation for 55 years
    currentYear = 0
    currentContributions = (tradAccountTotal + rothAccountTotal + hsaAccountTotal + educationalAccountTotal +
                            employmentAccountTotal)

    while currentYear < 55:

        #updating the accounts for 1 year worth of contributions and interest
        tradAccountTotal = updateAccountAmount(tradAccountTotal, tradYearlyAddition, returnRate)
        rothAccountTotal = updateAccountAmount(rothAccountTotal, rothYearlyAddition, returnRate)
        hsaAccountTotal = updateAccountAmount(hsaAccountTotal, hsaYearlyAddition, returnRate)
        educationalAccountTotal = updateAccountAmount(educationalAccountTotal, educationalYearlyAddition, returnRate)
        employmentAccountTotal = updateEmployerAmount(employmentAccountTotal, employmentYearlyAddition, returnRate,
                                                      employerMatch)
        currentContributions += (tradYearlyAddition + rothYearlyAddition + hsaYearlyAddition +
                                 educationalYearlyAddition + employmentYearlyAddition +
                                 (employmentYearlyAddition * (employerMatch/100)))

        currentSavingsTotal = sumSavings(tradAccountTotal, rothAccountTotal, hsaAccountTotal, educationalAccountTotal,
                                         employmentAccountTotal)

        currentYear += 1

        #year trackers/messages
        if currentYear == 1:
            tracker(1, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal,
                    educationalAccountTotal, employmentAccountTotal, currentContributions)

        elif currentYear == 5:
            tracker(5, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal,
                    educationalAccountTotal, employmentAccountTotal, currentContributions)

        elif currentYear == 10:
            tracker(10, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal,
                    educationalAccountTotal, employmentAccountTotal, currentContributions)

        elif currentYear == 15:
            tracker(15, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal,
                    educationalAccountTotal, employmentAccountTotal, currentContributions)

        elif currentYear == 25:
            tracker(25, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal,
                    educationalAccountTotal, employmentAccountTotal, currentContributions)

        elif currentYear == 50:
            tracker(50, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal,
                    educationalAccountTotal, employmentAccountTotal, currentContributions)

    # csv saving reminder
    print("\nSaving retirement account information for use next time")


def sumSavings(traditionalIraSavings, rothIraSavings, hsaSavings, educationalSavings, employmentSavings):
    """ Computes sum from all current savings accounts."""

    totalSum = (traditionalIraSavings + rothIraSavings + hsaSavings + educationalSavings + employmentSavings)
    return totalSum


def updateAccountAmount(accountTotal, yearlyAddition, returnRate):
    """ This algorithm computes an account's value after one year. It first converts the return rate to a decimal,
    and converts the yearly user contribution to a monthly contribution. It then adds to the account total the
    account total times the decimal return rate, representing the interest that the starting account amount will
    accumulate over the year.

    The for loop then represents a user making an equal monthly payment at the start of each month throughout
    the year. The interest that each monthly payment will accumulate is calculated as the payment amount times
    the decimal return rate times a correction factor for how many months this payment will actually be in the account
    in that year. For example, the first payment will be in the account for 12 months in the year
    and therefore the correction factor will be 12/12. However, the last payment will only be in the account for
    1 out of the 12 months and therefore the return rate will have a correction factor applied of 1/12.
    """

    returnRateDecimal = (returnRate / 100)
    monthlyAddition = yearlyAddition / 12
    accountTotal += (accountTotal * returnRateDecimal)

    for i in range(12, 0, -1):
        monthCorrectionFactor = (i / 12)
        accountTotal += (monthlyAddition + (monthlyAddition * returnRateDecimal * monthCorrectionFactor))

    return accountTotal


def updateEmployerAmount(accountTotal, yearlyAddition, returnRate, employerMatch):
    """ Updates the 401k account amount including the employer match rate."""

    returnRateDecimal = (returnRate / 100)
    monthlyAddition = (yearlyAddition / 12)

    #this first line adds the interest for the amount that has been in there from the start of the year
    accountTotal += (accountTotal * returnRateDecimal)
    employerTotal = yearlyAddition * (employerMatch/100)
    monthlyEmployerAddition = (employerTotal / 12)

    #the for loop represents a user putting in a monthly deposit at the beginning of the month equal to
    #one twelfth of the yearly deposit amount, and the employer putting in a monthly deposit equal to one twelfth
    #of the employer yearly deposit, and having these grow for the rest of the year according to a fraction
    #of the return rate corresponding to the number of months left in the year for it to grow

    for i in range(12, 0, -1):

        monthCorrectionFactor = (i / 12)
        accountTotal += (monthlyAddition + (monthlyAddition * returnRateDecimal * monthCorrectionFactor))
        accountTotal += (monthlyEmployerAddition +
                         (monthlyEmployerAddition * returnRateDecimal * monthCorrectionFactor))

    return accountTotal


def validateNumberGreaterThanEqualToZero(message):
    """ Validates number entries."""

    badInput = True
    while badInput:
        try:
            response = int(input(message))
            while response < 0:
                response = int(input("Only positive amounts greater than or equal to 0 allowed. Try again: "))
            badInput = False
        except ValueError:
            print("Only numbers allowed")
    return response


def retirementType(type1, limit):
    """ Handles queries regarding retirement account entries."""

    acceptedAnswers = ["yes", "YES", "Yes", "NO", "No", "no"]

    response = input("\nWould you like to enter a new " + str(type1) + " account?: ")
    while response not in acceptedAnswers:
        response = input("only yes or no responses allowed, try again: ")
    if response == "YES" or response == "Yes" or response == "yes":
        accountTotal = validateNumberGreaterThanEqualToZero("How much money do you currently have"
                                                            " in the " + str(type1) + "?: ")
        if limit != "don't repeat":
            print('The annual contribution limit for this type of account is ' + str(limit))
            sleep(2)
        accountYearlyAddition = validateNumberGreaterThanEqualToZero("What will your yearly contribution "
                                                                     "into this account be?: ")

        return accountTotal, accountYearlyAddition

    else:
        return 0, 0


def tracker(years, currentSavingsTotal, tradAccountTotal, rothAccountTotal, hsaAccountTotal, educationalAccountTotal,
            employmentAccountTotal, currentContributions):
    """Displays information regarding current amount totals at different time intervals."""

    currentInterestTotal = currentSavingsTotal - currentContributions

    #message if the tracker is reporting info for 1 year
    if years == 1:
        print("\nAfter " + str(years) + " year (" + str(currentDate.year + years) +
              "), total savings are " + "${:,.0f}".format(int(currentSavingsTotal)))
        print("Composition Breakdown:  Contributions = " + "${:,.0f}".format(int(currentContributions)) +
              "  Interest = " + "${:,.0f}".format(int(currentInterestTotal)))
        print("Account Breakdown: (Traditional IRA " + "${:,.0f})".format(int(tradAccountTotal)) + ", (Roth IRA " +
              "${:,.0f})".format(int(rothAccountTotal)) + ", (HSA " + "${:,.0f})".format(int(hsaAccountTotal))
              + ", (Educational Savings " + "${:,.0f})".format(int(educationalAccountTotal)) + ", (401k " +
              "${:,.0f})".format(int(employmentAccountTotal)))
        sleep(2)

    #message if the tracker is reporting for longer periods of time
    else:
        print("\nAfter " + str(years) + " years (" + str(currentDate.year + years) +
              "), total savings are " + "${:,.0f}".format(int(currentSavingsTotal)))
        print("Composition Breakdown:  Contributions = " + "${:,.0f}".format(int(currentContributions)) +
              "  Interest = " + "${:,.0f}".format(int(currentInterestTotal)))
        print("Account Breakdown: (Traditional IRA " + "${:,.0f})".format(int(tradAccountTotal)) + ", (Roth IRA " +
              "${:,.0f})".format(int(rothAccountTotal)) + ", (HSA " + "${:,.0f})".format(int(hsaAccountTotal))
              + ", (Educational Savings " + "${:,.0f})".format(int(educationalAccountTotal)) + ", (401k " +
              "${:,.0f})".format(int(employmentAccountTotal)))
        sleep(2)


def loadStoredData():
    """ Loads data stored in csv storage."""

    with open("savings.csv", mode='r', newline='') as file1:

        csv_reader = csv.reader(file1)
        savedElements = []

        for row in csv_reader:
            element = [int(row[0]), int(row[1])]
            savedElements.append(element)

        return savedElements


def loadingQuery(accountValue, yearlyAddition, accountType):
    """Asks users if they want to use saved account information."""

    acceptableAnswers = ["yes", "Yes", "YES", "No", "NO", "no"]

    if accountValue == 0 and yearlyAddition == 0:
        return "NO"

    elif accountValue != 0 or yearlyAddition != 0:
        print("\nStored " + str(accountType) + " account found. Account value: " + "${:,.0f}".format(int(accountValue))
              + "  Monthly Contribution: " + "${:,.0f}".format(int(yearlyAddition)))

        response = input("\nWould you like to use this saved account? ")
        while response not in acceptableAnswers:
            response = input("only yes or no responses allowed, try again: ")
        if response == "YES" or response == "Yes" or response == "yes":
            return "YES"
        elif response == "NO" or response == "No" or response == "no":
            return "NO"
