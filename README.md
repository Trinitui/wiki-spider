# wiki-spider
## A personal project to generate large datasets
Utilizing web scraping packages for python and cheap database hosting at AWS, this script crawls fandom wikis for relevant links to other pages in that wiki, captures them in a python list, then goes one-by-one through that list capturing the HTML of the page and extracting relevant information. Github Actions runs the script. 