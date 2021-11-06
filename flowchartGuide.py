
from functions import budget, welcome, grabQuotes, displayQuote, emergencyFund, employerMatch, eliminateDebt
from functions import iraEducation, retirementSaving, advancedMethods
from time import sleep


def flowchartGuide():
    """ Provides control flow for the personal finance flowchart guide."""

    quoteList = []
    grabQuotes(quoteList)
    lenList = len(quoteList)
    welcome()
    input("Press enter to begin:\n")
    budget(lenList, quoteList)
    input("\nPress enter to proceed to the next step:\n")
    emergencyFund(lenList, quoteList)
    input("\nPress enter to proceed:\n")
    employerMatch(lenList, quoteList)
    input("\nPress enter to proceed to the next step:\n")
    eliminateDebt(lenList, quoteList)
    input("\nPress enter to proceed to the next step:\n")
    iraEducation(lenList, quoteList)
    input("\nPress enter to proceed to the next step:\n")
    retirementSaving(lenList, quoteList)
    input("\nPress enter to proceed to the next step:\n")
    advancedMethods(lenList, quoteList)


if __name__ == '__main__':
    flowchartGuide()
