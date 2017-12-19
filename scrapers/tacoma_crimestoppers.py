#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import SeleniumScraper
from record import Record
from address_finder import AddressFinder
from age_extractor import AgeExtractor

import re
import datefinder
import pdb

class TacomaCrimeStoppersRecord(Record):
  RECORD_CONTAINER = '.profile_container'
  DOMAIN = 'http://www.tpcrimestoppers.com'

  @classmethod
  def include_record(cls, element):
    return 'DATE SOLVED' not in element.text

  def _get_name(self, element):
    name = element.find_element_by_tag_name('h3').text.replace('VICTIM ', '')
    return name.title()

  def _get_image(self, element):
    return element.find_element_by_tag_name('a').get_attribute('href')

  def _get_location(self, element):
    return AddressFinder.find_addresses(self.description)

  def _get_age(self, element):
    return AgeExtractor.find_age(self.description)

  def _get_gender(self, element):
    if 'male' in self.description:
      return 'Male'
    elif 'female' in self.description:
      return 'Female'
    elif 'his' in self.description:
      return 'Male'
    elif 'her' in self.description:
      return 'Female'
    return 'Unknown'

  def _get_date(self, element):
    dates = datefinder.find_dates(self.description)
    # datefinder is throwing false positives for 38-years-old
    return dates.next().strftime("%B %d, %Y")

  def _get_description(self, element):
    text = [el.text for el in element.find_elements_by_tag_name('p')]
    return "\n".join(text)


class TacomaCrimeStoppersScraper(SeleniumScraper):
  BASE_URL = 'http://www.tpcrimestoppers.com/case.php?cid=2'
  LINK_CONTAINER = '.case a'
  NAVIGATE_TO_LINKS = True
  PAGINATION_CLASS = 'a.next'
  RECORDS_CONTAINER = '.cases'
  RECORD_CLASS = TacomaCrimeStoppersRecord
