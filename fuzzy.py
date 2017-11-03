from __future__ import division
import re, sys
from func import *
from collections import OrderedDict, Counter


###VARIABLES###

myList        = [] #list of the text contained in the example file
spaces        = [] #list of the location of empty spaces in the file
st            = [] #used to store temporary values for parsing from rules in order to apply min/max
a             = [] #list of duplicate rules for combining contributions
checked       = [] #used to store a list of already checked values
orValues      = [] #used to identify the values when rules are fired
orVars        = [] #used to identify the operator when rules are fired. this is important for deciding between min/max
fuzzyset      = {} #stores the Mu values after fuzzification
inputs        = {} #values at the end of file key<--name, value<--numeric_value
rulesContr    = {} #stores the values after 'Firing of the rules' section in a machine readable way. enables combining duplicate rules by using OR in the next step 
combinedRules = {} #combined rulesContr values into a combined dictionary
areas         = {} #list of areas
centres       = {} #list of centres --> same order as areas
AiXi          = float() #area * centre
Ai            = float() #area
fuz           = OrderedDict() #contains the parsed values from the file(ie. fuzzy categories and the 4tuples)
fuz2          = OrderedDict() #used to create the fuz dictionary
rules         = OrderedDict() #parsed rules from the file in a machine readable format
regexp        = re.compile(r'^\b(([a-z]+)*.([a-z]+))*[a-z]+\b(?!(\s(\d|=)))') #used to identify the variables and their values (ie. temperature)
###############

### vvv mess starts here -- clean up vvv ##

###parse the file in a list
myList = loadFile("example.txt")

###store the empty rows locations
spaces = eSpaces(myList)

###parse the rules from file to dictionary
rules = parse(myList, spaces[0], spaces[1])

###inputs from the end of the file
for i in range(spaces[len(spaces)-1]+1, len(myList)):
  inputs[re.split(r'\s.\s',myList[i])[0]] \
    = float3(strip(re.split(r'\s.\s',myList[i])[1]).replace(' ',''))

###get the variables from the file
for i in range(len(myList)):
  if regexp.search(myList[i]) and i >= spaces[1] and i< spaces[len(spaces)-1]:
    for j in range(i+2,len(myList)):
      if j in spaces:
        break
      fuz2[myList[j].split(' ', 1)[0]] = [ float3(k) for k in filter(None,re.split(r'\s', myList[j].split(' ', 1)[1]))]
    fuz[strip(myList[i].split('\n',1)[0]).replace(' ','')] = fuz2
    fuz2 = OrderedDict()

###fuzzifier
print( "###Fuzzification###")
for k_i in inputs.keys():
  print("\n" + k_i + " = " + str(inputs[k_i]))
  for k_j in fuz[k_i].keys():
    #outside
    if inputs[k_i] < fuz[k_i][k_j][0] - fuz[k_i][k_j][2]:
      print(" u("+ k_j +") = 0")
      if k_i in fuzzyset:
        fuzzyset[k_i][k_j] = 0
      else:
        fuzzyset[k_i] = {k_j: 0}
    elif inputs[k_i] > fuz[k_i][k_j][1] + fuz[k_i][k_j][3]:
      print(" u("+ k_j +") = 0")
      if k_i in fuzzyset:
        fuzzyset[k_i] = {k_j: 0}
      else:
        fuzzyset[k_i] = {k_j: 0}
    #inside
    elif inputs[k_i] < fuz[k_i][k_j][1] + fuz[k_i][k_j][3] \
      and inputs[k_i] > fuz[k_i][k_j][0] - fuz[k_i][k_j][2]:
      if inputs[k_i] >= fuz[k_i][k_j][0] and inputs[k_i] <= fuz[k_i][k_j][1]:
        print(" u("+ k_j +") = 1")
        if k_i in fuzzyset:
          fuzzyset[k_i][k_j] = 1
        else:
          fuzzyset[k_i] = {k_j: 1}
      #alpha
      elif inputs[k_i] < fuz[k_i][k_j][0] \
        and inputs[k_i] > fuz[k_i][k_j][0] - fuz[k_i][k_j][2]:
        value = (inputs[k_i]       \
              - fuz[k_i][k_j][0]   \
              + fuz[k_i][k_j][2])  \
              / fuz[k_i][k_j][2]
        print(" u("+ k_j +") = " + str(float3(value)))
        if k_i in fuzzyset:
          fuzzyset[k_i][k_j] = float3(value)
        else:
          fuzzyset[k_i] = {k_j: float3(value)}
      #beta
      elif inputs[k_i] > fuz[k_i][k_j][1] \
        and inputs[k_i] < fuz[k_i][k_j][1] + fuz[k_i][k_j][3]:
        value = (fuz[k_i][k_j][1]  \
              + fuz[k_i][k_j][3]   \
              - inputs[k_i])       \
              / fuz[k_i][k_j][3]
        print(" u("+ k_j +") = " + str(float3(value)))
        if k_i in fuzzyset:
          fuzzyset[k_i][k_j] = float3(value)
        else:
          fuzzyset[k_i] = {k_j: float3(value)}


