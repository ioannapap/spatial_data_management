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

	dividedRangeX=(float(b[1])-float(b[0]))/10
	dividedRangeY=(float(b[3])-float(b[2]))/10

	for x in range(10):
		for y in range(10):
			
			lowerXCellBound=float(b[0])+(x*dividedRangeX)
			upperXCellBound=float(b[0])+((x+1)*dividedRangeX)
			lowerYCellBound=float(b[2])+(y*dividedRangeY)
			upperYCellBound=float(b[2])+((y+1)*dividedRangeY)
			
			if d[0]>=lowerXCellBound
			#print('cell (%d ,%d)' % (x,y))
			#print(lowerXCellBound)
			#print(upperXCellBound)
			#print(lowerYCellBound)
			#print(upperYCellBound)
			if d[0]==lowerXCellBound and d[1]==upperXCellBound and d[2]==lowerYCellBound and d[3]==upperYCellBound:
				#1
			elif d[0]>lowerXCellBound and d[1]<upperXCellBound and d[2]>lowerYCellBound and d[3]<upperYCellBound:
				#2
			elif d[0]>=lowerXCellBound and d[0]<upperXCellBound and d[1]>upperXCellBound and d[2]>=lowerYCellBound and d[2]<upperYCellBound and d[3]>upperYCellBound:
				#3
			elif d[0]<lowerXCellBound and d[1]<=upperXCellBound and d[1]>lowerXCellBound and d[2]<lowerYCellBound and d[3]<=upperYCellBound and d[3]>lowerYCellBound:
				#4
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

if __name__ == '__main__':

	dirList=[] 			#list of float lists
	dimensions=[]		#float list
	bounds=dirData() 	#string list
	getWindow(bounds)
	#print(dirList)		[[0, 0, 0, 108], [0, 1, 2894, 179], [0, 2, 7688, 20],...]
	windowEvaluation(dimensions, bounds)
	