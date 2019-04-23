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



def getKq(b):
	
	print('---------------------------NEAREST NEIGHBOR SELECTION ---------------------------')
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
				break
	spotList=sorted(spotList, key=itemgetter(2))	#from smallest distance to biggest
	
	print('SORTEDSPOTS CELL:', cell)	
	print(spotList[:10])
	return spotList
		

def knnGenerator(q, b, cell, ordCells):
	checkPQ=0
	#first time:
	nc=cell
	ncx=cell[0]				
	ncy=cell[1]
	ncdistance=0
	priorityQueue.insert(len(priorityQueue), [ncx, ncy, ncdistance])

	while True:
		
		if priorityQueue[0][0]>=0 and priorityQueue[0][0]<=9:
			
			allVisitedCells.insert(len(allVisitedCells), [priorityQueue[0][0], priorityQueue[0][1]])
			#ordCells.insert(len(ordCells), mindist(nc))		
			ordSpots=orderedNSpots(q, [priorityQueue[0][0], priorityQueue[0][1]])	
			priorityQueue.pop(0) 
			############
			ncell=ordCells[0]				
			nc=[ncell[0], ncell[1]]	
			ncx=ncell[0]
			ncy=ncell[1]
			ncdistance=ncell[2]			
			ordCells.pop(0)

			############
			place=0
			print('############### PRIORITY QUEUE after removing the cell: ##################\n', priorityQueue[:20])
			for spot in ordSpots:
				nsdistance=spot[2]
				if checkPQ==1: 
					for coord in priorityQueue:
						inPQdistance=coord[2]
						if nsdistance<inPQdistance:
							priorityQueue.insert(place, [spot[0], spot[1], spot[2]])		
							place+=1
							break
						else:
							place+=1

				elif nsdistance<=ncdistance:	#adding spots to the priorityQueue
							
					priorityQueue.insert(place, [spot[0], spot[1], spot[2]])
					place+=1
							
				while nsdistance>ncdistance: #adding cells to the priorityQueue
									
					priorityQueue.insert(place, [ncx, ncy, ncdistance])
					
					place+=1
					checkPQ=1
						############
							
					ncell=ordCells[0]
					nc=[ncell[0], ncell[1]]
					ncx=ncell[0]
					ncy=ncell[1]
					ncdistance=ncell[2]
					if ordCells:
						ordCells.pop(0)	
					else:
						break
						###########
					if nsdistance<=ncdistance: #...until spots have smaller distance
							
						priorityQueue.insert(place, [spot[0], spot[1], spot[2]])
						place+=1
						#auto-break while
				
			for whatsleft in ordCells:
				priorityQueue.insert(len(priorityQueue), [whatsleft[0], whatsleft[1], whatsleft[2]])
				
		else:								#found a spot!
			
			nearestNeighbor=priorityQueue[0]
			priorityQueue.pop(0)
			yield nearestNeighbor	
			
			print('################ PRIORITY QUEUE AFTER nearestNeighbor: ###################\n', priorityQueue[:20])	
					
			



