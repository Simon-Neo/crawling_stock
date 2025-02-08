import requests
from bs4 import BeautifulSoup
import yfinance as yf

ticker = "vrt"

def find_data(soup, find_data):
    # Find the table containing the data
    table = soup.find('table')

    if table:
        # Find the row that contains 'PE Ratio'
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells and find_data in cells[0].text:
                # Extract the value from the 'Current' column (the second cell)
                try:
                    pe_ratio = cells[1].text.strip()  # current
                    return pe_ratio
                except IndexError:
                    print("Could not find PE Ratio in the 'Current' column.")
                break
    else:
        print("Table not found on the page.")

    return None

if __name__ == "__main__":

    # ticker = yf.Ticker("ARM")
    # info = ticker.info
    #
    # current_price = info['currentPrice']
    # print("yh current_price", current_price)
    # per = info.get('trailingPE', 'N/A')
    # print("yh per", per)
    # peg = info.get('pegRatio', 'N/A')
    # print("yh peg", peg)

    url = f"https://stockanalysis.com/stocks/{ticker}/financials/ratios/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')

    per =float(find_data(soup, "PE Ratio"))
    print("per", per)

    peg = float(find_data(soup, "PEG Ratio"))
    print("peg", peg)

    growth_rate = per / peg
    print("growth_rate", growth_rate)

    price_div = soup.find('div', class_='text-4xl') # font-bold transition-colors duration-300 inline-block
    current_price = float(price_div.text.strip())
    print("current_price", current_price)
    eps = current_price / per
    print("eps", eps)

    good_price = growth_rate * eps
    print()
    print(f"{ticker} peg 1 price is : {int(good_price)}", )




