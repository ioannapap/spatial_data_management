import math
from operator import itemgetter

def checkArgs(inpt,b): 								
	
	minX=float(b[0])
	maxX=float(b[1])
	minY=float(b[2])
	maxY=float(b[3])

	if int(inpt[0])>=1 and int(inpt[0])<51790 and float(inpt[1])>=minX and float(inpt[1])<=maxX and float(inpt[2])>=minY and float(inpt[2])<=maxY :	
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
		args=input('Give k (1-51699), x_coordinate (%s-%s) and y_coordinate (%s-%s): ' % (b[0], b[1], b[2], b[3]) ).split(' ')
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
		

def knnGenerator(q, b, cell):

	ordCells=[]
	ncell=cell
	ncdistance=0

	priorityQueue.insert(len(priorityQueue), ncell)
	allVisitedCells.insert(len(allVisitedCells), [priorityQueue[0][0], priorityQueue[0][1]])
	newNCells=mindist(q, bounds, ordCells, [priorityQueue[0][0], priorityQueue[0][1]])
	for i in newNCells:
		ordCells.insert(len(ordCells), i)
	ordSpots=orderedNSpots(q, [priorityQueue[0][0], priorityQueue[0][1]])	
	priorityQueue.pop(0) 
	
	ncell=ordCells[0]		
	ncdistance=ncell[2]	
	
	while not ordSpots:
		priorityQueue.insert(len(priorityQueue), ncell)
		ordCells.pop(0)
		allVisitedCells.insert(len(allVisitedCells), [priorityQueue[0][0], priorityQueue[0][1]])
		newNCells=mindist(q, bounds, ordCells, [priorityQueue[0][0], priorityQueue[0][1]])
		for i in newNCells:
			if i not in ordCells:
				ordCells.insert(len(ordCells), i)		
		ordCells=sorted(ordCells, key=itemgetter(2))
		if ordCells:
			ncell=ordCells[0]		
			ncdistance=ncell[2]	
		ordSpots=orderedNSpots(q, [priorityQueue[0][0], priorityQueue[0][1]])	
		priorityQueue.pop(0) 

	if not priorityQueue:				 #apla topothetw tin prwti fora
			
			place=0

			for spot in ordSpots:
				nsdistance=spot[2]
					
				if nsdistance<=ncdistance:	
					priorityQueue.insert(place, spot)
					place+=1
								
				else: 					#nsdistance>ncdistance: 
					priorityQueue.insert(place, ncell)
					if ordCells:
						ordCells.pop(0)
					else:
						break
					if ordCells:
						ncell=ordCells[0]		
						ncdistance=ncell[2]	
					else:
						break
					
					place+=1
				
		
	while True:

		if priorityQueue[0][0]>=0 and priorityQueue[0][0]<=9:

			ordSpots=orderedNSpots(q, [priorityQueue[0][0], priorityQueue[0][1]])
			print('found cell', [priorityQueue[0][0], priorityQueue[0][1]])
			allVisitedCells.insert(len(allVisitedCells), [priorityQueue[0][0], priorityQueue[0][1]])
			newNCells=mindist(q, bounds, ordCells, [priorityQueue[0][0], priorityQueue[0][1]])
			for i in newNCells:
				ordCells.insert(len(ordCells), i)
			priorityQueue.pop(0)
			
			place=0
			
			if ordSpots:
				print('this cell has spots')
				for spot in ordSpots:
					nsdistance=spot[2]
					for coord in priorityQueue:
						inPQdistance=coord[2]
						if coord[0]>=10 and nsdistance<inPQdistance and spot not in priorityQueue: 
							priorityQueue.insert(place, spot)	
							place+=1
							break		
						else:
							place+=1
			else:
				print('this cell has no spots')
				for coord in priorityQueue:
					inPQdistance=coord[2]
					if ncdistance<inPQdistance:
						priorityQueue.insert(place,ncell)
						ordCells.pop(0)

						if ordCells:
							ncell=ordCells[0]		
							ncdistance=ncell[2]
						else:
							break
						break
					place+=1


		elif priorityQueue[0][0]>=10:						
			
			nearestNeighbor=priorityQueue[0]
			priorityQueue.pop(0)
			
			yield nearestNeighbor	
			place=0
			

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
	
		if [x+1, y] not in nCList:
			nCList.insert(len(nCList), [x+1, y])
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
		for nn in knnGenerator(q, bounds, cell):
			if i<k:
				print('nearestNeighbor:', nn)
				rp3.write('%s %s\n' % ('{0:.6f}'.format(nn[0]), '{0:.6f}'.format(nn[1])))
				i+=1
			else:
				print('all visited cells:', allVisitedCells)
				for i in allVisitedCells:

					rp3.write(str(i))
				break