import csv
import random
from time import sleep


def grabQuotes(quoteList):
    """ Retrieves quotes from csv storage."""

    with open("quotes.csv", mode='r', newline='') as file1:

        csv_reader = csv.reader(file1)
        for row in csv_reader:
            quoteList.append(row)


def displayQuote(lenList, quoteList):
    """ Displays a random quote. """

    nextQuote = random.randint(0, lenList-1)
    print("Quote: " + quoteList[nextQuote][0] + "\n")


def welcome():
    """ Displays introduction to the personal finance app."""

    print("\nWelcome to the Personal Finance education command line program!")
    sleep(3)
    print("Here you will complete an interactive version of the \nReddit:Personal "
          "Finance 7 step flowchart plan\n")
    sleep(4)


def budget(lenList, quoteList):
    """ Displays introduction to the budgeting step."""

    print("Congrats on making it to step 1!  [(1) 2 3 4 5 6 7]   Essential Budget")
    sleep(3)
    displayQuote(lenList, quoteList)
    sleep(4)
    print("The first step to sound personal finance is creating a budget regarding "
          "your essentials each month.\nWe will start by checking in on your monthly budget items\n")
    sleep(4)
    budgetQuestion("rent/mortgage")
    budgetQuestion("food/groceries")
    budgetQuestion("essentials(utilities (power/heat), toiletries, etc)")
    budgetQuestion("income earning essentials(car insurance, gas, phone bill, etc)")
    budgetQuestion("health care/insurance")
    budgetQuestion("minimum monthly payments on all debts and loans(student loans, credit cards)")
    sleep(1)
    print("\nYou have completed step 1 and have a sound budget to work from.")
    sleep(2)


def budgetQuestion(text):
    """ Queries users regarding budgeting information."""

    acceptedYesAnswers = ["yes", "Yes", "YES"]
    acceptedNoAnswers = ["no", "No", "NO"]

    responseIsNo = True
    while responseIsNo:
        response = input("Have you budgeted for " + text + "? ")
        while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
            response = input("only yes or no responses, try again: ")
        if response in acceptedNoAnswers:
            print("Budgeting for " + text + " should be one of your current goals, focus here and return"
                  " when completed")
        elif response in acceptedYesAnswers:
            responseIsNo = False


def emergencyFund(lenList, quoteList):
    """ Provides control flow for emergency fund step."""

    print("Congrats on making it to step 2!  [1 (2) 3 4 5 6 7]      Emergency Fund")
    sleep(3)
    displayQuote(lenList, quoteList)
    sleep(4)
    print("The next step to sound personal finance is building a small emergency fund.\nIn a"
          " bank account, save either 1000$ or enough money to cover 1 month of expenses, \ndepending "
          "on which is greater.\n")
    sleep(8)
    payingGoal(lenList, quoteList, "emergency fund")
    print('Before proceeding to the next step, now is the appropriate'
          ' time to cover any Non-Essential Bills, such as Cable, internet, etc.')
    sleep(3)


def employerMatch(lenList, quoteList):
    """ Provides control flow for employer match step."""

    acceptedYesAnswers = ["yes", "Yes", "YES"]
    acceptedNoAnswers = ["no", "No", "NO"]

    print("Congrats on making it to step 3!  [1 2 (3) 4 5 6 7]       Employer Match")
    sleep(3)
    displayQuote(lenList, quoteList)
    sleep(4)

    response = input("For this section, does your work offer retirement accounts with employer matching?: ")
    while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
        response = input("only yes or no responses, try again: ")
    if response in acceptedNoAnswers:
        print("In that case, we can proceed to step 4! If you end up switching jobs\n"
              "to one that offers employer matching, feel free to return to this step.")
        sleep(4)
    elif response in acceptedYesAnswers:

        badInput = True
        while badInput:
            try:
                employerDollar = int(input("What is the largest amount you can contribute "
                                           "to get the full employer match?: "))
                while employerDollar <= 0:
                    employerDollar = int(input("Only positive amounts greater than 0 allowed. Try again: "))
                badInput = False
            except ValueError:
                print("Only numbers allowed")
        goalAmount = employerDollar

        sleep(1)
        print("Maximizing the employer match should be one of your current goals.")
        sleep(2)
        print("Update this section as you contribute more money to the match.\n")
        sleep(5)

        response = 0
        while response < goalAmount:

            badInput = True
            while badInput:
                try:
                    response = int(
                        input("How much of the employer match of $" + str(goalAmount) + " have you "
                              "contributed to this year, in dollars?: "))

                    while response < 0:
                        response = int(input("Only positive values allowed. Try again: "))
                    badInput = False
                except ValueError:
                    print("Only numbers allowed")

            if response < goalAmount:
                print("Congratulations! "
                      "You have contributed " + str(round((response / goalAmount) * 100)) + "% " +
                      "of the employer match. Keep up the great work!")
                sleep(3)
                displayQuote(lenList, quoteList)
                sleep(4)

        sleep(1)
        print("You have maxed out the employer match! Congratulations!!!\n")
        sleep(2)


