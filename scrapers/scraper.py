#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pdb
import glob
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver

# SELENIUM CHEATSHEET
#   driver.page_source
#   driver.title

#      iframe = self._browser.find_elements_by_tag_name('iframe')[0]
#      self._browser.switch_to_frame(iframe)

class Scraper:
  FIELDS = ('name', 'location', 'source', 'gender', 'age', 'manner_of_death', 'date')

  def __init__(self):
    self._records = []
    return

  def scrape(self):
    self._get_initial_page()

    if self.NAVIGATE_TO_LINKS:
      self._build_records_from_links()
    return

class SeleniumScraper(Scraper):
  def __init__(self):
    path_to_chromedriver = '/home/tally/projects/chromedriver_27'
    self._browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    return

  def _get_initial_page(self):
    self._browser.get(self.BASE_URL)
    return

  def _build_records_from_links():
    links = self._get_record_links()

    for link in links[0:2]:
      self._browser.get(link)
      record = self._browser.find_elements_by_css_selector(self.RECORD_CLASS.RECORD_CONTAINER)
      self._records.append(self._build_record(record))
      
  def _get_record_links(self):
    links = self._browser.find_elements_by_css_selector(self.LINK_CONTAINER)
    return [link.get_attribute('href') for link in links]

  def _build_record(self):
    return

class BeautifulSoupScraper(Scraper):
  def __init__(self):
    return

  def _get_initial_page(self):
    return