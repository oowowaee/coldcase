#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
from scrapers.toronto_police_department import TorontoPoliceDepartmentScraper
from scrapers.tacoma_crimestoppers import TacomaCrimeStoppersScraper
from selenium import webdriver

import csv

def main():
  # path_to_chromedriver = '/home/tally/projects/chromedriver_27'
  # browser = webdriver.Chrome(executable_path = path_to_chromedriver)

  browser = webdriver.PhantomJS()
  FIELDS = ('name', 'location', 'image', 'source', 'gender', 'age', 'description', 'manner_of_death', 'date', 'latitude', 'longitude')

  records = []

  # scraper = TorontoPoliceDepartmentScraper(browser, FIELDS)
  # scraper.scrape()

  scraper = TacomaCrimeStoppersScraper(browser, FIELDS)
  scraper.scrape()

  records += scraper.records
  outfile = 'csv/' + scraper.__class__.__name__ + '.csv'

  with open(outfile, 'wb') as csvfile:
    writer = csv.writer(csvfile,
                        delimiter=',',
                        quoting=csv.QUOTE_MINIMAL)

    writer.writerow(FIELDS)

    for record in records:
      writer.writerow([unicode(s).encode('utf-8') for s in record])

if __name__ == '__main__':
  main()