def eliminateDebt(lenList, quoteList):
    """ Provides control flow for eliminating debt step."""

    acceptedYesAnswers = ["yes", "Yes", "YES"]
    acceptedNoAnswers = ["no", "No", "NO"]

    print("Congrats on making it to step 4!  [1 2 3 (4) 5 6 7]    Eliminate High/Mid Interest debt")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)

    response = input("For this step, do you have any debts that are high interest (10% rate or higher)?: ")
    while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
        response = input("only yes or no responses, try again: ")
    if response in acceptedNoAnswers:
        print("In that case, we can move forward.")
        sleep(2)
    elif response in acceptedYesAnswers:
        payingDebt(lenList, quoteList, "high interest debt")

    print("Before we pay off any any additional debts, we will increase our emergency fund to cover living expenses"
          " for 3-6 months.")
    payingGoal(lenList, quoteList, "extended emergency fund")

    response = input("For the last part of step 4, do you have any debts that are mid interest "
                     "(4%-10% rate, not including mortgage)?: ")
    while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
        response = input("only yes or no responses, try again: ")
    if response in acceptedNoAnswers:
        print("In that case, we can move forward.")
        sleep(2)
    elif response in acceptedYesAnswers:

        payingDebt(lenList, quoteList, "mid interest debt")


def iraEducation(lenList, quoteList):
    """ Provides control flow for IRA savings step."""

    acceptedYesAnswers = ["yes", "Yes", "YES"]
    acceptedNoAnswers = ["no", "No", "NO"]

    print("Congrats on making it to step 5!  [1 2 3 4 (5) 6 7]    IRAs and Education expenses")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)

    print("For this step, we will start by building an IRA, or individual retirement account. \n"
          "The two types to consider are the Roth or Traditional IRA. Which type you use will depend on "
          "your circumstances. \n"
          "The maximum contribution per year for an individual under 50 is $6000.\n")
    sleep(5)
    payingGoal(lenList, quoteList, "IRA")

    response = input("For the next part of this step, do you expect to have any personal investments or large mandatory"
                     "\npurchases in the near future?(Degree, professional license, vehicle for a job))?: ")
    while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
        response = input("only yes or no responses, try again: ")
    if response in acceptedNoAnswers:
        print("In that case, we can move forward.")
        sleep(2)
    elif response in acceptedYesAnswers:

        payingGoal(lenList, quoteList, "personal investment")


def retirementSaving(lenList, quoteList):
    """ Provides control flow for retirement savings step."""

    acceptedYesAnswers = ["yes", "Yes", "YES"]
    acceptedNoAnswers = ["no", "No", "NO"]

    print("Congrats on making it to step 6!  [1 2 3 4 5 (6) 7]    Additional Retirement Saving")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)

    response = input("For this step, are you currently saving at least 15% of pre-tax income for retirement?: ")

    while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
        response = input("only yes or no responses, try again: ")
    if response in acceptedYesAnswers:
        print("That's great! In that case, we can move forward.")
        sleep(2)
    elif response in acceptedNoAnswers:

        print("Our current goal is saving 15% of pre-tax income for retirement. \n")
        sleep(3)
        print("If your employer offers retirement accounts such as a 401k, you can continue saving in these.")
        sleep(3)
        print("If you are self-employed, consider individual 401k, SIMPLE or SEP-Ira's to save in.")
        sleep(3)
        print("If neither of these apply, consider contributing to a taxable account for this purpose.\n")
        sleep(3)

        payingGoal(lenList, quoteList, "retirement savings (15% income)")


