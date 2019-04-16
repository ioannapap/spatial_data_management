import sys


def windowEvaluation():

def rTreeCreation():

	with open('grid.dir', 'r', encoding='UTF-8') as dfdir:
		
		try:
			dfdir.__next__() 											
		except StopIteration:
			print('StopIteration')
			sys.exit(1)	
			
		for row in dfdir:




if __name__ == "__main__":
	
	print("------------------------------WINDOW SELECTION QUERY---------------------------------")
	xLow, xHiqh, yLow, yHigh=input("Insert lower X, upper X, lower Y, upper Y:").split()
	try: 
		xLow=float(xLow)
		xHigh=float(xHiqh)
		yLow=float(yLow)
		yHigh=float(yHigh)
	except ValueError:
		print('ValueError: You need to insert float numbers. Exiting...')
		sys.exit(1)

	rTreeCreation()
	windowEvaluation()