def checkDimensions(d, b): 								
	
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


def windowEvaluation(d,b):							
	
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
			
			if d[0]>=lowerXCellBound and d[0]<upperXCellBound and d[2]>=lowerYCellBound and d[2]<upperYCellBound:
				print('lower left corner cell (%d ,%d)' % (x,y))
				founddl=1	
				xdl=x
				ydl=y

			if d[1]<=upperXCellBound and d[1]>lowerXCellBound and d[3]<=upperYCellBound and d[3]>lowerYCellBound:
				print('upper right corner cell (%d ,%d)' % (x,y))
				foundur=1	
				xur=x
				yur=y

			if founddl==1 and foundur==1:
				with open('grid.grd', 'r', encoding='UTF-8') as dfgrd, open('results_part2.txt', 'w', encoding='UTF-8') as rp2: 
					for l in dirList:
						numspots=0
						
						if l[0]>xdl and l[0]<xur and l[1]>ydl and l[1]<yur and numspots==0: 
							print('inside cell (%d ,%d)\n' % (l[0],l[1]))
							dfgrd.seek(l[2])
							
							for row in dfgrd:
								numspots+=1
								row=row.split(' ')
								if numspots<=l[3]:			
									print(row[0]+' '+row[1]+' '+row[2])	
									rp2.write('%s %s %s' % (row[0], row[1], row[2]))
								else:
									break

						elif ((l[0]==xdl or l[0]==xur) and l[1]>=ydl and l[1]<=yur) or ((l[1]==ydl or l[1]==yur) and l[0]>=xdl and l[0]<=xur) and numspots==0:
							print('crossed by window"s line cell (%d ,%d)\n' % (l[0],l[1]))
							dfgrd.seek(l[2])
							
							for row in dfgrd:
								numspots+=1
								row=row.split(' ')
								if float(row[1])>=d[0] and float(row[1])<=d[1] and float(row[2])>=d[2] and float(row[2])<=d[3] and numspots<=l[3]:	
									print(row[0]+' '+row[1]+' '+row[2])
									rp2.write('%s %s %s' % (row[0], row[1], row[2]))
								elif numspots>l[3]:
									break

				break
		
		if founddl==1 and foundur==1:
			break


def getWindow(b):
	
	print('---------------------------WINDOW SELECTION QUERY---------------------------')
	checked=0
	while checked==0 or len(dimensions)!=4:
		dimensions=input('Give LowerX, UpperX (%s-%s) and LowerY, UpperY (%s-%s): ' % (b[0], b[1], b[2], b[3]) ).split(' ')	
		try: 
			dimensions=[float(i) for i in dimensions]
			checked=checkDimensions(dimensions, b)
		except ValueError:
			checked=0	
	
	return dimensions


if __name__ == '__main__':

	dirList=[] 				
	bounds=dirData() 	
	dimensions=getWindow(bounds)
	windowEvaluation(dimensions, bounds)
	