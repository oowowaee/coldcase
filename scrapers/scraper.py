#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import pdb

# SELENIUM CHEATSHEET
#   driver.page_source
#   driver.title

#      iframe = self._browser.find_elements_by_tag_name('iframe')[0]
#      self._browser.switch_to_frame(iframe)

class Scraper:
  def __init__(self):
    self._records = []
    return

  def scrape(self):
    self._get_initial_page()

    if self.NAVIGATE_TO_LINKS:
      links = self._get_all_record_links()
      self._build_records_from_links(links)

    self._browser.close()
    return


class SeleniumScraper(Scraper):
  def __init__(self, webdriver_instance, required_fields):
    Scraper.__init__(self)
    self._browser = webdriver_instance
    self._required_fields = required_fields
    return

  @property
  def records(self):
    return [record.to_array(self._required_fields) for record in self._records]
  
  def _navigate_to_next_page(self):
    try:
      self._browser.find_element_by_css_selector(self.PAGINATION_CLASS).click()
      return True
    except NoSuchElementException:
      return False

  def _get_initial_page(self):
    self._browser.get(self.BASE_URL)
    return

  def _build_records_from_links(self, links):
    for link in links:
      print 'Scraping ' + link
      self._browser.get(link)
      record = self._build_record(link)
      if record:
        self._records.append(record)

  def _build_record(self, link):
    element = self._browser.find_element_by_css_selector(self.RECORD_CLASS.RECORD_CONTAINER)
    if self.RECORD_CLASS.include_record(element):
      try:
        return self.RECORD_CLASS(element, source = link)
      except NoSuchElementException:
        print 'Could not find element in ' + link
        return None

  def _get_all_record_links(self):
    links = self._get_page_links()

    if self.PAGINATION_CLASS:
      while self._navigate_to_next_page():
        links += self._get_page_links()

    return links

  def _get_page_links(self):
    page_links = self._browser.find_elements_by_css_selector(self.LINK_CONTAINER)
    return [link.get_attribute('href') for link in page_links]


class BeautifulSoupScraper(Scraper):
  def __init__(self):
    return

  def _get_initial_page(self):
    return