# https://www.sheerid.com/shoppers/studentdeals/
# https://scrapeops.io/python-web-scraping-playbook/best-python-html-parsing-libraries/

import requests
from bs4 import BeautifulSoup
import json

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def StartScrape():
    pagenum = 1
    jsnScrape = {
        "modulesite": "sheerid",
        "dealdata": []
    }   
    result = False
    while not result:
        result = ScrapeNextPage(jsnScrape, pagenum)
        pagenum += 1
    
    print("Done scraping! total pages: " + str(pagenum-1))
    return jsnScrape

def ScrapeNextPage(jsnScrape, pagenum):
    page = requests.get(
        'https://www.sheerid.com/shoppers/studentdeals/?pagenum={0}&sorting=featured&category=Student'.format(pagenum),
        headers={"User-Agent": useragent}
    )
    soup = BeautifulSoup(page.content, 'html.parser')
    dealsdiv = soup.find("div", {"class": "products-wrapper"})

    if dealsdiv == None:
        return True
    else :
        dealsdiv = dealsdiv.contents[1]

    for citem in dealsdiv.find_all('div', 'deal'):
        details_link = citem.find('a')['href']

        #print("Scraping for " + citem['data-brands'].encode("utf-8"))
        details_page = requests.get(
            details_link,
            headers={"User-Agent": useragent}
        )
        details_soup = BeautifulSoup(details_page.content, 'html.parser')
        details_div = details_soup.find("div", "product")
        discount_links = {}
        for link in details_div.findAll("div", "single-btn-wrapper"):
            ahref = link.contents[1]
            discount_links[str(ahref.contents[0]).strip()] = ahref['href']
        jsnScrape['dealdata'].append({
            "name": citem['data-brands'],
            "title": details_div.find("h1", "product_title").contents[0],
            "desc_short": "unknown",
            "desc_long": massReplaceStr(str(details_div.find("div", "woocommerce-product-details__short-description").contents[1]), {"<p>":"", "</p>":"\n", "<br/>":"\n", "<h2>":"## ", "</h2>":"\n", "<b>":"**", "</b>":"**"}), # markdown readability
            "discount_link_provider": details_link,
            "discount_links": discount_links,
            "images": [(details_div.find_all("img", "size-shop_single")[1]['src'] if details_div.find("img", "size-shop_single") != None else '')], # using find_all with index 1 because html parser sees no script as queryable html
            "category_unparsed": citem['data-industries']
        })
        print("Scraped data for: " + str(citem['data-brands'].encode("utf-8")) + " (Sheerid)")

def massReplaceStr(str, jsndict): 
    for key in jsndict.keys():
        str = str.replace(key, jsndict[key])
    return str