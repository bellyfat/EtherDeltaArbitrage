from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

def calculate_profit(coin):
	driver = webdriver.Chrome('C://chromedriver.exe')
	url = "https://etherdelta.com/#" + coin + "-ETH"
	driver.get(url)	
	time.sleep(35)
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	orders = soup.find(id = 'orders')
	ratios = orders.find_all(class_ = "three-columns overflow-hidden padding-left")
	amounts = orders.find_all(class_ = "three-columns overflow-hidden")[::2]


	buy_sell = "buy"
	buy_ratios = []
	sell_ratios = []
	buy_amounts = []
	sell_amounts = []
	for order in range(0, len(ratios)):	
		if buy_sell == "buy":	
			if ratios[order].text == coin + "/ETH":
				buy_sell = "sell"
			else:
				buy_ratios.append(float(ratios[order].text))	
				buy_amounts.append(float(amounts[order].text))
		else:
			sell_ratios.append(float(ratios[order].text))
			sell_amounts.append(float(amounts[order].text))

	buy_ratio = len(buy_ratios) - 1	
	profits = 0
	while buy_ratio > -1:
		sell_ratio = 0
		while sell_ratio < len(sell_ratios):
			if (buy_ratios[buy_ratio] * 1.003) < (sell_ratios[sell_ratio] * .997):
				if buy_amounts[buy_ratio] < sell_amounts[sell_ratio]:
					print ("Buy " + str(buy_amounts[buy_ratio]) + " " + coin + " for " + str(buy_ratios[buy_ratio] * buy_amounts[buy_ratio] * 1.003) + " ETH and sell for " + str(sell_ratios[sell_ratio] * buy_amounts[buy_ratio] * .997) + " ETH")
					profits += ((sell_ratios[sell_ratio] * buy_amounts[buy_ratio] * 1.003) - (buy_ratios[buy_ratio] * buy_amounts[buy_ratio]) * .997)
					sell_amounts[sell_ratio] -= buy_amounts[buy_ratio]
					break
				else:
					print ("Buy " + str(sell_amounts[sell_ratio]) + " " + coin + " for " + str(buy_ratios[buy_ratio] * sell_amounts[sell_ratio] * 1.003) + " ETH and sell for " + str(sell_ratios[sell_ratio] * sell_amounts[sell_ratio] * .997) + " ETH")
					profits += ((sell_ratios[sell_ratio] * sell_amounts[sell_ratio] * 1.003) - (buy_ratios[buy_ratio] * sell_amounts[sell_ratio]) * .997)
					buy_amounts[buy_ratio] -= sell_amounts[sell_ratio]
					del sell_ratios[sell_ratio]	
					del sell_amounts[sell_ratio]
			else:
				sell_ratio += 1
		buy_ratio -= 1
					
	print (coin + ": Your profit is " + str(profits) + " ETH")
	driver.close()
	return profits


coins = ['DRGN', 'PPT', 'LEND', 'VERI', 'EOS', 'COB', 'PPP', 'BLUE', 'OMG', 'GRX', 'RDN', 'PLR', 'AION', 'SALT']
total_profit = 0
for coin in coins:
	total_profit += calculate_profit(coin)
print ("Your total profit is: " + str(total_profit))
