import sys
import math

dirList=[]
dimensions=[]

def checkDimensions(d): 								#xLow:	d[0]	xHigh:	d[1]	yLow:	d[2]	yHigh:	d[3]
	if d[0]<=d[1] and d[2]<=d[3] and d[0]>=0 and d[0]<=9 and d[1]>=0 and d[1]<=9 and d[2]>=0 and d[2]<=9 and d[3]>=0 and d[3]<=9:	
		return 1
	else:	
		return 0


def fixDir():
	with open('grid.dir', 'r', encoding='UTF-8') as dfdir:
		try:
			dfdir.__next__() 											
		except StopIteration:
			print('StopIteration')
			sys.exit(1)	
		for row in dfdir:
			row=row.split(' ')
			intRow=[int(i) for i in row]	
			dirList.insert(len(dirList), intRow)
	
def windowEvaluation(d):
 	
 	for x in range(10):
 		for y in range(10):
 			if x==math.floor(d[0])

	

def getWindow():
	print('---------------------------WINDOW SELECTION QUERY---------------------------')
	checked=0
	while checked==0 or len(dimensions)!=4:
		dimensions=input("Insert (0.0-9.0): Lower X, Upper X, Lower Y, Upper Y: ").split(' ')	
		try: 
			dimensions=[float(i) for i in dimensions]
			#if not float goes right away to except ValueError --> it skips check=checkDimensions
			checked=checkDimensions(dimensions)
		except ValueError:
			checked=0				

if __name__ == '__main__':
	getWindow()
	fixDir()												#print(dirList)		[[0, 0, 0, 108], [0, 1, 2894, 179], [0, 2, 7688, 20],...]
	windowEvaluation(dimensions)
	