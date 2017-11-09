from __future__ import division
import re, sys
from func import *
from collections import OrderedDict, Counter


regexp  = re.compile(r'^\b(([a-z]+)*.([a-z]+))*[a-z]+\b(?!(\s(\d|=)))')

#########################################

def float3(String):
  return round(float(String),3)
  #return float(String)

def loadFile(String):
  f = open(String, "r")
  myList = []
  for line in f:
    myList.append(line)
  return myList

def eSpaces(List):
  spaces = []
  for i in range(len(List)):
      if List[i] == "\n" or List[i] == "\r\n":
        spaces.append(i)
  return spaces

def strip(String):
  return String.replace("the ", "") \
             .replace("is ", "")    \
             .replace("\n", "")     \
             .replace("\r", "")     \
             .replace("will ", "")  \
             .replace("to ", "")    \
             .replace("be ", "")

def getVars(List):
  var = OrderedDict()
  for i in range(2, len(List)):
    if List[i] == 'If':
      pass
    elif List[i] 	 == 'then' \
      or List[i+1] == 'then':
      break
    elif List[i] 	 == 'and'\
      or List[i] 	 == 'AND'\
      or List[i] 	 == 'or' \
      or List[i]	 == 'OR' \
      or List[i+1] == 'and'\
      or List[i+1] == 'AND'\
      or List[i+1] == 'or' \
      or List[i+1] == 'OR' :
      pass
    else:
      var[List[i]] = List[i+1]
      i+=1
  return var

def getLog(List):
  log = []
  for i in range(len(List)):
    if 	 List[i] 	 == 'and' \
      or List[i] 	 == 'AND' \
      or List[i] 	 == 'or'  \
      or List[i]	 == 'OR'  :
      log.append(List[i])
  return log

def getAction(List):
  action = OrderedDict()
  for i in range(len(List)):
    if List[i] == 'then':
      action[List[i+1]] = List[i+2]
  return action


def parse(List,start,stop):
  rules = OrderedDict()
  for i in range(start+1, stop):
    rules[re.split(r'\s', strip(List[i]))[0]   \
         + " "                                 \
         + re.split(r'\s', strip(List[i]))[1]  \
       ] = {"Variables": getVars  (re.split(r'\s', strip(List[i]))) ,\
          "and|or"   : getLog   (re.split(r'\s', strip(List[i])))   ,\
          "Actions"  : getAction(re.split(r'\s', strip(List[i])))    \
         }
  return rules

def getMin(List):
  min = List[0]
  for i in List:
    if i < min:
      min = i
  return min
def getMax(List):
  max = List[0]
  for i in List:
    if i > max:
      max = i
  return max

def getInputs(spaces, fileList):
  inputs = {}
  for i in range(spaces[len(spaces)-1]+1, len(fileList)):
    inputs[re.split(r'\s.\s',fileList[i])[0]] \
      = float3(strip(re.split(r'\s.\s',fileList[i])[1]).replace(' ',''))
  return inputs

def getFuzzy(spaces, fileList):
  fuz     = OrderedDict()
  fuz2    = OrderedDict()
  for i in range(len(fileList)):
    if regexp.search(fileList[i]) and i >= spaces[1] and i< spaces[len(spaces)-1]:
      for j in range(i+2,len(fileList)):
        if j in spaces:
          break
        fuz2[fileList[j].split(' ', 1)[0]] = [ float3(k) for k in filter(None,re.split(r'\s', fileList[j].split(' ', 1)[1]))]
      fuz[strip(fileList[i].split('\n',1)[0]).replace(' ','')] = fuz2
      fuz2 = OrderedDict()
  return fuz

def makeFuzzy(inputs, fuz):
  fuzzyset = {}
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
  return fuzzyset

def getRulesC(fuzzyset, rules):
  st = []
  rC = {}
  for k in rules.keys():
    for g in range(len(rules[k]['Variables'].keys())):
      st.append(fuzzyset[list(rules[k]['Variables'].keys())[g]][rules[k]['Variables'][list(rules[k]['Variables'].keys())[g]]])
    minmax = applyMinMax(rules[k]['and|or'],st)
    print(" " + k +": " + rules[k]['Actions'][list(rules[k]['Actions'].keys())[0]] + " = " + str(minmax))
    rC[k] = (rules[k]['Actions'][list(rules[k]['Actions'].keys())[0]], minmax)
    st = []
  return rC

def combRules(duplList, rulesCList):
  combinedRules = {}
  checked       = []
  orValues      = []
  if duplList:
    print("\nCombine contributions from rules using the OR relation:")
    for i in rulesCList.keys():
      if rulesCList[i][0] not in duplList:
        print(" " + rulesCList[i][0] +" = "+ str(rulesCList[i][1]))
        combinedRules[rulesCList[i][0]] = rulesCList[i][1]
      elif rulesCList[i][0] not in checked:
        checked.append(rulesCList[i][0])
        for j in rulesCList.keys():
          if rulesCList[j][0] == rulesCList[i][0]:
            orVars = rulesCList[i][0]
            orValues.append(rulesCList[j][1])
        combinedRules[orVars]  =  getMax(orValues)
    print(" " + orVars + " = " + str(getMax(orValues)))
  else:
    for i in rulesCList.keys():
      combinedRules[rulesCList[i][0]] = rulesCList[i][1]
  return combinedRules

def applyMinMax(operator, List):
  if not operator:
    return getMin(List)
  elif operator[0] == 'or' or operator[0] == 'OR':
    return getMax(List)
  elif operator[0] == 'and' or operator[0] == 'AND':
    return getMin(List)

def getArea(fuz, combinedRules, action):
  areas = {}
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
  return areas

def getCentres(fuz, combinedRules, action):
  previous = 0
  counter  = 0
  centres  = {}
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
  return centres
