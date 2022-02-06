from bs4 import BeautifulSoup
import requests
import re

URL= "https://marvel.fandom.com/wiki/Goblin_Glider"
print("Trying: ",URL)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
print("Done with grabbing soup for ",URL)

# Scraping elements on the page to find what we need and saving to vars
title = soup.find("h1",{"class":"page-header__title"})
title = str(title).split(">")[1].split("<")[0]
title = re.sub(r'\s', '', title)


categories = soup.findAll("li", {"class": "category normal"})
print(categories)
categories = str(categories).split(">")

cat_list = []
for el in categories:
    if "Category:" in el:
        a = el.split("Category:")[1]
        a = a.split('"')[0]
        cat_list.append(a)
print("Found categories ",cat_list, " for ",URL)

#length = 0
#for tag in soup.findAll(True):
#    length += int(len(soup.find(tag.name).text))
#print("Found length ",length, " for ",el)

print("DATA:,\n",title,cat_list)