import math
from operator import itemgetter
import time
startTime = time.time()

def checkArgs(inpt,b): 								
	
	minX=float(b[0])
	maxX=float(b[1])
	minY=float(b[2])
	maxY=float(b[3])

	if int(inpt[0])>=1 and int(inpt[0])<51970 and float(inpt[1])>=minX and float(inpt[1])<=maxX and float(inpt[2])>=minY and float(inpt[2])<=maxY :	
		return 1
	else:
		return 0


def dirData():

	firstRow=1

	with open('grid.dir', 'r', encoding='UTF-8') as dfdir:
		for row in dfdir:	
			if firstRow==1:
				boundaries=row.split(' ')
				firstRow=0
			else:
				row=row.split(' ')
				intRow=[int(i) for i in row]	
				dirList.insert(len(dirList), intRow)
	return boundaries


def getkq(b):
	
	print('-----------------INCREMENTAL NEAREST NEIGHBOR SELECTION-----------------')
	checked=0
	while checked==0 or len(args)!=3:
		args=input('Give k (1-51969), x_coordinate (%s-%s) and y_coordinate (%s-%s): ' % (b[0], b[1], b[2], b[3]) ).split(' ')
		try: 
			checked=checkArgs(args,b)
		except ValueError:
			checked=0	
	return args


def orderedNSpots(q, cell):
	
	spotList=[]
	for l in dirList:
		numspots=0
		if l[0]==cell[0] and l[1]==cell[1]:
			
			with open('grid.grd', 'r', encoding='UTF-8') as dfgrd: 
				dfgrd.seek(l[2])
				for row in dfgrd:	
					numspots+=1
					row=row.split(' ')
					if numspots<=l[3]:
						euclideanDist=math.sqrt((float(row[1])-q[0])**2+(float(row[2])-q[1])**2)
						spotList.insert(len(spotList), [float(row[1]), float(row[2]), euclideanDist] )
						
	return sorted(spotList, key=itemgetter(2))
		

