from __future__ import division
import re, sys
from func import *
from collections import OrderedDict


###VARIABLES###
f 					= open("example2.txt", "r")
myList 			= []
spaces 			= []
fuz 				= OrderedDict()
fuz2 				= OrderedDict()
rules				= OrderedDict()
inputs 			= {}
regexp 			= re.compile(r'^\b(([a-z]+)*.([a-z]+))*[a-z]+\b(?!(\s(\d|=)))')
regexpbreap = re.compile(r'')
###############


###parse the file in a list
for line in f:
  myList.append(line)

###store the empty rows in file
for i in range(len(myList)):
	if myList[i] == "\n" or myList[i] == "\r\n":
		spaces.append(i)

###parse the rules from tile to dictionary
rules = parse(myList, spaces[0], spaces[1])

###inputs from the end of the file
for i in range(spaces[len(spaces)-1]+1, len(myList)):
	inputs[re.split(r'\s.\s',myList[i])[0]] 	\
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
for k_i in inputs.keys():
	print k_i + "=" + str(inputs[k_i])
	for k_j in fuz[k_i].keys():

		#print k_j 
		#print fuz[k_i][k_j]

		#outside
		if inputs[k_i] < fuz[k_i][k_j][0] - fuz[k_i][k_j][2]:
			print "u("+ k_j +") = 0"
		elif inputs[k_i] > fuz[k_i][k_j][1] + fuz[k_i][k_j][3]:
			print "u("+ k_j +") = 0"
		#inside
		elif inputs[k_i] < fuz[k_i][k_j][1] + fuz[k_i][k_j][3] \
				and inputs[k_i] > fuz[k_i][k_j][0] - fuz[k_i][k_j][2]:
			if inputs[k_i] >= fuz[k_i][k_j][0] and inputs[k_i] <= fuz[k_i][k_j][1]:
				print "u("+ k_j +") = 1"
			#alpha
			elif inputs[k_i] < fuz[k_i][k_j][0] \
					and inputs[k_i] > fuz[k_i][k_j][0] - fuz[k_i][k_j][2]:
				value = (inputs[k_i] 			\
							- fuz[k_i][k_j][0] 	\
							+ fuz[k_i][k_j][2])	\
							/ fuz[k_i][k_j][2]
				#print "(" + fuz[k_i][k_j][0] + "+" + fuz[k_i][k_j][2] + "-" + inputs[k_i] + ")/"+ fuz[k_i][k_j][2] + "=" + str(value)
				print "u("+ k_j +") = " + str(float3(value))
			#beta
			elif inputs[k_i] > fuz[k_i][k_j][1] \
					and inputs[k_i] < fuz[k_i][k_j][1] + fuz[k_i][k_j][3]:
				value = (fuz[k_i][k_j][1] 	\
							+ fuz[k_i][k_j][3]		\
							- inputs[k_i])				\
							/ fuz[k_i][k_j][3]
				#print "(" + fuz[k_i][k_j][1] + "+" + fuz[k_i][k_j][3] + "-" + inputs[k_i] + ")/"+ fuz[k_i][k_j][3] + "=" + str(value)
				print "u("+ k_j +") = " + str(float3(value))
#print fuz
#print inputs
print rules['Rule 1']['Variables']
#[1, 6, 8, 12, 14, 18, 20, 24]