import sys
import json
import os

sys.path.append("ScrapeModules")
import sheerid, studentbeans

if not os.path.isdir("Output"):
    os.mkdir("Output")
    

sheeridData = sheerid.StartScrape()
#print(sheeridData)
with open("Output/sheerid_output.json", "w") as outfile:
    outfile.write(json.dumps(sheeridData, separators=(',', ':')))

studentbeansData = studentbeans.StartScrape()
#print(studentbeansData)
with open("Output/studentbeans_output.json", "w") as outfile:
    outfile.write(json.dumps(studentbeansData, separators=(',', ':')))