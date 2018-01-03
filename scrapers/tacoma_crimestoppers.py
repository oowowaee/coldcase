#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import Scraper
from record import Record
from record_element import RecordElement

from address_finder import AddressFinder
from age_extractor import AgeExtractor

from cached_property import cached_property
import re
import datefinder
import pdb

class TacomaCrimeStoppersRecordElement(RecordElement):
  @cached_property
  def text(self):
    return self._element.text

  @cached_property
  def name(self):
    return self._element.find_element_by_tag_name('h3').text

  @cached_property
  def image(self):
    return self._element.find_element_by_tag_name('img').get_attribute('src')

  @cached_property
  def description(self):
    return [el.text for el in self._element.find_elements_by_tag_name('p')]


class TacomaCrimeStoppersRecord(Record):
  RECORD_CONTAINER = '.profile_container'
  ELEMENT_CLASS = TacomaCrimeStoppersRecordElement

  @classmethod
  def include_record(cls, element):
    unsolved = 'DATE SOLVED' not in element.text
    identified = 'UNIDENTIFIED' not in element.name
    return unsolved and identified

  @property
  def location(self):
    return AddressFinder.find_addresses(self.description) + ', Tacoma'

  @property
  def multiple(self):
    name = self._element.name
    return 'Victims' in name or '&' in name

  @property
  def image(self):
    image_src = self._element.image
    return '' if 'john-doe' in image_src else image_src

  @property
  def description(self):
    return "  ".join(self._element.description).replace('\n', '  ')

  @property
  def date(self):
    new_text = re.sub('([0-9]+)[\s-]years?[\s-]old', '', self.description)
    dates = datefinder.find_dates(new_text)
    # datefinder is throwing false positives for 38-years-old

    return dates.next().strftime("%B %d, %Y")

  def _get_name(self):
    return self._element.name.replace('VICTIM ', '').title()


class TacomaCrimeStoppersScraper(Scraper):
  BASE_URL = 'http://www.tpcrimestoppers.com/case.php?cid=2'
  LINK_CONTAINER = '.case a'
  NAVIGATE_TO_LINKS = True
  PAGINATION_SELECTOR = 'a.next'
  RECORDS_CONTAINER = '.cases'
  RECORD_CLASS = TacomaCrimeStoppersRecord
