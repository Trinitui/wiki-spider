# wiki-spider
[![Wiki Scraper Status: ](https://github.com/Trinitui/wiki-spider/actions/workflows/python-app.yml/badge.svg)](https://github.com/Trinitui/wiki-spider/actions/workflows/python-app.yml)

## A personal project to generate large datasets
Utilizing web scraping packages for python and cheap database hosting at AWS, this script crawls fandom wikis for relevant links to other pages in that wiki, captures them in a python list, then goes one-by-one through that list capturing the HTML of the page and extracting relevant information. Github Actions runs the script. 