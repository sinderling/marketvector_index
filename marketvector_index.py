import requests
from yahoo_fin import stock_info as si
import os
import csv
import zipfile


# Set the URL to download the index from and headers
url = 'https://marketvector.com/constituents/download/MVBIZD_constituents.zip'
headers = {'authorization': 'Basic bWlrZXN0dWZmMTEwQGdtYWlsLmNvbTpob2x5Y293MjU='}

# Downloading the file
req = requests.get(url, headers=headers)
 
# Writing the file to metadata folder
with open('C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD.zip','wb') as output_file:
    output_file.write(req.content)

# Extracting zip file
with zipfile.ZipFile('C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD.zip', 'r') as zip_ref:
    zip_ref.extractall('C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD_files')

# Removing the zip file
os.remove('C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD.zip')

# Removing unneeded files
dir_list = os.listdir('C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD_files')
for file in dir_list:
    if 'MVBIZDTR-OPENING' not in file:
        os.remove(f'C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD_files\\{file}')

# Read the text file in fails_to_deliver_current
read_directory = 'C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD_files\\'
file = os.listdir(read_directory)

# Building full portfolio of tickers in index
with open(read_directory + file[0]) as ftd:
    reader = csv.reader(ftd,delimiter=';')
    full_portfolio = []
    for row in reader:
        if row[0].startswith('US'):
            temp_dic = {}
            index_of_period = row[2].index('.')
            ticker = row[2][0:index_of_period]
            percent_of_portfolio = (float(row[16][:-1]))/100
            temp_dic['ticker'] = ticker
            temp_dic['pop'] = percent_of_portfolio
            full_portfolio.append(temp_dic)

# Clearing files
dir_list = os.listdir('C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD_files')
for file in dir_list:
    os.remove(f'C:\\Users\\User\\PycharmProjects\\stock_picker\\metadata\\MVBIZD_files\\{file}')

total_to_invest = float(input('Please input Total to Invest: $'))

for stock in full_portfolio:
    stock['price'] = si.get_live_price(stock['ticker'])
    if stock['price'] != stock['price']:
        stock['price'] = 'price_not_found'
        break
    stock['quantity'] = int((total_to_invest*stock['pop'])//stock['price'])
    quantity_long = float((total_to_invest*stock['pop'])/stock['price'])
    stock['quantity_remainder'] = quantity_long - stock['quantity']

# This sorts the list based on the remainder of quantity
full_portfolio = sorted(full_portfolio, key = lambda i: i['quantity_remainder'],reverse=True)

# This gets total portfolio price based on initial math
total_porftolio_price = 0
for stock in full_portfolio:
    total_porftolio_price += (stock['price']*stock['quantity'])

# This increase quantity of stocks smartly until we reach the total to invest
should_i_loop = 1
while should_i_loop == 1:
    should_i_loop = 0
    for stock in full_portfolio:
        if total_porftolio_price + stock['price'] < total_to_invest:
            stock['quantity'] += 1
            total_porftolio_price += stock['price']
            should_i_loop = 1

# This removes any stocks with quantity of 0
temp_index = full_portfolio.copy()
for stock in temp_index:
    if stock['quantity'] == 0:
        full_portfolio.remove(stock)

# This sorts list based on total price
for stock in full_portfolio:
    stock['total_price'] = stock['quantity']*stock['price']
full_portfolio = sorted(full_portfolio, key = lambda i: i['total_price'],reverse=True)

# This prints out list items we care about 
print('Ticker,Quantity,Price,Total Price')
for stock in full_portfolio:
    print(f'''{stock['ticker']},{stock['quantity']},{stock['price']},{stock['total_price']}''')