def knnGenerator(q, k, b, cell):
	
	ordCells=[[cell[0], cell[1], 0]]
	ordSpots=[]
	firstSpotNeighborCells=[]
	haveCell=1
	firstTime=1
	countSpots=0
	canYield=0
	firstCell=[]
	flag=0
	priorityQueue.insert(len(priorityQueue), [cell[0], cell[1], 0])
	wheresLastSpot=-1 #because if last spot is the first element in the queue i want to be 0.
	lastSpot=[]
	while True:

		if haveCell==1:
			print('priorityQueue[0]', priorityQueue[0])
			inserting(priorityQueue[0][0], priorityQueue[0][1], firstTime, countSpots, ordCells, ordSpots, firstSpotNeighborCells, allVisitedCells)
			print('pq:', priorityQueue)
			if firstTime==1:
				firstTime=0
			wheresLastSpot=-1
			for element in priorityQueue:			
				if element[0]>=10:
					lastSpot=element
					wheresLastSpot+=1
					haveCell=0 #to be here means that i do have at least one spot
				else:
					break
			print('lastSpot dist in pq:', lastSpot)												
			print('firstSpot dist in next nearest cell:', firstSpotNeighborCells[0])	
		
		elif not firstSpotNeighborCells:
			flag=1
			print(' i have no more cells to insert')
			for element in priorityQueue:
				if element[0]>=0 and element[0]<=9:
					firstCell=element
					break
			if not firstCell: #there is no cell in pq
				for element in priorityQueue:
					yield element #end of story
			else:
				print('firstCell:', firstCell)
				for element in priorityQueue:
					if element!=firstCell:
						nearestNeighbor=element
						priorityQueue.pop(0)
						yield nearestNeighbor

				


		#iflastSpot means that we still have NEIGHBORs to visit
		elif haveCell==0 and lastSpot[2]>firstSpotNeighborCells[0][2] and k>=wheresLastSpot+1 and flag==0: 			#if the last spot before cell in pq is more far than the first spot in next ncell:
			print('lastSpot dist in pq:', lastSpot)												 									#k>=wheresLastSpot means that we definately need to open up the next cell 'cause spots inadequate	
			print('firstSpot dist in next nearest cell:', firstSpotNeighborCells[0])
			print('inserting ...', [firstSpotNeighborCells[0][0], firstSpotNeighborCells[0][1]] )
			inserting(firstSpotNeighborCells[0][0], firstSpotNeighborCells[0][1], firstTime, countSpots, ordCells, ordSpots, firstSpotNeighborCells, allVisitedCells)
			print('pq:', priorityQueue[:60])
		 	#let's find the next lastSpot before cell in pq
			wheresLastSpot=-1
			for element in priorityQueue:			
				if element[0]>=10:
					lastSpot=element
					wheresLastSpot+=1
				else:
					if priorityQueue[0][0]>=0 and priorityQueue[0][0]<=9:
						haveCell=1
					break	
				

		elif haveCell==0 and lastSpot[2]<=firstSpotNeighborCells[0][2] and k>=wheresLastSpot+1 and flag==0:
			#yield some
			for element in priorityQueue:
				#print('element #', element)
				canYield=0
				checked=0
				if element[0]>=10 and checked==0:
					for ncell in firstSpotNeighborCells:
						if lastSpot[2]<=ncell[2]: #maybe is <= from the firstSpotNeighborCell but not for all (maybe another one is closer for spots)
							canYield=1
						else: 									#means that we found the first element in the pq before lastSpot that is > than the firstSpotNeighborCells distance so...
				 			canYield=0
				 			checked=1
				 			inserting(ncell[0], ncell[1], firstTime, countSpots, ordCells, ordSpots, firstSpotNeighborCells, allVisitedCells)
		 					#let's find the next lastSpot before cell in pq
		 					wheresLastSpot=-1
		 					for element in priorityQueue:			
		 						if element[0]>=10:
		 							lastSpot=element
		 							wheresLastSpot+=1
		 						else:
		 							if priorityQueue[0][0]>=0 and priorityQueue[0][0]<=9:
		 								haveCell=1
		 							break		
				 			break
						if canYield==1:
							checked=1
							nearestNeighbor=element
							priorityQueue.remove(element)
							yield nearestNeighbor
							break
				else:
					if element[0]>=0 and element[0]<=9:
						haveCell=1
				break			

		elif haveCell==0 and lastSpot[2]>firstSpotNeighborCells[0][2] and k<wheresLastSpot+1 and flag==0:
			#yield some
			for element in priorityQueue:
				canYield=0
				checked=0
				if element[0]>=10 and checked==0:
					for ncell in firstSpotNeighborCells:
				 		if element[2]<=ncell[2]: #from all
				 			canYield=1
				 		else: #means that we found the first element in the pq before lastSpot that is > than the firstSpotNeighborCells distance so...
				 			canYield=0
				 			checked=1
				 			inserting(ncell[0], ncell[1], firstTime, countSpots, ordCells, ordSpots, firstSpotNeighborCells, allVisitedCells)
		 					#let's find the next lastSpot before cell in pq
		 					wheresLastSpot=-1
		 					for element in priorityQueue:			
		 						if element[0]>=10:
		 							lastSpot=element
		 							wheresLastSpot+=1
		 						else:
		 							if priorityQueue[0][0]>=0 and priorityQueue[0][0]<=9:
		 								haveCell=1
		 							break		
				 			break
				 		if canYield==1:
				 			checked=1
					 		nearestNeighbor=element
					 		priorityQueue.remove(element)
					 		yield nearestNeighbor
					 		break
				else:
					if element[0]>=0 and element[0]<=9:
						haveCell=1
				break
		#here we dont care about cells or about firstSpotNeighborCells

		elif lastSpot[2]<=firstSpotNeighborCells[0][2] and k<wheresLastSpot+1 and flag==0:
			#yield all
			for element in priorityQueue:
			 	if element[0]>=10:
			 		nearestNeighbor=element
			 		yield nearestNeighbor

######################################################################################################	
				 	
def inserting(xcoord, ycoord, firstTime, countSpots, ordCells, ordSpots, firstSpotNeighborCells, allVisitedCells):
	
	if firstTime==0:
		for f in firstSpotNeighborCells:
			if f[0]==xcoord and f[1]==ycoord:
				firstSpotNeighborCells.remove(f)
				break

	allVisitedCells.insert(len(allVisitedCells), [xcoord, ycoord])
	newNCells=mindist(q, bounds,ordCells, [xcoord, ycoord])
	print('after removing cell these are the new neighbors to insert:', newNCells)	#it might be empty	
	
	for i in newNCells:
		if i not in ordCells:	
			#****************************************	
			newiSpots=orderedNSpots(q, [i[0], i[1]])
			if newiSpots:
				firstSpotDist=newiSpots[0][2]
				p=[i[0], i[1], firstSpotDist]
				firstSpotNeighborCells.insert(len(firstSpotNeighborCells), p)
			#*******************************************
			ordCells.insert(len(ordCells), i)		
				
	ordSpots=orderedNSpots(q, [xcoord, ycoord])
	for cells in ordCells:
		if cells[0]==xcoord and cells[1]==ycoord:
			xdl=cells[2]
			break

	priorityQueue.remove([xcoord, ycoord, xdl])
	################
	#about to insert new spots to the pq (if i dont have it's fine- just skips it)
	for spot in ordSpots:
		place=0
		spotdist=spot[2]
		for element in priorityQueue:
			eldist=element[2]
			if spotdist<=eldist and spot not in priorityQueue:
				priorityQueue.insert(place, spot)	
				countSpots+=1
				break			
			else:
				place+=1
	for spot in ordSpots:
		if spot not in priorityQueue:
			priorityQueue.insert(len(priorityQueue), spot)
			countSpots+=1	
	#################
	#about to insert new cells to the pq (if i dont have it's fine- just skips it)
	for c in newNCells: #quicker this way no ordCells:
		place=0
		celldist=c[2]
		for element in priorityQueue:
			eldist=element[2]
			if celldist<eldist:
				priorityQueue.insert(place, c)
				break
			else:
				place+=1
	for c in newNCells: #quicker this way no ordCells:
		priorityQueue.insert(len(priorityQueue), c)	
	
	print('length of pq:', len(priorityQueue))

