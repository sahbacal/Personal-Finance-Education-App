from flowchartGuide import flowchartGuide

from debtRepayment import debtRepayment
from functions import grabQuotes, displayQuote
from time import sleep
from retirementSavings import retirementSavings


def main():
    """ Provides main control flow for personal finance app."""

    quoteList = []
    grabQuotes(quoteList)
    lenList = len(quoteList)
    print("Welcome to the Personal Finance Guidance and Utility program!")
    sleep(2)
    displayQuote(lenList, quoteList)
    sleep(3)
    print("The goal of this program is to help provide the tools and knowledge needed to help anyone\n"
          "on the route to financial stability.\n")
    sleep(3)
    print("To use this program's utilities, input the following words and then press Enter")
    sleep(3)
    print("For the Debt Repayment Simulator, use 'REPAY'")
    print("For the Retirement Savings Simulator, use 'SAVE'")
    print("For the Personal Finance flowchart guide, use 'GUIDE'")
    sleep(0)

    acceptedAnswers = ["REPAY", "Repay", "repay", "SAVE", "Save", "save", "guide", "Guide", "GUIDE"]

    response = input("Enter utility:")
    while response not in acceptedAnswers:
        response = input("only designated words allowed, try again: ")
    if response == "REPAY" or response == "repay" or response == "Repay":
        debtRepayment()
    elif response == "SAVE" or response == "Save" or response == "save":
        retirementSavings()
    elif response == "GUIDE" or response == "guide" or response == "Guide":
        flowchartGuide()


if __name__ == '__main__':
    main()
