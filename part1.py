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
	
		return [minX, maxX, minY, maxY] 						

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

def theGrid(cList, boundaries):

	dividedRangeX=(boundaries[1]-boundaries[0])/10
	dividedRangeY=(boundaries[3]-boundaries[2])/10
	#print(dividedRangeX)
	#print(dividedRangeY)
	cell=0
	counter=0
	belongsToCell=[]
	firstTime=1
	with open('grid.grd', 'w+', encoding='UTF-8') as dfgrid, open('grid.dir', 'w+', encoding='UTF-8') as dfdir: #write and reading
		
		for x in range(10):
			for y in range(10):
				for sublist in cList:
					#sublist[1]=xcoordinate sublist[2]=ycoordinate
					if sublist[1]>=boundaries[0] and sublist[1]<boundaries[0]+((x+1)*dividedRangeX) and sublist[2]>=boundaries[2] and sublist[2]<boundaries[2]+((y+1)*dividedRangeY):
						belongsToCell.insert(len(belongsToCell), sublist)
						counter+=1
						if firstTime==1:
							firstRestaurant=[x,y, sublist[0]]
							firstTime=0
				
				#sorted(belongsToCell, key=itemgetter(0)) 						#sort the cell by its identifier
				
				print(belongsToCell) #[51791, 39.745316, 116.152629], [51800, 39.730122, 116.11868], [51821, 39.779803, 116.178883]
				cell+=1
				print('---------------------------------next cell %d ----------------------------------------------' % cell)
				'''
				#write grid.grd
				for i in belongsToCell:
					dfgrid.write(i)
				'''
				firstRestaurant.insert(3, counter)
				print(firstRestaurant)
				'''
				#write grid.dir
				dfdir.write(firstRestaurant)
				'''
				counter=0														#because we are moving to the next cell
				firstTime=1														#because we are moving to the next cell 
				break			
			break



if __name__ == "__main__":

	boundaries=findLimits()									#the results "boundaries" should be the first line in grid.dir
	#print(boundaries)
	#print(coordList)											#e.g: [...[51951, 39.947793, 116.192175], [51952, 39.925906, 116.438004]...]
	#xSortedCoordList=sorted(coordList, key=itemgetter(1))
	#ySortedCoordList=sorted(coordList, key=itemgetter(2)) 		#to benefit when we will make the linearly scan for the grid creation
	#print(xSortedCoordList)									#e.g: [...[37616, 40.179829, 116.164818], [27786, 40.179911, 116.40583]]
	#print(ySortedCoordList)									#e.g: [...[1140, 40.082111, 116.719937], [48288, 39.95366, 116.719976]]
	
	theGrid(coordList, boundaries)
	print("--- %s seconds ---" % (time.time() - startTime))
