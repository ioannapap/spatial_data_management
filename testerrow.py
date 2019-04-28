
if __name__ == '__main__':
	with open('results_part3.txt', 'r', encoding='UTF-8') as rp3: 
		big=0
		rowcounter=1
		for row in rp3:
			row=row.split(' ')
			rowcounter+=1
			if big<=float(row[2]):
				big=float(row[2])

			else:
				print('\n \n')
				print('distance in row (%d): %s' % (rowcounter, str(row[2])))
				print('the previous row had:', big)


'''
51969 39.69 116.071

distance in row (1158): 0.19277259971531438

the previous row had: 0.23948091089897205

------------

distance in row (1016): 0.1312162743298245

the previous row had: 0.1332089613351883


'''