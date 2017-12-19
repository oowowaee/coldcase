#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
from scrapers.toronto_police_department import TorontoPoliceDepartmentScraper
from scrapers.tacoma_crimestoppers import TacomaCrimeStoppersScraper
from selenium import webdriver

def main():
  path_to_chromedriver = '/home/tally/projects/chromedriver_27'
  browser = webdriver.Chrome(executable_path = path_to_chromedriver)

  # scraper = TorontoPoliceDepartmentScraper(browser)
  # scraper.scrape()

  scraper = TacomaCrimeStoppersScraper(browser)
  scraper.scrape()

  for record in scraper.records:
    print ", ".join(record) + "\n"

if __name__ == '__main__':
  main()
