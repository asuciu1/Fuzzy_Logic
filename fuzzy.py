from __future__ import division
import re, sys
from func import *
from collections import OrderedDict, Counter


def main():
  #parse the file in a list
  myList = loadFile("example4.txt")

  #store the empty rows locations
  spaces = eSpaces(myList)

  #parse the rules from file to dictionary
  rules = parse(myList, spaces[0], spaces[1])

  #inputs from the end of the file
  inputs = getInputs(spaces, myList)

  #get the variables from the file
  fuz = getFuzzy(spaces, myList)

  #start fuzzifier
  print( "#->> Fuzzification <<-#")

  #get fuzzy set in a dictionary (4-tuples -> machine readable format)
  fuzzyset = makeFuzzy(inputs, fuz)
  print("\nFiring of the rules:")

  #get the rules firing after fuzzification
  rulesContr = getRulesC(fuzzyset, rules)

  #check for duplicate rules
  a = []
  duplicateRules = Counter([rulesContr[i][0] for i in rulesContr.keys()])
  for i in duplicateRules.keys():
    if duplicateRules[i] > 1:
      a.append(i)

  #combine the rules using OR if there are duplicates
  combinedRules = combRules(a, rulesContr)

  #what is the action for the fuzzy system (eg. tip)
  action = strip(myList[spaces[-3]+1]).replace(' ','')

  #start defuzification
  print("\n\n#->> Defuzzification <<-#\n")

  #get the areas from the fuzzy variables, combined rules and the action
  print("Area")
  areas = getArea(fuz, combinedRules, action)

  #get the centres from the fuzzy variables, combined rules and the action
  print("\nCentres")
  centres = getCentres(fuz, combinedRules, action)

  #get the sum of AiXi and sum of Ai parameters for the final sum division
  AiXi = float()
  Ai   = float()
  for i in areas.keys():
    AiXi += areas[i]*centres[i]
    Ai   += areas[i]

  #print the defuzzified value
  print("The defuzzified value is "+ str(AiXi/Ai) + " from the lhs")

if __name__ == '__main__':
  main()