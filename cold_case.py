#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
from scrapers.toronto_police_department import TorontoPoliceDepartmentScraper
from scrapers.tacoma_crimestoppers import TacomaCrimeStoppersScraper
from scrapers.orange_county_sherriff import OrangeCountySherriffScraper
from selenium import webdriver
import argparse

import csv

def main():
  FIELDS = ('name', 'location', 'date', 'manner_of_death', 'source', 'image', 'gender', 'age', 'description', 'latitude', 'longitude')
  records = []
  command_args = _get_args()

  if command_args.chrome:
    path_to_chromedriver = '/home/tally/projects/chromedriver_27'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
  else:
    browser = webdriver.PhantomJS()

  browser.implicitly_wait(5)

  # scraper = TorontoPoliceDepartmentScraper(browser, FIELDS)
  # scraper.scrape()

  # scraper = TacomaCrimeStoppersScraper(browser, FIELDS)
  # scraper.scrape()

  scraper = OrangeCountySherriffScraper(browser, FIELDS)
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

def _get_args():
  help_text = "{}"
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--chrome", action='store_true',
                      help=help_text.format("flag to use chrome browswer"))

  return parser.parse_args()

if __name__ == '__main__':
  main()
