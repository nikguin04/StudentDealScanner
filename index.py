import sys
import json
import os

sys.path.append("ScrapeModules")
import sheerid, studentbeans, studiz

if not os.path.isdir("Output"):
    os.mkdir("Output")
    
scrapeModules = {
    "Sheerid": {
        "module": sheerid,
        "function": "StartScrape"
    },
    "Studentbeans": {
        "module": studentbeans,
        "function": "StartScrape"
    },
    "Studiz": {
        "module": studiz,
        "function": "StartScrape"
    }
}

def init():
    print("Available modules:")
    keys = list(scrapeModules.keys())
    for i in range(0, len(keys)): # print module names and key int indexes
        print(keys[i] + ": (" + str(i) + ")")    

    moduleindex = int(input("Enter module to scrape (0-" + str(len(keys)-1) + "): "))
    print("Scraping data for " + keys[moduleindex])
    mod_func = getattr(scrapeModules[keys[moduleindex]]["module"], scrapeModules[keys[moduleindex]]["function"]) # get function
    json_result = mod_func()

    with open("Output/" + keys[moduleindex] + "_output.json", "w") as outfile:
        outfile.write(json.dumps(json_result, separators=(',', ':')))
    
    print("Scraping is complete, and data has been saved (Returning to start function)")
    init()

init()