import urllib.request, json

url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
req = urllib.request.Request(url)

r = urllib.request.urlopen(req).read()
cont = json.loads(r.decode('utf-8'))

print(cont['time']['updatedISO'])

print(cont['bpi']['EUR']['rate_float'])
