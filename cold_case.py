#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
from scrapers.toronto_police_department import TorontoPoliceDepartmentScraper

def main():
  scraper = TorontoPoliceDepartmentScraper()
  scraper.scrape()

  for record in scraper.records:
    print ", ".join(record) + "\n"

if __name__ == '__main__':
  main()