def mindist(q, b, cell):
	
	cellList=[]
	md=100
	c=[cell[0], cell[1]]
	# cell[0] cell[1] so as not to include myself as the nearest cell
	for x in range(10):
		for y in range(10):
			
			if x==cell[0] and y==cell[1]:
				pass
			
			dividedRangeX=(float(b[1])-float(b[0]))/10
			dividedRangeY=(float(b[3])-float(b[2]))/10
			c=[x,y]
			
			if c in nearestCells(cell):

				lowerXCellBound=float(b[0])+(x*dividedRangeX)
				upperXCellBound=float(b[0])+((x+1)*dividedRangeX)
				lowerYCellBound=float(b[2])+(y*dividedRangeY)
				upperYCellBound=float(b[2])+((y+1)*dividedRangeY)
				

				if q[0]>upperXCellBound and q[1]>lowerYCellBound and q[1]<upperYCellBound:

					minCellDist=q[0]-upperXCellBound
					
				elif q[0]<lowerXCellBound and q[1]>lowerYCellBound and q[1]<upperYCellBound:
						
					minCellDist=lowerXCellBound-q[0]
					
				elif q[0]>lowerXCellBound and q[0]<upperXCellBound and q[1]<lowerYCellBound:
						
					minCellDist=lowerYCellBound-q[1]
					
				elif q[0]>lowerXCellBound and q[0]<upperXCellBound and q[1]>upperYCellBound:
						
					minCellDist=q[1]-lowerYCellBound
					
				elif (q[0]<lowerXCellBound or q[0]>upperXCellBound) and (q[1]<lowerYCellBound or q[1]>upperYCellBound) :
						
					minCellDist=math.sqrt((lowerXCellBound-q[0])**2+(lowerYCellBound-q[1])**2)

				cellList.insert(len(cellList), [x, y, minCellDist])
				
				if md>minCellDist:
					md=minCellDist
					mdCell=[x,y]
	
	cellList=sorted(cellList, key=itemgetter(2))

	print('Nearest Cell from q: ', mdCell)
	print('Nearest Distance from Cell is: ', md)
	return cellList
	#[mdCell, md] was working



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

	if x==0 and y==0:
		nCList.insert(len(nCList), [x, y+1]) 
		nCList.insert(len(nCList), [x+1, y+1])
		nCList.insert(len(nCList), [x+1, y])
		return [[x, y+1], [x+1, y+1], [x+1, y]]

	elif x==0 and y>=1 and y<=8:
		nCList.insert(len(nCList), [x, y+1])
		nCList.insert(len(nCList), [x+1, y+1])
		nCList.insert(len(nCList), [x+1, y])
		nCList.insert(len(nCList), [x+1, y-1])
		nCList.insert(len(nCList), [x, y-1])
		return [[x, y+1], [x+1, y+1], [x+1, y], [x+1, y-1], [x, y-1]]
				
	elif x==0 and y==9:
		nCList.insert(len(nCList), [x+1, y])
		nCList.insert(len(nCList), [x+1, y-1])
		nCList.insert(len(nCList), [x, y-1])
		return [[x+1, y], [x+1, y-1], [x, y-1]]

	elif x==9 and y==0:
		nCList.insert(len(nCList), [x-1, y])
		nCList.insert(len(nCList), [x-1, y+1])
		nCList.insert(len(nCList), [x, y+1])
		return [[x-1, y], [x-1, y+1], [x, y+1]]

	elif x>=1 and x<=8 and y==0:
		nCList.insert(len(nCList), [x-1, y])
		nCList.insert(len(nCList), [x-1, y+1])
		nCList.insert(len(nCList), [x, y+1])
		nCList.insert(len(nCList), [x+1, y+1])
		nCList.insert(len(nCList), [x+1, y])
		return [[x-1, y], [x-1, y+1], [x, y+1], [x+1, y+1], [x+1, y]]

	elif x==9 and y==9:
		nCList.insert(len(nCList), [x-1, y])
		nCList.insert(len(nCList), [x-1, y-1])
		nCList.insert(len(nCList), [x, y-1])
		return [[x-1, y],[x-1, y-1], [x, y-1]]

	elif x>=1 and x<=8 and y==9:
		nCList.insert(len(nCList), [x-1, y])
		nCList.insert(len(nCList), [x-1, y-1])
		nCList.insert(len(nCList), [x, y-1])
		nCList.insert(len(nCList), [x+1, y-1])
		nCList.insert(len(nCList), [x+1, y])
		return [[x-1,y], [x-1,y-1], [x, y-1], [x+1, y-1], [x+1, y]]

	elif x==9 and y>=1 and y<=8:
		nCList.insert(len(nCList), [x, y+1])
		nCList.insert(len(nCList), [x-1, y+1])
		nCList.insert(len(nCList), [x-1, y])
		nCList.insert(len(nCList), [x-1, y-1])
		nCList.insert(len(nCList), [x, y-1])
		return [[x, y+1], [x-1, y+1], [x-1, y], [x-1, y-1], [x, y-1]]
	else:
		nCList.insert(len(nCList), [x-1, y+1])
		nCList.insert(len(nCList), [x, y+1])
		nCList.insert(len(nCList), [x+1, y+1])
		nCList.insert(len(nCList), [x-1, y])
		nCList.insert(len(nCList), [x+1, y])
		nCList.insert(len(nCList), [x-1, y-1])
		nCList.insert(len(nCList), [x, y-1])
		nCList.insert(len(nCList), [x+1, y-1])
		return [[x-1, y+1], [x, y+1], [x+1, y+1], [x-1, y], [x+1, y], [x-1, y-1], [x, y-1], [x+1, y-1]]


if __name__ == '__main__':
	nCList=[]
	dirList=[]
	allVisitedCells=[]			
	
	bounds=dirData() 
	arguments=getKq(bounds)
	
	k=int(arguments[0])
	q=[float(arguments[1]), float(arguments[2])]
	cell=findqCell(q, bounds)

	print('q Cell: (%d, %d)' % (cell[0], cell[1]))
	#print('Given coordinates: (%f, %f)' % (q[0], q[1]))
		
	ordCells=mindist(q, bounds, cell)
	print('ordered cells by distance from q: ', ordCells)
	#e.g [4, 5, 0.010018399999999872], [3, 6, 0.0201720000000023], [4, 6, 0.02252283113998083],...]
	
	with open('results_part3.txt', 'w', encoding='UTF-8') as rp3: 
		
		priorityQueue=[]
		i=0
		for nn in knnGenerator(q, bounds, cell, ordCells):
			if i<k:
				print('\n')
				print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!nearestNeighbor:', nn)
				i+=1
			else:
				print('ALL VISITED CELLS:\n', allVisitedCells)
				break
			#rp3.write('%s %s' % ('{0:.6f}'.format(nn[0]), '{0:.6f}'.format(nn[0])))
			
		#for i in allVisitedCells:
		#	rp3.write(str(i))