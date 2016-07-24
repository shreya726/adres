#!/usr/bin/python
import csv
import os
exec(open('sublexical.py').read())

def parse_csv(filename):
	ae = 0
	csvfile = open(filename, "r")
	input1= csv.reader(open(filename, 'rU'), dialect=csv.excel_tab)
	errors = 0
	scores = 0
	gpe_errors = 0
	for row in input1:
		try:
			a = [y.strip() for y in row[0].split(',')]	
		except:
			pass
		try: 
			score = main(a[0],a[1])
			scores +=1
			if str(score) != a[2]: 
				if a[2] == '8':
					gpe_errors +=1
				errors +=1
				print("ERROR: target = "+a[0]+" response = " + a[1])
				print("Manual score: " + a[2])
				print("Automated score: " + str(score))
		except: 
			ae +=1
	print("--------------------")
	print("Total errors:")
	print(errors)
	return (errors,ae,scores, gpe_errors)

total_ae = 0
total_errors = 0
total_scores = 0
gpe_errors = 0
print('SUBLEXICAL TESTING')
for i in os.listdir(os.getcwd()):
	
	if i.endswith('.csv'):
		print(i[:-4])
		(t, a,s,g) = parse_csv(i)
		total_errors += t
		total_ae += a
		total_scores += s
		gpe_errors += g
print("************************************")		
print('Total errors in this test: '+str(total_errors))
print('of the errors, ' + str(gpe_errors)+' are gpe errors')
print("Total scores: "+str(total_scores))