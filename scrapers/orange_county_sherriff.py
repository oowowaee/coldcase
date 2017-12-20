#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import Scraper
from record import Record
from record_element import RecordElement
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from dateutil.relativedelta import relativedelta
from cached_property import cached_property

import re
import pdb

class OrangeCountySherriffRecordElement(RecordElement):
  @cached_property
  def image(self):
    return self._element.find_element_by_tag_name('img').get_attribute('src')

  @cached_property
  def body(self):
    return self._element.find_element_by_tag_name('td').text


class OrangeCountySherriffRecord(Record):
  RECORD_CONTAINER = '#case-card-section table table tr:nth-child(2)'
  ELEMENT_CLASS = OrangeCountySherriffRecordElement

  @classmethod
  def include_record(cls, element):
    return 'Doe' not in element.body

  @cached_property
  def image(self):
    image_src = self._element.image
    return '' if 'john-doe' in image_src else image_src

  @cached_property
  def location(self):
    pattern = re.compile("(?<=Location:).*?(?=\n)")
    return pattern.search(self._element.body).group(0)

  @cached_property
  def date(self):
    pattern = re.compile("(?<=Date Murdered:).*?(?=\n)")
    date = pattern.search(self._element.body).group(0).strip()
    date = datetime.strptime(date, '%d/%m/%y')

    return date.strftime("%B %d, %Y")

  @cached_property
  def description(self):
    pattern = re.compile("(?<=Description:).*?(?=\n\nSubmit)")
    return pattern.search(self._element.body).group(0)

  def _get_name(self):
    return self._element.body

  def _get_gender(self):
    pattern = re.compile("(?<=Sex:).*?(?=\n)")
    gender = pattern.search(self._element.body).group(0).strip()    
    return 'Male' if gender == 'M' else 'Female'

  def _get_age(self):
    pattern = re.compile("(?<=Age:).*?(?=Race)")
    age = pattern.search(self._element.body).group(0).strip()

    if age == 0:
      pattern = re.compile("(?<=DOB:).*?(?=\n)")
      dob = pattern.search(self._element.body).group(0).strip()      
      dob = datetime.strptime(dob, '%d/%m/%y')
      age = relativedelta(self._get_date(), dob).years

    return age


class OrangeCountySherriffScraper(Scraper):
  BASE_URL = 'https://www.ocso.com/Crime-Information/Unresolved-Homicide'
  LINK_CONTAINER = 'a[id*="__lnk_"]'
  NAVIGATE_TO_LINKS = True
  PAGINATION_CLASS = 'a[id$="lnkNext"]'
  RECORDS_CONTAINER = '#unsolved-homicides'
  RECORD_CLASS = OrangeCountySherriffRecord

  def scrape(self):
    self._get_initial_page()
    self._visit_image_links()

  def _visit_image_links(self):
    link_idx = 0

    try:
      while True:
        link_class = 'a[id$="__lnk_{0}"]'.format(link_idx)
        print link_class
        self._browser.find_element_by_css_selector(link_class).click()
        print 'Scraping record {0}'.format(link_idx)
        self._harvest_link_information()
        link_idx += 1
    except NoSuchElementException:
      print 'No record {0}'.format(link_idx)
      if self._navigate_to_next_page():
        print self._browser.current_url
        self._visit_image_links()
    return

  def _harvest_link_information(self):
    self._add_record()
    pdb.set_trace()
    self._browser.find_element_by_link_text('<< Return').click()
    return