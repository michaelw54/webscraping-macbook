from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

my_url = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=macbook+pro&N=-1&isNodeId=1'

# opening up connection and grabbing the page to webscrape
uClient = uReq(my_url)

# reading the html content
page_html = uClient.read()

# closing the content
uClient.close()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", {"class": "item-container"})

filename = "macbooks.csv"
f = open(filename, "w")
headers = "Model, Price, Shipping\n"
f.write(headers)

for container in containers:
    info  = container.findAll("div", {"class": "item-info"})
    if len(info) != 0:
        model = info[0].findAll("a", {"class": "item-title"})
        if len(model) != 0:
            model = model[0].text.replace(",", "|").strip()
        else:
            continue
        price1 = info[0].findAll("div", {"class": "item-action"})
        if len(price1) != 0:
            price2 = price1[0].ul.findAll("li", {"class": "price-current"})
            shipping = price1[0].ul.findAll("li", {"class": "price-ship"})
            if len(shipping) != 0:
                shipping = shipping[0].text.strip()
            else:
                shipping = "N/A"
            if len(price2) != 0 and price2[0].strong != None and price2[0].sup != None:
                price = "$" + price2[0].strong.text + price2[0].sup.text
                price = price.strip().replace(",", "")
            else:
                price = "N/A"
        else: 
            price = "N/A"
            shipping = "N/A"
    else:
        continue
    print("\nmodel: " + model)
    print("price: " + price)
    print("shipping: " + shipping)
    f.write(model + "," + price + "," + shipping + "\n")

f.close()
