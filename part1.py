import csv
import time
from operator import itemgetter 									#lambda is slower in this case
startTime = time.time()
filename='Beijing_restaurants.txt'
coordList=[]						

def findLimits():
	
	with open(filename, 'r', encoding='UTF-8') as df1:
		
		lineNum=0			
		
		try:
			df1.__next__() 											#skipping the first line 
		except StopIteration:
			print('StopIteration')	
		
		maxX=0														#all greater than 0
		maxY=0														#all greater than 0
		minX=200													#around 40
		minY=200													#around 116
		
		for row in df1:
			
			lineNum+=1
			fixedData=fixData(lineNum, row)
			coordList.append(fixedData)
			
			if fixedData[1]>maxX:
				maxX=fixedData[1]
			elif fixedData[1]<minX:
				minX=fixedData[1]
			if fixedData[2]>maxY:
				maxY=fixedData[2]
			elif fixedData[2]<minY:
				minY=fixedData[2]
	
		return minX, maxX, minY, maxY 								#tuple

def fixData(lineNum, line):

	rawData=line.split(' ')	
	#print(rawData)											#['39.865999', '116.26745\n']
			
	splitXY=[i.split(',') for i in rawData]	
	#print(splitXY)											# [['39.865999'], ['116.26745\n']]		
	floatData= [float(j) for i in splitXY for j in i]		#transform strings to floats	
	#print(floatData)										#[39.865999, 116.26745]
	floatData.insert(0,lineNum)								#insert identifiers in the beggining 
	#print(floatData)										#[51959, 39.865999, 116.26745]
	return floatData

		
def sortingX(lists):

	return sorted(lists, key=itemgetter(1))

def sortingY(lists):

	return sorted(lists, key=itemgetter(2))

def makeGrid(bound):
	
	rangeX=(bound[1]-bound[0])/10
	rangeY=(bound[3]-bound[2])/10
	print('------')
	print(rangeX)
	print(rangeY)
	print('------')
	


if __name__ == "__main__":

	boundaries=findLimits()								#the results "boundaries" should be the first line in grid.dir
	
	#print(coordList)									#e.g: [...[51951, 39.947793, 116.192175], [51952, 39.925906, 116.438004]...]
	xSort=sortingX(coordList)
	ySort=sortingY(coordList)
	#print(xSort)										#e.g: [...[37616, 40.179829, 116.164818], [27786, 40.179911, 116.40583]]
	#print(ySort)										#e.g: [...[1140, 40.082111, 116.719937], [48288, 39.95366, 116.719976]]
	makeGrid(boundaries)
	print(boundaries)
	print("--- %s seconds ---" % (time.time() - startTime))