print(" ")
print("Firing of the rules:")
for k in rules.keys():
  for g in range(len(rules[k]['Variables'].keys())):
    st.append(fuzzyset[list(rules[k]['Variables'].keys())[g]][rules[k]['Variables'][list(rules[k]['Variables'].keys())[g]]])
  minmax = applyMinMax(rules[k]['and|or'],st)
  print(" " + k +": " + rules[k]['Actions'][list(rules[k]['Actions'].keys())[0]] + " = " + str(minmax))
  rulesContr[k] = (rules[k]['Actions'][list(rules[k]['Actions'].keys())[0]], minmax)
  st = []

duplicateRules = Counter([rulesContr[i][0] for i in rulesContr.keys()])
for i in duplicateRules.keys():
  if duplicateRules[i] > 1:
    a.append(i)

if a:
  print("\nCombine contributions from rules using the OR relation:")
  for i in rulesContr.keys():
    if rulesContr[i][0] not in a:
      print(rulesContr[i][0] +" = "+ str(rulesContr[i][1]))
      combinedRules[rulesContr[i][0]] = rulesContr[i][1]
    elif rulesContr[i][0] not in checked:
      checked.append(rulesContr[i][0])
      for j in rulesContr.keys():
        if rulesContr[j][0] == rulesContr[i][0]:
          orVars = rulesContr[i][0]
          orValues.append(rulesContr[j][1])
      combinedRules[orVars]  =  getMax(orValues)
  print(orVars + " = " + str(getMax(orValues)))
else:
  for i in rulesContr.keys():
    combinedRules[rulesContr[i][0]] = rulesContr[i][1]
  #print( combinedRules
print(" ")
#print( fuz["change_in_current"]
action = strip(myList[spaces[-3]+1]).replace(' ','')
print("\n###Defuzzification###\n")
print("Area")
for i in fuz[action].keys():
    if combinedRules[i] == 0:
     continue
    else:
        Length = float3((fuz[action][i][1]  \
               - fuz[action][i][0]          \
               + fuz[action][i][2]          \
               + fuz[action][i][3]))

        length = float3((fuz[action][i][1]  \
               - fuz[action][i][0]          \
               + fuz[action][i][2]          \
               + fuz[action][i][3])         \
               * (1.0 - combinedRules[i]))
    
        height = combinedRules[i]


        print(" " + i + " area is " + str(float3(((Length+length)*height)/2)))
        areas[i] = float3(((Length+length)*height)/2)
print(" ")

print("Centres are:")
previous = 0
counter  = 0

for i in fuz[action].keys():
  if combinedRules[i] == 0:
    if counter == 0:
      start = fuz[action][i][0] - fuz[action][i][2]
      counter = 1
    continue
  else:
    if counter == 0:
      start   = fuz[action][i][0] - fuz[action][i][2]
      counter = 1
    centre   = abs((fuz[action][i][0] + fuz[action][i][1])/2 - start)
    previous = centre
    print( " " + i +" centre is "+ str(centre))
    centres[i] = centre


for i in areas.keys():
  AiXi += areas[i]*centres[i]
  Ai   += areas[i]

print("The defuzzified value is "+ str(AiXi/Ai) + " from the lhs")
#print( fuz[action]
