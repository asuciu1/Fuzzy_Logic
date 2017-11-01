import re, sys
from parse import *
from collections import OrderedDict

###VARIABLES###
f 					= open("example3.txt", "r")
myList 			= []
spaces 			= []
fuz 				= OrderedDict()
fuz2 				= OrderedDict()
rules				= OrderedDict()
inputs 			= {}
regexp 			= re.compile(r'^\b(([a-z]+)*.([a-z]+))*[a-z]+\b(?!(\s(\d|=)))')
regexpbreap = re.compile(r'')
###############

###FUNCTIONS###
def strip(String):
	return String.replace("the ", "") 	\
							 .replace("is ", "") 		\
							 .replace("\n", "") 		\
							 .replace("\r", "") 		\
							 .replace("will ", "") 	\
							 .replace("be ", "")		\
###############


for line in f:
  myList.append(line)

#exec(myList[0] "= 'something'")

for i in range(len(myList)):
	if myList[i] == "\n" or myList[i] == "\r\n":
		spaces.append(i)

###parse the rules from tile to dictionary
for i in range(spaces[0]+1, spaces[1]):
	r = parse("{rule} If {variable1} {value1} {logicalconn} {variable2} {value2} then {action} {actionval}" \
			, strip(myList[i]))
	rules[r["rule"]] = r

###inputs from the end of the file
for i in range(spaces[len(spaces)-1]+1, len(myList)):
	inputs[re.split(r'\s.\s',myList[i])[0]] 	\
		= strip(re.split(r'\s.\s',myList[i])[1]).replace(' ','')

###get the variables from the file
for i in range(len(myList)):
	if regexp.search(myList[i]) and i >= spaces[1] and i< spaces[len(spaces)-1]:
		for j in range(i+2,len(myList)):
			if j in spaces:
				break
			fuz2[myList[j].split(' ', 1)[0]] = filter(None,re.split(r'\s', myList[j].split(' ', 1)[1]))
		fuz[strip(myList[i].split('\n',1)[0]).replace(' ','')] = fuz2
		fuz2 = OrderedDict()
"""
for keys in inputs.keys():
	print keys + "=" + inputs[keys]
	print fuz[keys]
"""


print fuz
print inputs
print rules
#[1, 6, 8, 12, 14, 18, 20, 24]