import csv
from santander import santanderRecord
from bs4 import BeautifulSoup
statementFile = open('statements.xls' , 'r')
soup = BeautifulSoup(statementFile , 'html.parser')

tableRow = soup.find('table').find_all('tr')


rowIndex = 0
tableHeaders = []
tableRecords = []

for row in tableRow:
	if rowIndex == 3:
		#print('row headers')
		#print(row)
		rowCells = row.find_all('td')

		#Get the Date
		tableHeaders.append(rowCells[1].get_text())


		#Get the Description
		tableHeaders.append(rowCells[3].get_text())

		#Get the MoneyIn
		tableHeaders.append(rowCells[5].get_text())

		#Get the MoneyOut
		tableHeaders.append(rowCells[6].get_text())

		#Get the Balance
		tableHeaders.append(rowCells[7].get_text().lstrip())

		##print(tableHeaders)

	if rowIndex > 4:
		rowCells = row.find_all('td')
		
		recordDate = rowCells[1].get_text().lstrip()

		#Get the Description
		recordDescription = rowCells[3].get_text().lstrip()

		#Get the MoneyIn
		recordMoneyIn = rowCells[5].get_text()
		recordMoneyIn = recordMoneyIn.replace('£' , '').replace(',' , '').lstrip()
		if not recordMoneyIn:
			recordMoneyIn = 0

		#Get the MoneyOut
		recordMoneyOut = rowCells[6].get_text()
		recordMoneyOut = recordMoneyOut.replace('£' , '').replace(',' , '').lstrip()
		if not recordMoneyOut:
			recordMoneyOut = 0

		#Get the Balance
		recordBalance = rowCells[7].get_text()
		recordBalance = recordBalance.replace('£' , '').replace(',' , '').lstrip()

		#find the type
		recordType = ''
		if recordDescription.find('DIRECT DEBIT PAYMENT TO') is not -1:
			recordType = 'fixedBill'
		if recordDescription.find('CARD PAYMENT TO NETFLIX.COM') is not -1:
			recordType = 'fixedBill'
		if recordDescription.find('MONTHLY ACCOUNT FEE') is not -1:
			recordType = 'fixedBill'
		if recordDescription.find('REGULAR TRANSFER PAYMENT TO ACCOUNT SAVING') is not -1:
			recordType = 'fixedBill'
		if recordDescription.find('STANDING ORDER VIA FASTER PAYMENT TO J A KELLY REFERENCE S K Money') is not -1:
			recordType = 'fixedBill'	
		if recordDescription.find('ARRANGED OVERDRAFT USAGE FEE') is not -1:
			recordType = 'overdraft'

		if recordDescription.find('CARD PAYMENT TO Just Eat') is not -1:
			recordType = 'takeaway'
		if recordDescription.find('MCDONALDS') is not -1:
			recordType = 'takeaway'
		if recordDescription.find('KFC') is not -1:
			recordType = 'takeaway'

			 

		if recordDescription.find('MORRISON') is not -1:
			recordType = 'food'
		if recordDescription.find('ASDA') is not -1:
			recordType = 'food'
			
			
		if recordDescription.find('APPLE PAY') is not -1:
			recordType = 'applePay'

		if recordDescription.find('Cashback') is not -1:
			recordType = 'cashBack'
			

		san = santanderRecord(recordDate , recordDescription , recordMoneyIn , recordMoneyOut , recordBalance , recordType)

		tableRecords.append(san)
		#print(san.date + ' ' + san.description + ' ' + san.moneyIn + ' ' + san.moneyOut + ' ' + san.balance)
		#print(row)


	rowIndex +=1

with open('output.csv' , mode='w' , newline='') as outputFile:
	csvWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	#Write headers
	csvWriter.writerow([tableHeaders[0] , tableHeaders[1] , tableHeaders[2] , tableHeaders[3] , tableHeaders[4]])

	#Write Records
	for record in tableRecords:
		csvWriter.writerow([record.date , record.description , record.moneyIn , record.moneyOut , record.balance , record.type])