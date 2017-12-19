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

  # Todo, this really shouldn't be a class method
  @classmethod
  def include_record(cls, element):
    unsolved = 'DATE SOLVED' not in element.text
    identified = 'UNIDENTIFIED' not in element.find_element_by_tag_name('h3').text
    return unsolved and identified

  def _determine_multiple(self, element):
    name = element.find_element_by_tag_name('h3').text
    return 'Victims' in name or '&' in name

  def _get_name(self, element):
    name = element.find_element_by_tag_name('h3').text.replace('VICTIM ', '')
    return name.title()

  def _get_image(self, element):
    return element.find_element_by_tag_name('img').get_attribute('src')

  def _get_date(self, element):
    new_text = re.sub('([0-9]+)[\s-]years?[\s-]old', '', self.description)
    dates = datefinder.find_dates(new_text)
    # datefinder is throwing false positives for 38-years-old

    return dates.next().strftime("%B %d, %Y")

  def _get_description(self, element):
    text = [el.text for el in element.find_elements_by_tag_name('p')]
    return "  ".join(text).replace('\n', '  ')


class TacomaCrimeStoppersScraper(SeleniumScraper):
  BASE_URL = 'http://www.tpcrimestoppers.com/case.php?cid=2'
  LINK_CONTAINER = '.case a'
  NAVIGATE_TO_LINKS = True
  PAGINATION_CLASS = 'a.next'
  RECORDS_CONTAINER = '.cases'
  RECORD_CLASS = TacomaCrimeStoppersRecord
