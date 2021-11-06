from functions import grabQuotes, displayQuote
from time import sleep
from operator import itemgetter
import copy
import csv
from datetime import date


currentDate = date.today()


def debtRepayment():
    """
    Algorithm implementation: After loading all applicable debts, the program then makes two copies of the array, each
    containing all of the debts. It then sorts the arrays, for the snowball method it is in ascending order based on
    the principal amount. For the avalanche method the array is in descending order based on the interest rate. The
    program then runs two simulations, one for each debt repayment method. The simulation runs on a month by month
    basis. It takes the monthly payment for a certain month, then runs through each debt and subtracts that debt's
    monthly interest from the monthly payment. (Monthly interest is calculated by taking yearly interest rate,
    dividing by 12, then multiplying this by the debt principal amount.) With the remaining monthly payment, it
    subtracts this payment from the next corresponding debt principal amount until either the monthly payment is all
    gone or that debt is gone. This process is repeated monthly until all debts principals are zero.

    """

    #motivational quote integration
    quoteList = []
    grabQuotes(quoteList)
    lenList = len(quoteList)

    # welcome messages
    print("Welcome to the debt repayment simulator!\n")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)
    print("The purpose of this tool is to help give you information regarding debt repayment, ")
    print("such as how long it will take to pay debts off, comparing different forms")
    print("of repayment, and total amount of money spent after the debt is paid off.\n")
    sleep(4)
    print("Note: This simulator assumes that for all debts, you are making at least a minimum monthly payment"
          " that equals the monthly interest.\n")
    sleep(3)

    #loading csv data
    acceptedAnswers = ["yes", "YES", "Yes", "NO", "No", "no"]
    debts = []
    savedElements = loadStoredData()
    notDoneEntering = True

    if len(savedElements) > 0:

        response = input("Would you like to use any of your saved values from the previous session?:")
        while response not in acceptedAnswers:
            response = input("only yes or no responses allowed, try again: ")
        if response == "YES" or response == "Yes" or response == "yes":
            sleep(1)
            print("Loading saved values")
            sleep(2)
            print("These values are FORMAT: Index. (debt, interest rate)")

            for i in range(len(savedElements)):
                print(str(i+1) + ". " + str(savedElements[i]))

            response = input("Enter the indexes of the debts you would like to use, separated by a space: ")
            splitResponse = response.split()

            for i in range(len(splitResponse)):
                debts.append(savedElements[int(splitResponse[i]) - 1])

            sleep(1)
            response = input("Would you like to enter additional debts?:")
            while response not in acceptedAnswers:
                response = input("only yes or no responses allowed, try again: ")
            if response == "NO" or response == "No" or response == "no":
                notDoneEntering = False

        elif response == "NO" or response == "No" or response == "no":

            print("\nThe simulator will use new values, starting with the first entered debt.")

    elif len(savedElements) == 0:
        print("\nThe simulator will use new values, starting with the first entered debt.")

    #entering new debts
    while notDoneEntering:

        debtAmount = validateNumberGreaterThanZero("Enter the dollar amount of this debt: ")
        debtRate = validateNumberGreaterThanZero("Enter the annual interest rate of this debt, as a whole number "
                                                 "(ex. for 5% enter 5): ")

        debts.append([debtAmount, debtRate])
        print("Entry added\n")
        sleep(2)
        response = input("Would you like to enter an additional debt?:")
        while response not in acceptedAnswers:
            response = input("only yes or no responses allowed, try again: ")
        if response == "NO" or response == "No" or response == "no":
            notDoneEntering = False

    #creating and sorting debt arrays for avalanche method and snowball method
    snowball = copy.deepcopy(debts)
    avalanche = copy.deepcopy(debts)

    snowball1 = sorted(snowball, key=itemgetter(0))
    avalanche1 = sorted(avalanche, key=itemgetter(1), reverse=True)

    #determining monthly payment
    monthlyPayment = validateNumberGreaterThanZero("Enter the dollar amount you will be putting towards paying "
                                                   "off these debts monthly: ")
    #running snowball simulation
    snowMonths, snowInterest, paymentTooSmall = debtSimulatorFunction(snowball1, "snowball", monthlyPayment)

    if paymentTooSmall:
        return

    #running avalanche simulation
    avalancheMonths, avalancheInterest, paymentTooSmall = debtSimulatorFunction(avalanche1, "avalanche", monthlyPayment)

    if paymentTooSmall:
        return

    #calculating differences in time and money between the two different methods
    costDifference = snowInterest - avalancheInterest
    monthDifference = snowMonths - avalancheMonths

    #Messages regarding comparing the avalanche and snowball methods
    print("Using the avalanche method, you will pay " + "${:,.0f}".format(int(costDifference)) +
          " dollars less than the snowball method")
    sleep(3)

    if monthDifference == 1:
        print("Using the avalanche method you will pay the debt off roughly " + str(monthDifference) + " month faster")
        sleep(3)

    elif monthDifference < 12:
        print("Using the avalanche method you will pay the debt off roughly " + str(monthDifference) + " months faster")
        sleep(3)

    elif monthDifference > 12:

        yearDif, monthDif = divmod(monthDifference, 12)

        if monthDif != 1:
            print("Using the avalanche method you will pay the debt off roughly " + str(yearDif) + " years and "
                  + str(monthDif) + " months faster")
            sleep(3)
        elif monthDif == 1:
            print("Using the avalanche method you will pay the debt off roughly " + str(yearDif) + " years and "
                  + str(monthDif) + " month faster")
            sleep(3)

    #saving debts for next time
    print("\nSaving debt information for use next time")
    with open("debts.csv", mode='wt', newline="") as file1:

        csv_writer = csv.writer(file1)
        header = ["Debts", "Rates"]
        csv_writer.writerow(header)
        for element in debts:
            csv_writer.writerow(element)


