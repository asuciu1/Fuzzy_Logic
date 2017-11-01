import re, sys
from parse import *
from collections import OrderedDict

###VARIABLES###
f 					= open("example.txt", "r")
myList 			= []
spaces 			= []
dic 				= OrderedDict()
dic2 				= OrderedDict()
inputs 			= {}
regexp 			= re.compile(r'^\b(([a-z]+)*.([a-z]+))*[a-z]+\b(?!(\s(\d|=)))')
regexpbreap = re.compile(r'')
###############

for line in f:
  myList.append(line)

#exec(myList[0] "= 'something'")

for i in range(len(myList)):
	if myList[i] == "\n" or myList[i] == "\r\n":
		spaces.append(i)
  #print myList[i].replace("the ", "").replace("is ", "").replace("\n", "")
#r = parse("{variable}",myList[spaces[2]-1])

###inputs from the end of the file
for i in range(spaces[len(spaces)-1]+1, len(myList)):
	inputs[re.split(r'\s.\s',myList[i])[0]] 	\
		= re.split(r'\s.\s',myList[i])[1].replace('\r','').replace('\n','').replace(' ','')

###get the variables from the file
for i in range(len(myList)):
	if regexp.search(myList[i]) and i >= spaces[1] and i< spaces[len(spaces)-1]:
		for j in range(i+2,len(myList)):
			if j in spaces:
				break
			dic2[myList[j].split(' ', 1)[0]] = filter(None,re.split(r'\s', myList[j].split(' ', 1)[1]))
		dic[myList[i].split('\n',1)[0].replace('\r','').replace('\n','').replace(' ','')] = dic2
		dic2 = {}

print dic["driving"]["average"][2]
#print inputs
#[1, 6, 8, 12, 14, 18, 20, 24]