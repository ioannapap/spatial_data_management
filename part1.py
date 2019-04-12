import csv
import time
import math
import operator
startTime = time.time()
filename='Beijing_restaurants.txt'
coordDict=[{0 : 51970}]							#about to make dictionary...this is the first default line



def findLimits():
	with open(filename, 'r', encoding='UTF-8') as df1:
		lineNum=0			
		try:
			df1.__next__() 								#skipping the first line 
		except StopIteration:
			print('StopIteration')	
		
		maxX=0											#all greater than 0
		maxY=0											#all greater than 0
		minX=200										#around 40
		minY=200										#around 116
		
		for row in df1:
			lineNum+=1
			rawData=row.split(' ')						
			fixedData= [float(i) for i in rawData]		#transform strings to floats		
			
			addIdentifiers(lineNum, fixedData)			#identifier for every line 	
			
			if fixedData[0]>maxX:
				maxX=fixedData[0]
			elif fixedData[0]<minX:
				minX=fixedData[0]
			if fixedData[1]>maxY:
				maxY=fixedData[1]
			elif fixedData[1]<minY:
				minY=fixedData[1]
		
		return minX, maxX, minY, maxY 


def addIdentifiers(line, spot):

	coordDict.append({line : spot})

def sorting(lis):

	print(sorted(lis, key=lambda i: i.values()))

def makeGrid(bound):
	temp=list()
	rangeX=(bound[1]-bound[0])/10
	rangeY=(bound[3]-bound[2])/10
	print(rangeX)
	print(rangeY)
	
	




if __name__ == "__main__":

	boundaries=findLimits()								#the results "boundaries" should be the first line in grid.dir
	print(boundaries)
	
	print(coordDict) # 51900: [39.899093, 116.21044], 51901: [39.940503, 116.313144], 51902: [39.986791, 116.703016]
	sorting(coordDict)
	makeGrid(boundaries)
	
	print("--- %s seconds ---" % (time.time() - startTime))
