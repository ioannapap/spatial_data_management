import sys
import math

def checkDimensions(d, b): 								#xLow:d[0]	xHigh:d[1]	yLow:d[2]	yHigh:d[3]
	
	minX=float(b[0])
	maxX=float(b[1])
	minY=float(b[2])
	maxY=float(b[3])

	if d[0]<=d[1] and d[2]<=d[3] and d[0]>=minX and d[0]<=maxX and d[1]>=minX and d[1]<=maxX and d[2]>=minY and d[2]<=maxY and d[3]>=minY and d[3]<=maxY:	
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

def windowEvaluation(d,b):								#xLow:d[0]	xHigh:d[1]	yLow:d[2]	yHigh:d[3]
	founddl=0
	foundur=0
	dividedRangeX=(float(b[1])-float(b[0]))/10
	dividedRangeY=(float(b[3])-float(b[2]))/10

	for x in range(10):
		for y in range(10):
			
			lowerXCellBound=float(b[0])+(x*dividedRangeX)
			upperXCellBound=float(b[0])+((x+1)*dividedRangeX)
			lowerYCellBound=float(b[2])+(y*dividedRangeY)
			upperYCellBound=float(b[2])+((y+1)*dividedRangeY)
			
			'''
			print(lowerXCellBound)
			print(upperXCellBound)
			print(lowerYCellBound)
			print(upperYCellBound)
			'''
			if d[0]>=lowerXCellBound and d[0]<upperXCellBound and d[2]>=lowerYCellBound and d[2]<upperYCellBound:
				#general case-find lower bound and start searching
				print('cell (%d ,%d)' % (x,y))
				#founddl=1
				xdl=x
				ydl=y
				

				for l in dirList:
					if l[0]==x and l[1]==y:
						founddl=1
						
						with open('grid.grd', 'r', encoding='UTF-8') as dfgrd: 
							dfgrd.seek(l[2])
							for row in dfgrd:
								row=row.split(' ')

								if float(row[1])>=lowerXCellBound and float(row[1])<=upperXCellBound and float(row[2])>=lowerYCellBound and float(row[2])<=upperYCellBound:
									print(row[0]+' '+row[1]+' '+row[2])
					if founddl==1:
						founddl=0
						break
				'''

			if d[1]<=upperXCellBound and d[1]>lowerXCellBound and d[3]<=upperYCellBound and d[3]>lowerYCellBound:
				print('cell (%d ,%d)' % (x,y))
				foundur=1
				xur=x
				yur=y
			#################################
			if founddl==1 and foundur==1:
				for l in dirList:
					numspots=0
					if l[0]>xdl and l[0]<xur and l[1]>ydl and l[1]<yur:
						with open('grid.grd', 'r', encoding='UTF-8') as dfgrd: 
							dfgrd.seek(l[2])
							for row in dfgrd:
								if numspots<=l[3]:
									numspots+=1
									row=row.split(' ')
									print(row[0]+' '+row[1]+' '+row[2])
								else:
									break
					else:
						
			#################################


				break
		if founddl==1 and foundur==1:
				break
				'''

def getWindow(b):
	print('---------------------------WINDOW SELECTION QUERY---------------------------')
	checked=0
	while checked==0 or len(dimensions)!=4:
		dimensions=input("Insert LowerX, UpperX (%s-%s) and LowerY, UpperY (%s-%s):\n" % (b[0], b[1], b[2], b[3]) ).split(' ')	
		try: 
			dimensions=[float(i) for i in dimensions]
			#if not float goes right away to except ValueError --> it skips check=checkDimensions
			checked=checkDimensions(dimensions, b)
		except ValueError:
			checked=0	
	return dimensions			

if __name__ == '__main__':

	dirList=[] 			#list of float lists
	
	bounds=dirData() 	#string list
	dimensions=getWindow(bounds)
	#print(dirList)		[[0, 0, 0, 108], [0, 1, 2894, 179], [0, 2, 7688, 20],...]
	
	windowEvaluation(dimensions, bounds)
	