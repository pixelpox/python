import wget
import requests


#hhttps://www.raspberrypi.org/magpi-issues/MagPi21.pdf
baseURL = 'https://www.raspberrypi.org/magpi-issues/MagPi'

for issue in range(1,81):
	url = baseURL
	
	if(issue >= 1 and issue <= 9):
		url = url + '0' + str(issue)
	else:
		url = url + str(issue)

	url = url + '.pdf'

	print(url)

	response = requests.get(url)

	filename = str(issue) + '.pdf'



	with open(filename, 'wb') as f:
		f.write(response.content)