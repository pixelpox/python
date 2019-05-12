##
# requires requests to be installed
# requires BeautifulSoup4 to be installed
# https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3
import requests
from bs4 import BeautifulSoup
import urllib3

#stop it complaining about fildder
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#steamProfileURL = 'https://steamcommunity.com/profiles/76561198208160528/games/?tab=all'

def checkPlatformSupport(html):
	print("looking at the platform")

	platformSupport = {}

	
	if(str(html).find('platform_img win') != -1):
		platformSupport['windows'] = True
	else:
		platformSupport['windows'] = False

	if(str(html).find('platform_img mac') != -1):
		platformSupport['mac'] = True
	else:
		platformSupport['mac'] = False

	if(str(html).find('platform_img linux') != -1):
		platformSupport['linux'] = True
	else:
		platformSupport['linux'] = False
		
	return platformSupport

def gameModes(html):
	print("looking at what games modes there are")
	modeSupport = {}

	if(str(html).find('Single-player') != -1):
		modeSupport['singlePayer'] = True
	else: 
		modeSupport['singlePayer'] = False

	if(str(html).find('Multi-player') != -1):
		modeSupport['Multiplayer'] = True
	else: 
		modeSupport['Multiplayer'] = False
		
	if(str(html).find('Online Multi-Player') != -1):
		modeSupport['OnlineMulti-Player'] = True
	else: 
		modeSupport['OnlineMulti-Player'] = False

	if(str(html).find('Local Multi-Player') != -1):
			modeSupport['LocalMultiPlayer'] = True
	else: 
		modeSupport['LocalMultiPlayer'] = False

	if(str(html).find('Co-op') != -1):
			modeSupport['CoOp'] = True
	else: 
		modeSupport['CoOp'] = False

	if(str(html).find('Online Co-op') != -1):
			modeSupport['OnlineCoOp'] = True
	else: 
		modeSupport['OnlineCoOp'] = False


	return modeSupport
	
	
def getGameInformation(gameId = 344850):
	url = 'https://store.steampowered.com/app/' + str(gameId)
	page = requests.get(url , verify = False)
	soup = BeautifulSoup(page.text, 'html.parser')

	gameName = soup.find(class_='apphub_AppName').text
	print(gameName)

	platform = soup.find(class_='game_area_purchase_platform')
	
	platformSupport = checkPlatformSupport(platform)

	print(platformSupport)

	gameDetails = soup.findAll(class_='game_area_details_specs')
	modeSupport = gameModes(gameDetails)
	print(modeSupport)


getGameInformation(427250)
