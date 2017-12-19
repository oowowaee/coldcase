#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapers.toronto_police_department import TorontoPoliceDepartmentScraper

def main():
  s = TorontoPoliceDepartmentScraper()
  s.scrape()

if __name__ == '__main__':
  main()
