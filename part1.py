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
	#print(dividedRangeX) == 0.04998209999999972
	#print(dividedRangeY) == 0.06495100000000065
	cellWithElements=0
	numOfRest=0
	lineInGrd=0
	firstTime=1
	belongsToCell=[]
	with open('grid.grd', 'w+', encoding='UTF-8') as dfgrd, open('grid.dir', 'w+', encoding='UTF-8') as dfdir: #write and reading
		
		for x in range(10):
			for y in range(10):
				
				for sublist in cList:
					#sublist[1]=xcoordinate sublist[2]=ycoordinate
					if sublist[1]>=boundaries[0]+(x*dividedRangeX) and sublist[1]<boundaries[0]+((x+1)*dividedRangeX) and sublist[2]>=boundaries[2]+(y*dividedRangeY) and sublist[2]<boundaries[2]+((y+1)*dividedRangeY): #< 'cause if it was <= it wouldnt be written to the next cell'
						cellWithElements=1
						belongsToCell.insert(len(belongsToCell), sublist)
						if firstTime==1:
							firstRestaurant=[x,y, lineInGrd]					
							firstTime=0
						lineInGrd+=1
						numOfRest+=1	
				
				#print(belongsToCell) #[[56, 39.72927, 116.119278], [573, 39.729398, 116.128704], [1253, 39.723127, 116.121828], [1372, 39.729585, 116.127883], [1395, 39.729571, 116.128738]...
				
				dfgrd.writelines('%s %s %s \n' % (str(i[0]), str(i[1]), str(i[2]))  for i in belongsToCell)
				if cellWithElements==1:
					firstRestaurant.insert(len(firstRestaurant), numOfRest)
					dfdir.write('%s %s %s %s \n' % ( str(firstRestaurant[0]), str(firstRestaurant[1]), str(firstRestaurant[2]), str(firstRestaurant[3])))
				numOfRest=0														#because we are moving to the next cell
				firstTime=1														#because we are moving to the next cell 
				cellWithElements=0

if __name__ == "__main__":

	boundaries=findLimits()									#the results "boundaries" should be the first line in grid.dir
	#print(boundaries)
	#print(coordList)											#e.g: [...[51951, 39.947793, 116.192175], [51952, 39.925906, 116.438004]...]
	#print(xSortedCoordList)									#e.g: [...[37616, 40.179829, 116.164818], [27786, 40.179911, 116.40583]]
	#print(ySortedCoordList)									#e.g: [...[1140, 40.082111, 116.719937], [48288, 39.95366, 116.719976]]
	
	theGrid(coordList, boundaries)
	print("--- %s seconds ---" % (time.time() - startTime))
