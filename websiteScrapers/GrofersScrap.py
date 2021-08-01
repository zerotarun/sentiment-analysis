from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as soup


def perKgPriceCalculator(itemName):
    req = Request(
        'https://grofers.com/s/?q=' + itemName + '&suggestion_type=0&t=1',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    uClient = urlopen(req, timeout=20)
    pageHtml = uClient.read()
    uClient.close()

    # creating a csv
    fileName = 'searchResults\\' + itemName + 'Prices.csv'
    f = open(fileName, 'w')
    csvHeaders = "Name, ListedQuantity, NetQuantity, ListedPrice, PricePerKg\n"
    f.write(csvHeaders)

    pageSoup = soup(pageHtml, 'html.parser')

    chips = pageSoup.findAll("div", {"class": "plp-product"})
    print(len(chips))
    name_fail, listed_quantity_fail, price_fail, price_per_kg_fail = 0, 0, 0, 0
    for chip in chips:
        # name of the chip
        try:
            name = chip.findAll("div", {"class": "plp-product__name--box"})[0].text
        except:
            name_fail+=1

        # quantity
        try:
            if (chip.findAll("div", {"class": "plp-product__quantity"})[0].span):
                temp = chip.findAll("div", {"class": "plp-product__quantity"})[0].span.text
                textQuantity = temp
                netQuantity = eval(temp.replace("x", "*").replace("g", "").replace("gm", "").strip())
            else:
                textQuantity = "not found"
                netQuantity = "not found"
        except:
            listed_quantity_fail+=1

        # price
        try:
            if (chip.findAll("div", {"class": "display--inline-block@mobile"})[0].span):
                listedPrice = chip.findAll("div", {"class": "display--inline-block@mobile"})[0].span.text[1:]
            else:
                listedPrice = "not found"
        except:
            price_fail+=1

        # price per kg calculation
        try:
            if (listedPrice != "not found" and netQuantity != "not found"):
                pricePerKg = (int(listedPrice) / netQuantity) * 1000
            else:
                pricePerKg = "cannot be calculated"
            f.write(name + "," + textQuantity + "," + str(netQuantity) + "," + listedPrice + "," + str(
                pricePerKg) + "," + "\n")
        except:
            price_per_kg_fail+=1

    f.close()
    print("name_fail:::"+str(name_fail))
    print("listed_quantity_fail:::"+str(listed_quantity_fail))
    print("price_fail:::"+str(price_fail))
    print("price_per_kg_fail:::"+str(price_per_kg_fail))