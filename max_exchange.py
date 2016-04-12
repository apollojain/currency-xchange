import requests, json, math

currencies = ["AUD", "BRL", "CAD", "CNY", "GBP", "HKD", "INR", "JPY", "KRW", "MXN", "MYR", "RUB", "EUR", "USD"]	
# currencies = currencies[:6]
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

def add_to_graph(startcurr, endcurr, headcur, tailcur):
	if headcur not in order[startcur][endcur]:
		order[startcur][endcur][headcur] = {}
	if tailcur not in order[startcur][endcur][headcur]:
		order[startcur][endcur][headcur][tailcur] = 0
	order[startcur][endcur][headcur][tailcur] += 1

def new_ordering(c1, c2, c3):
	
	startcurr0 = c1 
	endcurr0 = c2 
	startcurr1 = c1 
	endcurr1 = c3 
	startcurr2 = c3 
	endcurr2 = c2

	# print order[startcurr0][endcurr0]
	# order[startcurr0][endcurr0] = order[startcurr1][endcurr1]
	dictionary = order[startcurr1][endcurr1]

	for curr1 in order[startcurr2][endcurr2].keys():
		for curr2 in order[startcurr2][endcurr2][curr1].keys():
			if curr1 not in dictionary:
				dictionary[curr1] = {}
			if curr2 not in dictionary[curr1]:
				dictionary[curr1][curr2] = 0
			new_ordering = dictionary[curr1][curr2] + order[startcurr2][endcurr2][curr1][curr2]
			if new_ordering > 1000: 
				return False
			dictionary[curr1][curr2] = new_ordering
	order[startcurr0][endcurr0] = dictionary
	return True
	
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
			order[cur1][cur2] = {}
			order[cur1][cur2][cur1] = {}
			order[cur1][cur2][cur1][cur2] = 1
			# order[cur1][cur2] = [cur1, cur2]
	for i in range(c):
		cur1 = currencies[i]
		for j in range(c):
			cur2 = currencies[j]
			dist[cur1][cur2] = get_exchange_rate(cur1, cur2)
			# print dist[cur1][cur2]
	for k in range(c): 
		cur3 = currencies[k]
		for i in range(c):
			cur1 = currencies[i]
			for j in range(c):
				cur2 = currencies[j]
				a1 = dist[cur1][cur3]
				a2 = dist[cur3][cur2]
				a = a1 + a2
				b = dist[cur1][cur2]
				if a < b:
					if new_ordering(cur1, cur2, cur3):
						dist[cur1][cur2] = a
					
	return dist	 

distances = floyd_warshall()
def max_exchange(cur1, cur2):
	global distances
	try: 
		return_exchange = 10**(-1*distances[cur1][cur2])
		return return_exchange
	except: 
		return float('inf')

def get_order(cur1, cur2):
	return order[cur1][cur2]

# for i in range(len(currencies)):
# 	for j in range(len(currencies)):
# 		print currencies[i] + " -> " + currencies[j]
# 		print max_exchange(currencies[i], currencies[j])
# 		print get_order(currencies[i], currencies[j])
# 	