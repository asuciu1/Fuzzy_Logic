import re, sys
from collections import OrderedDict


f 			= open("example2.txt", "r")
rules		= OrderedDict()
log			= []
var 		= OrderedDict()
action 	= OrderedDict()

#########################################
def float3(String):
	return round(float(String),3)

def strip(String):
	return String.replace("the ", "") 	\
							 .replace("is ", "") 		\
							 .replace("\n", "") 		\
							 .replace("\r", "") 		\
							 .replace("will ", "") 	\
							 .replace("to ", "")		\
							 .replace("be ", "")

def getVars(List):
	var = OrderedDict()
	for i in range(2, len(List)):
		if List[i] == 'If':
			pass
		elif List[i] 	 == 'then'\
			or List[i+1] == 'then':
			break
		elif List[i] 	 == 'and' \
			or List[i] 	 == 'AND' \
			or List[i] 	 == 'or' 	\
			or List[i]	 == 'OR'	\
			or List[i+1] == 'and' \
			or List[i+1] == 'AND' \
			or List[i+1] == 'or' 	\
			or List[i+1] == 'OR'	:
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
			or List[i] 	 == 'or' 	\
			or List[i]	 == 'OR'	:
			log.append(List[i])
	return log

def getAction(List):
	action = OrderedDict()
	for i in range(len(List)):
		if List[i] == 'then':
			action[List[i+1]] = List[i+2]
	return action


def parse(List,start,stop):
	for i in range(start+1, stop):
		rules[	re.split(r'\s', strip(List[i]))[0] 	\
					+ " "																	\
					+ re.split(r'\s', strip(List[i]))[1]	\
				 ] = {"Variables": getVars		(re.split(r'\s', strip(List[i]))) ,\
				 			"and|or"		: getLog		(re.split(r'\s', strip(List[i]))) ,\
				 			"Actions"	: getAction	(re.split(r'\s', strip(List[i])))	\
				 		 }
	return rules