def debtSimulatorFunction(sortedArray, methodName, monthlyPayment):
    """ Runs simulation of debt repayment process."""

    #calculate total debt amount at beginning of simulation
    startingDebt = sumDebts(sortedArray)
    print("\nStarting debt amount: " + "${:,.0f}".format(int(startingDebt)))
    sleep(2)

    # starts month counter at 1 so that if you pay it off in the first month, still says it took 1 month to pay off
    # this means all times displayed are rounded up to next month
    # also starts variable for storing interest paid
    MonthCounter = 1
    totalInterestPaid = 0

    #start of the loop for running the entire simulation
    while len(sortedArray) > 0:

        # make a new thisPayment to work with for this month
        thisPayment = monthlyPayment

        # subtract the monthly interest of each debt from the monthly payment
        for i in range(len(sortedArray)):

            monthInterestRate = ((sortedArray[i][1]) / 100) / 12
            monthMinPayment = monthInterestRate * sortedArray[i][0]
            totalInterestPaid += monthMinPayment
            thisPayment -= monthMinPayment

            # if the payment does not even cover the interest, stops the simulation
            if thisPayment < 0:
                print("Monthly payment entered does not cover at least the monthly interest of debts")
                return 0, 0, True

        # Uses the remaining amount in the monthly payment to pay off the debts
        while thisPayment > 0:

            if len(sortedArray) > 0:

                #if remaining payment is greater than next debt
                if thisPayment >= sortedArray[0][0]:
                    thisPayment -= sortedArray[0][0]
                    sortedArray.pop(0)

                # if remaining payment is less than next debt
                elif thisPayment < sortedArray[0][0]:
                    sortedArray[0][0] -= thisPayment
                    thisPayment = 0

            #if no debts remain
            elif len(sortedArray) == 0:

                #paid off in 1 month message
                if MonthCounter == 1:
                    print("All debts have been paid off by the " + methodName + " method in roughly " + str(
                        MonthCounter) + " month")
                    sleep(3)

                # paid off between 1-12 months message
                elif MonthCounter < 12:
                    print("All debts have been paid off by the " + methodName + " method in roughly " + str(
                        MonthCounter) + " months")
                    sleep(3)

                # paid off in over 1 year message
                elif MonthCounter > 12:

                    year1, month1 = divmod(MonthCounter, 12)

                    if month1 != 1:
                        print("The " + methodName + " method will take roughly " + str(year1) + " years and " + str(
                            month1) + " months to pay off the debt.")
                        sleep(3)

                    elif month1 == 1:
                        print("The " + methodName + " method will take roughly " + str(year1) + " years and " + str(
                            month1) + " month to pay off the debt.")
                        sleep(3)

                #Total amount and total interest paid using this method messages
                print("The amount of interest paid using the " + methodName + " method is " +
                      "${:,.0f}".format(int(totalInterestPaid)))
                sleep(3)
                print("The total amount paid using the " + methodName + " method is " +
                      "${:,.0f}".format(int(totalInterestPaid + startingDebt)) + "\n")
                sleep(3)

                #end this specific simulation
                return MonthCounter, totalInterestPaid, False

        #keeping track of the months
        MonthCounter += 1

        # trackers that display the remaining debt at certain time points
        # we need an extra month for all these year ranges because we started with 1 with the counter
        if MonthCounter == 13:
            print("Debt remaining after 1 year of the " + methodName +
                  " method is " + "${:,.0f}".format(int(sumDebts(sortedArray))) +
                  "  (" + str(currentDate.year + 1) + ")")
            sleep(3)

        elif MonthCounter == 25:
            tracker(methodName, sortedArray, 2)
        elif MonthCounter == 61:
            tracker(methodName, sortedArray, 5)
        elif MonthCounter == 121:
            tracker(methodName, sortedArray, 10)
        elif MonthCounter == 301:
            tracker(methodName, sortedArray, 25)
        elif MonthCounter == 601:
            tracker(methodName, sortedArray, 50)


def sumDebts(debts):
    """ Adds up all current debts."""

    holder = 0
    for i in range(len(debts)):
        holder += debts[i][0]

    return int(holder)


def loadStoredData():
    """ Loads previous saved data from CSV storage."""

    with open("debts.csv", mode='r', newline='') as file1:

        csv_reader = csv.reader(file1)
        next(csv_reader)
        savedElements = []

        for row in csv_reader:

            element = [int(row[0]), int(row[1])]
            savedElements.append(element)

        return savedElements


def validateNumberGreaterThanZero(message):
    """ Validates user inputted numbers."""

    badInput = True
    while badInput:
        try:
            response = int(input(message))

            while response <= 0:
                response = int(input("Only positive amounts greater than 0 allowed. Try again: "))
            badInput = False
        except ValueError:
            print("Only numbers allowed")
    return response


def tracker(methodName, sortedArray, years):
    """ Provides information regarding debt remaining after certain time periods."""

    print("Debt remaining after " + str(years) + " years of the " + methodName +
          " method is " + "${:,.0f}".format(int(sumDebts(sortedArray))) + "  (" + str(currentDate.year + years) + ")")
    sleep(3)
