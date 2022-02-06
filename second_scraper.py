from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

def halo_search_2(halo_list):
    conn = sqlite3.connect("HaloData.db")
    c = conn.cursor()
    print(f"Connected to DB! Starting to scrape {len(halo_list)} pages...")
    ct = datetime.datetime.now()
    print("Time at start: ", ct)

    for index,el in enumerate(halo_list):
        try:
            URL= f"https://www.halopedia.org{el}"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")


            # Scraping elements on the page to find what we need and saving to vars
            title = soup.find("h1",{"class":"pagetitle"})
            title = str(title).split(">")[1].split("<")[0]

            categories = soup.find("div", {"class": "mw-normal-catlinks"})
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
            
            c.execute("INSERT INTO halo_db_2 VALUES(?,?,?)",(str(title),str(cat_list),int(length)))
            conn.commit()

            print(f"Done with {index}/{len(halo_list)}")
        except:
            print(f"Skipping {el}")
            pass
    print("Done scraping!")
    ct = datetime.datetime.now()
    print("Time at end: ", ct)




halo_names = open("halo_links_to_check.txt","r").readlines()
halo_search_2(halo_names)
