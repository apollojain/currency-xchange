import requests, json, math

currencies = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "THB", "TRY", "ZAR", "EUR", "USD"]
currencies = currencies[:6]
dist = {}
order = {}

exchange_dict = {}
def get_exchange_rates(fr):
	global exchange_dict
	url = "http://api.fixer.io/latest?base={fr}".format(fr=fr)
	response = requests.get(url)
	if response.status_code:
		json_data = json.loads(response.text)
		# print(json_data)
		exchange_dict[fr] = json_data['rates']

def exchanges():
	global exchange_dict
	for currency in currencies: 
		get_exchange_rates(currency)

def neg_log_exchange(fr, to):
	global exchange_dict
	rate = exchange_dict[fr][to]
	if rate is not None:
		return -1*float(math.log10(rate))

def floyd_warshall():
	global exchange_dict
	exchanges()
	def get_exchange_rate(fr, to):
		if fr == to:
			return 0.0
		rate = exchange_dict[fr][to]
		new_rate = -1*float(math.log10(rate))
		return new_rate
	c = len(currencies)
	for i in range(c):
		cur1 = currencies[i]
		dist[cur1] = {}
		order[cur1] = {}
		for j in range(c):
			cur2 = currencies[j]
			dist[cur1][cur2] = 1000000
			order[cur1][cur2] = [cur1, cur2]
	for i in range(c):
		cur1 = currencies[i]
		for j in range(c):
			cur2 = currencies[j]
			dist[cur1][cur2] = get_exchange_rate(cur1, cur2)
			print dist[cur1][cur2]
	for k in range(c): 
		cur3 = currencies[k]
		for i in range(c):
			cur1 = currencies[i]
			for j in range(c):
				cur2 = currencies[j]
				a1 = dist[cur1][cur3]
				a2 = dist[cur3][cur2]
				print a1
				print a2
				a = a1 + a2
				b = dist[cur1][cur2]
				if a < b:
					order[cur1][cur2] = order[cur1][cur3] + order[cur3][cur2][1:]
				dist[cur1][cur2] = min(a, b)
	return dist	 

distances = floyd_warshall()
def final_exchange(cur1, cur2):
	global distances
	try: 
		return_exchange = 10**(-1*distances[cur1][cur2])
		return return_exchange
	except: 
		return float('inf')


# print "here!"
for cur1 in currencies:
	for cur2 in currencies:
		a = 2
		print order[cur1][cur2]
		print final_exchange(cur1, cur2)




	