def advancedMethods(lenList, quoteList):
    """ Provides control flow for advanced methods step."""

    acceptedYesAnswers = ["yes", "Yes", "YES"]
    acceptedNoAnswers = ["no", "No", "NO"]

    print("Congrats on making it to step 7!  [1 2 3 4 5 6 (7)]    Advanced Methods")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)
    response = input("For this step, do you have a high deductible health insurance plan, \nmaking"
                     " you eligible for an HSA? (Health Savings Account): ")

    while response not in acceptedYesAnswers and response not in acceptedNoAnswers:
        response = input("only yes or no responses, try again: ")
    if response in acceptedNoAnswers:
        print("In that case, we can move forward. Return to this step if you ever enroll in one of these plans")
        sleep(2)
    elif response in acceptedYesAnswers:

        print("Your current goal should be to maximize your HSA contributions each year.\n")
        sleep(2)
        print("The current maximum allowable HSA contribution per year is $3,550 "
              "per year for individuals younger than 55.")

        payingGoal(lenList, quoteList, "HSA")

    print("At this point, there are several options on how to proceed forward with personal finance.\n")
    sleep(2)
    print("If you have children and want to help save for their college, use accounts such as the 529 to save money.")
    sleep(4)
    print("\nIf you would like to retire early, look into employer retirement accounts such as the 401k, \nlook"
          " into the mega backdoor Roth IRA, and then look into taxable accounts.\n")
    sleep(6)
    print("If you have more immediate goals, use a savings account to save for goals within 3-5 years, \n or"
          " use stocks and bonds to save for goals further away. \n")
    sleep(6)
    print("Congratulations on completing the Personal Finance interactive program! Best of luck with everything!\n")
    sleep(3)
    displayQuote(lenList, quoteList)


def payingDebt(lenList, quoteList, debtName):
    """ Reusable code block querying for debt repayment process."""

    badInput = True
    while badInput:
        try:
            highDebt = int(input("What is the total amount of the " + str(debtName) + "?: "))
            while highDebt <= 0:
                highDebt = int(input("Only positive amounts greater than 0 allowed. Try again: "))
            badInput = False
        except ValueError:
            print("Only numbers allowed")

    sleep(1)
    print("Eliminating " + str(debtName) + " should be one of your current goals.")
    sleep(2)
    print("Consider the Avalanche and Snowball methods according to your situation. "
          "\nUpdate this section as you continue to pay these off.\n")
    sleep(3)

    response = 100
    while response > 0:
        badInput = True
        while badInput:
            try:
                response = int(
                    input("How much of the original amount of " + str(debtName) + " remains"
                          ", in dollars?: "))

                while response < 0:
                    response = int(input("Only positive values or zero allowed. Try again: "))
                badInput = False
            except ValueError:
                print("Only numbers allowed")

        if response < highDebt:
            print("Congratulations! You have reduced the " + str(debtName) + " of $" + str(highDebt) +
                  " by " + str(round(((highDebt - response) / highDebt) * 100)) + "%! Keep up the great work!")
            sleep(3)
            displayQuote(lenList, quoteList)
            sleep(4)

    sleep(1)
    print("You have completely paid off all " + str(debtName) + "! Congratulations!!!\n")
    sleep(2)


def payingGoal(lenList, quoteList, goalName):
    """ Reusable code block for saving for a goal process."""

    badInput = True
    while badInput:
        try:
            response = int(input("Enter the goal amount in dollars you plan to save for your " + str(goalName) + ": "))
            while response <= 0:
                response = int(input("Only positive amounts greater than 0 allowed. Try again: "))
            badInput = False
        except ValueError:
            print("Only numbers allowed")
    goalAmount = response
    sleep(1)
    print("Building up this " + str(goalName) + " should be one of your current goals.")
    sleep(2)
    print("Update this section as you save more money.\n")
    sleep(3)

    response = 0
    while response < goalAmount:
        badInput = True
        while badInput:
            try:
                response = int(
                    input("How much of your $" + str(goalAmount) + " " + str(goalName) +
                          " have you completed, in dollars?: "))

                while response < 0:
                    response = int(input("Only positive values allowed. Try again: "))
                badInput = False
            except ValueError:
                print("Only numbers allowed")

        if response < goalAmount:
            print("Congratulations! "
                  "You have completed " + str(round((response / goalAmount) * 100)) + "% " +
                  "of your " + str(goalName) + ". Keep up the great work!")
            sleep(3)
            displayQuote(lenList, quoteList)
            sleep(4)

    sleep(1)
    print("You have completed your " + str(goalName) + "! Congratulations!!!\n")
    sleep(2)