def mindist(q, b, ordCells, cell):
	
	cellList=[]
	
	for x in range(10):
		for y in range(10):
			
			if x==cell[0] and y==cell[1]:
				pass
			
			if [x,y] in nearestCells(cell) and [x,y] not in allVisitedCells:

				dividedRangeX=(float(b[1])-float(b[0]))/10
				dividedRangeY=(float(b[3])-float(b[2]))/10
				
				lowerXCellBound=float(b[0])+(x*dividedRangeX)
				upperXCellBound=float(b[0])+((x+1)*dividedRangeX)
				lowerYCellBound=float(b[2])+(y*dividedRangeY)
				upperYCellBound=float(b[2])+((y+1)*dividedRangeY)

				if q[0]>=upperXCellBound and q[1]>=lowerYCellBound and q[1]<=upperYCellBound:

					minCellDist=q[0]-upperXCellBound
					
				elif q[0]<=lowerXCellBound and q[1]>=lowerYCellBound and q[1]<=upperYCellBound:
						
					minCellDist=lowerXCellBound-q[0]
					
				elif q[0]>=lowerXCellBound and q[0]<=upperXCellBound and q[1]<=lowerYCellBound:
						
					minCellDist=lowerYCellBound-q[1]
					
				elif q[0]>=lowerXCellBound and q[0]<=upperXCellBound and q[1]>=upperYCellBound:
						
					minCellDist=q[1]-upperYCellBound
					
				elif q[0]>upperXCellBound and q[1]<lowerYCellBound:
					
					minCellDist=math.sqrt((q[0]-upperXCellBound)**2+(lowerYCellBound-q[1])**2)
				
				elif q[0]<lowerXCellBound and q[1]<lowerYCellBound:
					
					minCellDist=math.sqrt((lowerXCellBound-q[0])**2+(lowerYCellBound-q[1])**2)

				elif q[0]>upperXCellBound and q[1]>upperYCellBound:

					minCellDist=math.sqrt((q[0]-upperXCellBound)**2+(q[1]-upperYCellBound)**2)

				elif q[0]<lowerXCellBound and q[1]>upperYCellBound:

					minCellDist=math.sqrt((lowerXCellBound-q[0])**2+(q[1]-upperYCellBound)**2)

				if [x, y, minCellDist] not in priorityQueue and [x, y, minCellDist] not in ordCells:
					cellList.insert(len(cellList), [x, y, minCellDist])	

	return sorted(cellList, key=itemgetter(2))


def findqCell(q, b):

	dividedRangeX=(float(b[1])-float(b[0]))/10
	dividedRangeY=(float(b[3])-float(b[2]))/10
	for x in range(10):
		for y in range(10):
			
			lowerXCellBound=float(b[0])+(x*dividedRangeX)
			upperXCellBound=float(b[0])+((x+1)*dividedRangeX)
			lowerYCellBound=float(b[2])+(y*dividedRangeY)
			upperYCellBound=float(b[2])+((y+1)*dividedRangeY)

			if q[0]>=lowerXCellBound and q[0]<=upperXCellBound and q[1]>=lowerYCellBound and q[1]<=upperYCellBound:
				
				return [x,y]		


