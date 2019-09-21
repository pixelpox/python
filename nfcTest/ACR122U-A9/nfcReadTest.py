# Sources
# code was taken form 
# https://github.com/rocky112358/ACS-ACR122U-Tool

# cant remember if i used this package
# https://github.com/LudovicRousseau/pyscard/blob/master/INSTALL.md
# https://ludovicrousseau.blogspot.com/2014/03/level-1-smart-card-support-on-mac-os-x.html
# https://pypi.org/project/pyscard/

from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
from smartcard.CardType import AnyCardType
import sys

r = readers()
if len(r) < 1:
	print "error: No readers available!"
	sys.exit()

data_from_reader = []
print "Available readers: ", r

reader = r[0]
print "Using: ", reader

connection = reader.createConnection()
connection.connect()


COMMAND = 'read'

if type(COMMAND) == str:
	

	if COMMAND == "read":
	# decrypt first block of sector with key. if succeed, sector is unlocked
	# if other sector is unlocked, previous sector is locked
		COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, int(1)*4, 0x60, 0x00]

		data, sw1, sw2 = connection.transmit(COMMAND)

		if (sw1, sw2) == (0x90, 0x0):
			print "Status: Decryption sector "+ str(1) +" using key #0 as Key A successful."

		elif (sw1, sw2) == (0x63, 0x0):
			print "Status: Decryption sector "+ str(1) +" failed. Trying as Key B"
			COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, int(1)*4, 0x61, 0x00]
			data, sw1, sw2 = connection.transmit(COMMAND)
			
			if (sw1, sw2) == (0x90, 0x0):
				print "Status: Decryption sector "+ str(1) +" using key #0 as Key B successful."
			elif (sw1, sw2) == (0x63, 0x0):
				print "Status: Decryption sector "+ str(1) +" failed."
				sys.exit()

			
		print "---------------------------------Sector "+ str(1) +"---------------------------------"

		for block in range(int(1)*4, int(1)*4+4):
			COMMAND = [0xFF, 0xB0, 0x00]
			COMMAND.append(block)
			COMMAND.append(16)

			#PP: This is where all the cool stuff happens 
			data, sw1, sw2 = connection.transmit(COMMAND)
			print "block "+ str(block) +":\t"+ toHexString(data) +" | "+''.join(chr(i) for i in data)
			data_from_reader.append(data)


		#print "Status words: %02X %02X" % (sw1, sw2)

		#if (sw1, sw2) == (0x90, 0x0):
			#print "Status: The operation completed successfully."
		if (sw1, sw2) == (0x63, 0x0):
			print "Status: The operation failed. Maybe auth is needed."
		
	
	
	
	else:
		print "error: Undefined command"
		sys.exit()	


#-------------------------------------------
# PixelPox edits
#-------------------------------------------
# get url from card

# There seems to be a start and end flag
startFlag = False
startPos = 0

cardContent = []

#var to store url
urlOnCard = ''

# Loop over all the data blocks and whole card contents into cardContent
for block in data_from_reader:
    for intLetter in block:
        cardContent.append(intLetter)
        
# now that all the data is in one var look out for start flag.
# 209 is the start flag and 254 is the end flag
for i, intLetter in enumerate(cardContent):
    if intLetter == 209 and startFlag == False:
        startFlag = True
        startPos = i+5
        
    if i >= startPos and startFlag==True:
			if intLetter == 254 :
					break 
			

			urlOnCard += chr(intLetter)

#just some screen padding
print '\n'+('.\n'*5)
print urlOnCard