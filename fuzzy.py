f = open("example.txt", "r")
myList = []



for line in f:
  myList.append(line)

#exec(myList[0] "= 'something'")

for i in range(len(myList)):
  print myList[i].replace("the ", "").replace("is ", "").replace("\n", "")

print myList[0]
print myList[2]

#print(myList)