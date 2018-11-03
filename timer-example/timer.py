import datetime
from datetime import timedelta

currentTime = datetime.datetime.now()

giftBoxLastOpened = datetime.datetime.now() - timedelta(hours=7)

giftBoxWaitPeriod = timedelta(hours=6)

nextGiftBoxTime = (giftBoxLastOpened + giftBoxWaitPeriod)

if currentTime > nextGiftBoxTime:
    print("lets open a damn box")
else:
    print("the next giftbox will be opened in: ", nextGiftBoxTime)



#source
#http://www.pressthered.com/adding_dates_and_times_in_python/