import requests
from bs4 import BeautifulSoup
import urllib3

#stop it complaining about fildder
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

steamProfileURL = 'https://steamcommunity.com/id/pixelpox/games/?tab=all'


page = requests.get(steamProfileURL , verify = False)
soup = BeautifulSoup(page.text, 'html.parser')
gameLayer = soup.findAll("div")
gameListRows = soup.find_all("div" , id="games_list_rows")

for game in gameListRows:
	print(game)

gameListRow = soup.find_all("div", class_="gameListRow")

print(soup.prettify())

with open("output1.html", "w", encoding='utf-8') as file:
    file.write(str(gameListRows))


#print(str(gameListRows))

print("end")

#pagecontent no_header

#games_list_rows
