from bs4 import BeautifulSoup
import requests
import datetime
import re
import mysql.connector
from mysql.connector import errorcode

# Connect to Amazon DB

try:
  cnx =mysql.connector.connect(user='admin', password='andrewwikiscrape12345',
                              host='wiki-scrape.c3khuyuubsmy.us-east-2.rds.amazonaws.com',
                              database='testing2'
                              )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()



# This is for fandom sites!

def wiki_spider(stop_num, url,cate): 
    URL= url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    link_list = []

    links = soup.find_all("a",href = True)
    for link in links:
        a = str(link).split("href=")[1]
        a = a.split('"')
        a = a[1]
        if a[0] == "/":
            link_list.append(a)

    print(f"Found data from {url}")
    print("Length of list before recursive scraping: ",len(link_list))
    lll = 0
    len_list = []

    for el in link_list:
        lll = len(link_list)
        try: 
            URL= f"{url}{el}"
            print("Trying... ",f"{url}{el}")
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            links = soup.find_all("a",href = True)
            for link in links:
                a = str(link).split("href=")[1]
                a = a.split('"')
                a = a[1]
                if a[0] == "/":
                    link_list.append(a)
            link_list = list(set(link_list))
            print("Length of list after some recursive scraping: ",len(link_list))
            len_list.append(len(link_list))
            
            # Stop Conditions
            if len_list[-1] == len_list[-6]:
                break
            if len(link_list) > stop_num:
                break
        except:
            print("skipping: ",el)
            #link_list = list(set(link_list))
    cnx.commit()


    link_list = list(set(link_list))
    print(link_list)
    print("Storing for later...")
    for el in link_list:
        try:
            sql = "INSERT INTO wiki_scraping_links_stage (link, type) VALUES (%s, %s)"
            val = (str(el), str(cate))
            cursor.execute(sql, val)
        except mysql.connector.Error as err:
            print(err)


    print("Dumping list to disk")
    textfile = open(f"{cate}_links_to_check.txt", "w")
    for element in link_list:
        textfile.write(f"{element}\n")
    textfile.close()
    print(f"Dumped {len(link_list)} links to disk. Ready for scraping.")
    print(f"see {cate}_links_to_check.txt for more details")


    def wiki_search(cate_list):
        print("Initiating Scrape...")
        print("Starting to scrape {len(cate_list)} pages...")
        ct = datetime.datetime.now()
        print("Time at start: ", ct)

        for index,el in enumerate(cate_list):
            try:
                URL= str(f"{url}{el}")
                print("Trying: ",URL)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                #print("Done with grabbing soup for ",URL)

                # Scraping elements on the page to find what we need and saving to vars
                title = soup.find("h1",{"class":"page-header__title"})
                title = str(title).split(">")[1].split("<")[0]
                title = re.sub(r'\s', '', title)
                

                categories = soup.findAll("li", {"class": "category normal"})
                categories = str(categories).split(">")
                cat_list = []
                for el in categories:
                    if "Category:" in el:
                        a = el.split("Category:")[1]
                        a = a.split('"')[0]
                        cat_list.append(a)
                

                length = 0
                for tag in soup.findAll(True):
                    length += int(len(soup.find(tag.name).text))
                
                print("Found title ",title, " for ",URL)
                print("Found categories ",cat_list, " for ",URL)
                print("Found length ",length, " for ",el)
                
                print("Putting data into DB")
                
                try:
                    sql = "INSERT INTO wiki_scraping_data_stage (title,categories,length,type) VALUES (%s,%s,%s,%s)"
                    val = (str(title),str(cat_list),int(length),str(cate))
                    cursor.execute(sql, val)
                    print("Data inserted into DB!")
                except mysql.connector.Error as err:
                    print(err)
            
            except:
                pass
            
            print(f"Done with {index}/{len(cate_list)}")
            cnx.commit()
        print("Done scraping!")
        ct = datetime.datetime.now()
        print("Time at end: ", ct)
        


    wiki_names = open(f"{cate}_links_to_check.txt","r").readlines()
    wiki_search(wiki_names)

#wiki_spider(20000,"https://marvel.fandom.com","marvel")
#wiki_spider(20000,"https://sonic.fandom.com","sonic")
#wiki_spider(20000,"https://starcraft.fandom.com","starcraft")
#wiki_spider(20000,"https://spiderman.fandom.com","spiderman")
#wiki_spider(20000,"https://stargate.fandom.com","stargate")
#wiki_spider(20000,"https://starwars.fandom.com","starwars")
#wiki_spider(20000,"https://fantendo.fandom.com","fantendo")
#wiki_spider(20000,"https://femalevillains.fandom.com","femalevillains")
#wiki_spider(20000,"https://fightingfantasy.fandom.com","fightingfantasy")
#wiki_spider(20000,"https://finalfantasy.fandom.com","finalfantasy")
#wiki_spider(20000,"https://ffxiclopedia.fandom.com","ffxiclopedia")
#wiki_spider(20000,"https://fireemblem.fandom.com","fireemblem")
#wiki_spider(20000,"https://forgottenrealms.fandom.com","forgottenrealms")
wiki_spider(20000,"https://wowpedia.fandom.com/","wowpedia")
wiki_spider(20000,"https://runescape.fandom.com/","runescape")
wiki_spider(20000,"https://tvdatabase.fandom.com/","tv")
wiki_spider(20000,"https://tardis.fandom.com/","doctorwho")
wiki_spider(20000,"https://fortnite.fandom.com/","fortnite")





cursor.close()
