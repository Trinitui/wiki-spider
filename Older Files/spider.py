from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime


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
            if len_list[-1] == len_list[-3]:
                break
            if len(link_list) > stop_num:
                break
        except:
            print("skipping: ",el)
            #link_list = list(set(link_list))


    print("Dumping list to disk")
    link_list = list(set(link_list))
    textfile = open(f"{cate}_links_to_check.txt", "w")
    for element in link_list:
        textfile.write(f"{element}\n")
    textfile.close()
    print(f"Dumped {len(link_list)} links to disk. Ready for scraping.")
    print(f"see {cate}_links_to_check.txt for more details")


    def wiki_search(cate_list):
        print("Initiating Scrape...")
        conn = sqlite3.connect("HaloData.db")
        c = conn.cursor()
        print(f"Connected to DB! Starting to scrape {len(cate_list)} pages...")
        ct = datetime.datetime.now()
        print("Time at start: ", ct)

        for index,el in enumerate(cate_list):
            try:
                URL= str(f"{url}{el}")
                print("Trying: ",URL)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                print("Done with grabbing soup for ",URL)

                # Scraping elements on the page to find what we need and saving to vars
                title = soup.find("h1",{"class":"pagetitle"})
                title = str(title).split(">")[1].split("<")[0]
                print("Found title ",title, " for ",URL)

                categories = soup.find("div", {"class": "mw-normal-catlinks"})
                categories = str(categories).split(">")
                cat_list = []
                for el in categories:
                    if "Category:" in el:
                        a = el.split("Category:")[1]
                        a = a.split('"')[0]
                        cat_list.append(a)
                print("Found categories ",cat_list, " for ",URL)

                length = 0
                for tag in soup.findAll(True):
                    length += int(len(soup.find(tag.name).text))
                print("Found length ",length, " for ",el)
                
                print("Putting data into DB")
                
                c.execute("INSERT INTO halo_db_2 VALUES(?,?,?,?)",(str(title),str(cat_list),int(length),str(cate)))
                conn.commit()
                print("Data inserted into DB!")
            except:
                pass
            print(f"Done with {index}/{len(cate_list)}")
        print("Done scraping!")
        ct = datetime.datetime.now()
        print("Time at end: ", ct)


    wiki_names = open(f"{cate}_links_to_check.txt","r").readlines()
    wiki_search(wiki_names)

wiki_spider(1000,"https://www.halopedia.org","halo")
#wiki_spider(1000,"https://en.uesp.net/wiki/","ES")