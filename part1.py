#from operator import itemgetter 									
def findLimits():
	
	with open('Beijing_restaurants.txt', 'r', encoding='UTF-8') as df1:
		
		lineNum=0			
		maxX=0														
		maxY=0														
		minX=200													
		minY=200		

		try:
			df1.__next__() 											
		except StopIteration:
			print('StopIteration')
			sys.exit(1)											

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
	splitXY=[i.split(',') for i in rawData]	
	floatData= [float(j) for i in splitXY for j in i]			
	floatData.insert(0,lineNum)								

	return floatData

def theGrid(cList, boundaries):

	dividedRangeX=(boundaries[1]-boundaries[0])/10
	dividedRangeY=(boundaries[3]-boundaries[2])/10

	cellWithElements=0
	firstTimeInCell=1
	belongsToCell=[]
	placeInGrd=0
	numOfRestaurants=0
	
	with open('grid.grd', 'w+', encoding='UTF-8') as dfgrd, open('grid.dir', 'w+', encoding='UTF-8') as dfdir:
		
		dfdir.write('%s %s %s %s\n' % ('{0:.6f}'.format(boundaries[0]), '{0:.6f}'.format(boundaries[1]), '{0:.6f}'.format(boundaries[2]), '{0:.6f}'.format(boundaries[3])))
		
		for x in range(10):
			for y in range(10):

				print('cell (%d ,%d)' % (x,y))
				print('lowerx boundary: %f' % (boundaries[0]+(x*dividedRangeX)))
				print('maxx boundary: %f' % (boundaries[0]+((x+1)*dividedRangeX)))
				print('lowery boundary: %f' % (boundaries[2]+(y*dividedRangeY)))
				print('maxy boundary: %f' % (boundaries[2]+((y+1)*dividedRangeY)))
				
				for sublist in cList:

					if ((sublist[1]>=boundaries[0]+(x*dividedRangeX) and sublist[1]<boundaries[0]+((x+1)*dividedRangeX)) or (x==9 and sublist[1]==boundaries[1])) and ((sublist[2]>=boundaries[2]+(y*dividedRangeY) and sublist[2]<boundaries[2]+((y+1)*dividedRangeY)) or (y==9 and sublist[2]==boundaries[3])):
						
						cellWithElements=1
						numOfRestaurants+=1	
						belongsToCell.insert(len(belongsToCell), sublist)

						if firstTimeInCell==1:

							firstRestaurant=[x,y,placeInGrd]					
							firstTimeInCell=0	
						
						with6decx='{0:.6f}'.format(sublist[1])
						with6decy='{0:.6f}'.format(sublist[2])	
						placeInGrd+=len(str(sublist[0]))+len(with6decx)+len(with6decy)+3 #two spaces and one \n
													
				dfgrd.writelines('%s %s %s \n' % (str(i[0]), '{0:.6f}'.format(i[1]), '{0:.6f}'.format(i[2]))  for i in belongsToCell)
				
				if cellWithElements==1:
					firstRestaurant.insert(len(firstRestaurant), numOfRestaurants)
					dfdir.write('%s %s %s %s\n' % (str(firstRestaurant[0]), str(firstRestaurant[1]), str(firstRestaurant[2]), str(firstRestaurant[3])))
				
				belongsToCell=[]
				numOfRestaurants=0														
				firstTimeInCell=1														
				cellWithElements=0

if __name__ == '__main__':
	
	coordList=[]	
	boundaries=findLimits()									
	theGrid(coordList, boundaries)