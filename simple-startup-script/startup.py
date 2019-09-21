import datetime
import sys
import os

def main():
	print("starting...")
	print(getTime())
	setup()
	print("ending...")
	print(getTime())

def setup():
	print("setup")
	print("-"*70)
	print(sys.argv[0])
	print(os.path.basename(__file__))
	print(datetime.datetime.now().strftime('%Y-%m-%d'))
	print("-"*70)

def getTime():
	return datetime.datetime.now().strftime('%H:%M:%S')


if __name__ == "__main__":
	main()