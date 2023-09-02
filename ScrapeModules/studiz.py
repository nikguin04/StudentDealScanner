# https://www.studiz.dk/studierabatter

import requests
from bs4 import BeautifulSoup, NavigableString
import json

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def StartScrape():
    jsnScrape = {
        "modulesite": "studiz",
        "dealdata": []
    }

    baseUrl = "https://www.studiz.dk"
    studizRes = requests.get("https://www.studiz.dk/studierabatter?online_offline%5B%5D=online&online_offline%5B%5D=offline&distance=750") # Get all rebates on this link (static link, should not be changed)
    studizSoup = BeautifulSoup(studizRes.content, 'html.parser')
    dealsdiv = studizSoup.find("div", {"class": "search-providers-result"})
    dealsgroup = dealsdiv.find_all("a", {"class": "provider_details"})

    for deal in dealsgroup:
        
        print("Getting: " + baseUrl + deal["href"])
        dealRes = requests.get(baseUrl + deal["href"])
        #print(dealRes.content)
        dealSoup = BeautifulSoup(dealRes.content, 'html.parser')

        # Get overall content 
        provider_info = dealSoup.find("div", {"class": "provider-info-new"})
        name = provider_info.find("h2", {"class": "text-center"}).contents[0]

        desc_long_html = provider_info.find("div", {"class": "company_description"})
        desc_long = desc_long_html.find("p").contents[0] if desc_long_html.find("p") != None else desc_long_html.contents[4]
        while (not isinstance(desc_long, NavigableString)): # We have hit a long desc with a <span> capsule, can be multiple
            desc_long = desc_long.contents[0]
        discount_link_provider = baseUrl + deal["href"]
        image_logo = provider_info.find("div", {"class": "logo"}).contents[1]["src"]

        # Categories are only included in the overall deal data page, so we have to get it from previous request
        category_unparsed = deal["data-tags-list"]

        """print(name)
        print(desc_long)
        print(discount_link_provider)
        print(image_logo)
        print(category_unparsed)"""

        # Loop through all deals (usually 1 but can be more)
        individualDealRow = dealSoup.find("div", {"class": "providers-show"}).find("div", {"class": "offset-sm-1"}).contents[1]
        for iDeal in individualDealRow.find_all("a"):
            discount_link = iDeal["href"]
            image_deal = iDeal.find("img")["src"]
            title = iDeal.find("h2", {"class": "text-start"}).contents[0]

            jsnScrape['dealdata'].append({
                "name": name,
                "title": title,
                "desc_short": "unknown",
                "desc_long": desc_long,
                "discount_link_provider": discount_link_provider,
                "discount_links": {"default": discount_link},
                "images": [image_logo, image_deal],
                "category_unparsed": category_unparsed
            })
            #if (type(name) == Tag)
        print("Scraped data for: " + name + " (Studiz)")
        #print(jsnScrape['dealdata'][len(jsnScrape['dealdata'])-1])
    return jsnScrape