def nearestCells(c):
	
	x=c[0]
	y=c[1]
	
	if [x,y] not in nCList:
		nCList.insert(len(nCList), [x,y])
	
	if x==0 and y==0:
		
		if [x, y+1] not in nCList:
			nCList.insert(len(nCList), [x, y+1]) 
		if [x+1, y+1] not in nCList:
			nCList.insert(len(nCList), [x+1, y+1])
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])
		
	elif x==0 and y>=1 and y<=8:
		
		if [x, y+1] not in nCList:
			nCList.insert(len(nCList), [x, y+1]) 
		if [x+1, y+1] not in nCList:
			nCList.insert(len(nCList), [x+1, y+1])
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])
		if [x+1, y-1] not in nCList:
			nCList.insert(len(nCList), [x+1, y-1])
		if [x, y-1] not in nCList:
			nCList.insert(len(nCList), [x, y-1])
	
	elif x==0 and y==9:
	
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])
		if [x+1, y-1] not in nCList:
			nCList.insert(len(nCList), [x+1, y-1])
		if [x, y-1] not in nCList:
			nCList.insert(len(nCList), [x, y-1])
		
	elif x==9 and y==0:
	
		if [x-1, y] not in nCList:
			nCList.insert(len(nCList), [x-1, y])
		if [x-1, y+1] not in nCList:
			nCList.insert(len(nCList), [x-1, y+1])
		if [x, y+1] not in nCList:
			nCList.insert(len(nCList), [x, y+1]) 

	elif x>=1 and x<=8 and y==0:
		
		if [x-1, y] not in nCList:
			nCList.insert(len(nCList), [x-1, y])
		if [x-1, y+1] not in nCList:
			nCList.insert(len(nCList), [x-1, y+1])
		if [x, y+1] not in nCList:
			nCList.insert(len(nCList), [x, y+1]) 
		if [x+1, y+1] not in nCList:
			nCList.insert(len(nCList), [x+1, y+1])
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])
		
	elif x==9 and y==9:
		
		if [x-1, y] not in nCList:
			nCList.insert(len(nCList), [x-1, y])
		if [x-1, y-1] not in nCList:
			nCList.insert(len(nCList), [x-1, y-1])
		if [x, y-1] not in nCList:
			nCList.insert(len(nCList), [x, y-1])

	elif x>=1 and x<=8 and y==9:
		
		if [x-1, y] not in nCList:
			nCList.insert(len(nCList), [x-1, y])
		if [x-1, y-1] not in nCList:
			nCList.insert(len(nCList), [x-1, y-1])
		if [x, y-1] not in nCList:
			nCList.insert(len(nCList), [x, y-1])
		if [x+1, y-1] not in nCList:
			nCList.insert(len(nCList), [x+1, y-1])
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])
		
	elif x==9 and y>=1 and y<=8:
		
		if [x, y+1] not in nCList:
			nCList.insert(len(nCList), [x, y+1])
		if [x-1, y+1] not in nCList:
			nCList.insert(len(nCList), [x-1, y+1])
		if [x-1, y] not in nCList:
			nCList.insert(len(nCList), [x-1, y])
		if [x-1, y-1] not in nCList:
			nCList.insert(len(nCList), [x-1, y-1])
		if [x, y-1] not in nCList:
			nCList.insert(len(nCList), [x, y-1])
	
	else:
		
		if [x-1, y+1] not in nCList:
			nCList.insert(len(nCList), [x-1, y+1])
		if [x, y+1] not in nCList:
			nCList.insert(len(nCList), [x, y+1])
		if [x+1, y+1] not in nCList:
			nCList.insert(len(nCList), [x+1, y+1])
		if [x-1, y] not in nCList:
			nCList.insert(len(nCList), [x-1, y])
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])	
		if [x-1, y-1] not in nCList:
			nCList.insert(len(nCList), [x-1, y-1])
		if [x, y-1] not in nCList:
			nCList.insert(len(nCList), [x, y-1])
		if [x+1, y-1] not in nCList:
			nCList.insert(len(nCList), [x+1, y-1])
		
	return nCList


if __name__ == '__main__':
	
	priorityQueue=[]
	nCList=[]
	dirList=[]
	allVisitedCells=[]			
	bounds=dirData() 
	arguments=getkq(bounds)
	
	k=int(arguments[0])
	q=[float(arguments[1]), float(arguments[2])]
	cell=findqCell(q, bounds)
	print('q cell:', cell)
	
	with open('results_part3.txt', 'w', encoding='UTF-8') as rp3: 
		i=0
		for nn in knnGenerator(q, k, bounds, cell):
			if i<k:
				print('nearestNeighbor:', nn)
				rp3.write('%s %s %s\n' % ('{0:.6f}'.format(nn[0]), '{0:.6f}'.format(nn[1]), '{}'.format(nn[2])))
				i+=1
			else:
				print('all visited cells:', allVisitedCells)
				for i in allVisitedCells:

					rp3.write(str(i))
				break
		print("--- %s seconds ---" % (time.time() - startTime))