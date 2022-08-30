from bs4 import BeautifulSoup
import requests

website = input("Enter Product: ")
shopify_web = requests.get(website).text


soup = BeautifulSoup(shopify_web, "lxml")

baseShopifyURL = website[:website.find(".com")]
baseShopifyURL = baseShopifyURL + ".com/"

variantString = """for (var attr in meta) {
  window.ShopifyAnalytics.meta[attr] = meta[attr];
}"""

scripts = soup.find_all("script")

for script in scripts:
    if(variantString in script.text):
         variant = script.text


variant = variant[variant.find("var")+23:]
variant = variant[variant.find("variants")+12:]
numOfVariants = variant.count('"id"')

sizeList = []
variantList = []
addToCartLinks = []

sku = ""
price = ""


for x in range(numOfVariants):
    
    miniString = variant[:variant.find('}')]
    variantList.append(miniString[miniString.find('"id"')+5:miniString.find('"id"')+19 ])

    if x ==0:
        price = miniString[miniString.find('"price"') + 8: miniString.find("name") - 2]

    miniString = miniString[miniString.find('"name"'):]
    sizeList.append(miniString[miniString.find(':') +2:miniString.find(',') -1 ])

    if x == 0:
        sku = miniString[miniString.find('"sku"') + 7: miniString.find('}')]
    
    addToCartLinks.append(baseShopifyURL + variantList[x] + ":1")

    print(variantList[x] +" " +sizeList[x] + "\t" + addToCartLinks[x])
    variant = variant[variant.find('}') +3 :]

price = [*price]

price.insert(-2,'.')
price.insert(0,'$')
pString = ""
for x in price:
    pString += x
print("Backend SKU is " + sku + " Price is " + pString)
