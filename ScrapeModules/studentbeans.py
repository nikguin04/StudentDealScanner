# https://www.studentbeans.com/student-discount/dk/all?source=nav

import requests
from bs4 import BeautifulSoup
import json

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

# this is currently a very simple scrape since we can scrape 100 offes at a time, and studentbeans only has about 60+- student offers right now, so we just need to handle a single page of json
# edit: for scraping final discount link and long description we need to scrape every companies page on studentbeans page itself
def StartScrape(): 
    pagenum = 1
    jsnScrape = {
        "modulesite": "studentbeans",
        "dealdata": []
    }   

    sbquery = requests.post(
        "https://graphql.studentbeans.com/graphql/v1/query",
        headers={"User-Agent": useragent},
        json={
            "operationName": "AllOffersPageFilterQuery",
            "variables": {
                "cursor": "MTI",
                "count": 100,
                "countryCodes": ["dk"],
                "redemptionClasses": ["online", "instore"],
                "visible": True,
                "closedConsumerGroup": "student",
                "sortBy": {
                    "column": "START_DATE",
                    "direction": "DESC"
                }
            },
            "query": "query AllOffersPageFilterQuery($count: Int, $countryCodes: [String], $cursor: String, $redemptionClasses: [String], $visible: Boolean, $closedConsumerGroup: String, $sortBy: OfferSort) {\n  accountsViewer {\n    offers(\n      first: $count\n      countryCodes: $countryCodes\n      after: $cursor\n      redemptionClasses: $redemptionClasses\n      visible: $visible\n      closedConsumerGroup: $closedConsumerGroup\n      sortBy: $sortBy\n    ) {\n      ...LoadMoreOfferListOffers\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LoadMoreOfferListOffers on OffersConnection {\n  totalCount\n  edges {\n    cursor\n    __typename\n  }\n  pageInfo {\n    hasNextPage\n    endCursor\n    __typename\n  }\n  ...OfferListOffers\n  __typename\n}\n\nfragment OfferListOffers on OffersConnection {\n  edges {\n    node {\n      uid\n      ...OfferTileOffer\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OfferTileOffer on Offer {\n  uid\n  impressionContent {\n    id\n    type\n    version\n    __typename\n  }\n  ...OfferContainerOffer\n  ...OfferLinkOffer\n  ...OfferSubtitleOffer\n  ...OfferTitleOffer\n  ...OfferAlertOffer\n  ...OfferRedemptionClassOffer\n  ...OfferImageOffer\n  ...OfferLogoOffer\n  __typename\n}\n\nfragment OfferContainerOffer on Offer {\n  expired\n  activeFlags {\n    edges {\n      node {\n        live\n        flag {\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OfferLinkOffer on Offer {\n  brand {\n    slug\n    __typename\n  }\n  country {\n    slug\n    __typename\n  }\n  expired\n  slug\n  __typename\n}\n\nfragment OfferSubtitleOffer on Offer {\n  subtitle\n  __typename\n}\n\nfragment OfferTitleOffer on Offer {\n  title\n  expired\n  __typename\n}\n\nfragment OfferAlertOffer on Offer {\n  expiringSoon\n  discountEndDate\n  closedConsumerGroup\n  baseRedemptionType {\n    exclusive\n    __typename\n  }\n  activeFlags {\n    edges {\n      node {\n        live\n        flag {\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OfferRedemptionClassOffer on Offer {\n  brand {\n    name\n    slug\n    __typename\n  }\n  country {\n    slug\n    __typename\n  }\n  expired\n  redemptionClass\n  redemptionType\n  baseRedemptionType {\n    androidStore\n    iosStore\n    installInstructions\n    __typename\n  }\n  __typename\n}\n\nfragment OfferImageOffer on Offer {\n  expired\n  defaultImage\n  defaultImageSmall\n  brand {\n    name\n    __typename\n  }\n  activeFlags {\n    edges {\n      node {\n        live\n        flag {\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OfferLogoOffer on Offer {\n  brand {\n    name\n    logo\n    __typename\n  }\n  __typename\n}"
        }
    )

    next_data_list = {} # list next_data by the company "slug" name (eg:emp)
    for jsnobj in sbquery.json()["data"]["accountsViewer"]["offers"]["edges"]:
        offerobj = jsnobj["node"]
        brand_name_slug = offerobj["brand"]["slug"]
        sb_company_data_link = "https://www.studentbeans.com/student-discount/dk/" + brand_name_slug
        # check if we already have scraped this, if not, request link
        if not brand_name_slug in next_data_list:
            comp_data=requests.get(sb_company_data_link)
            cd_soup=BeautifulSoup(comp_data.content,"html.parser")
            next_data= json.loads(cd_soup.select("#__NEXT_DATA__")[0].contents[0])
            next_data_list[brand_name_slug] = next_data
            print("Scraped data for: " + offerobj["brand"]["name"] + " (Studentbeans)")




        """return
        print(next_data_list[brand_name_slug])
        print()
        jsnScrape["dealdata"].append({
            "name": offerobj["brand"]["name"],
            "title": offerobj["title"],
            "desc_short": offerobj["subtitle"],
            "desc_long": "unknown",
            "discount_link_provider": "https://www.studentbeans.com/student-discount/dk/" + brand_name_slug + "?source=category&offer=" + offerobj["slug"],
            "discount_links": {"default": "NONE YET"},
            "images": [offerobj["brand"]["logo"], offerobj["defaultImage"]],
            "category_unparsed": "unknown"
        })"""

    for nextobj in next_data_list.keys():
        offers = next_data_list[nextobj]["props"]["pageProps"]["offers"]
        for offer in offers:
            node = offer["node"]
            jsnScrape["dealdata"].append({
                "name": node["brand"]["name"],
                "title": node["title"],
                "desc_short": node["subtitle"],
                "desc_long": node["description"],
                "discount_link_provider": "https://www.studentbeans.com/student-discount/dk/" + node["brand"]["slug"] + "?source=category&offer=" + node["slug"],
                "discount_links": {"default": node["baseRedemptionType"]["affiliateLink"]},
                "images": [node["brand"]["logo"], node["defaultImageSmall"]],
                "category_unparsed": "unknown"
            })
    
    #print("Done scraping!")
    return jsnScrape

