#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cached_property import cached_property
from scraper import Scraper
from record import Record
from record_element import RecordElement

import pdb
import re
from selenium.common.exceptions import NoSuchElementException

class TorontoRecordElement(RecordElement):
  @cached_property
  def first_name(self):
    return self._element.find_element_by_class_name('victim-name').text

  @cached_property
  def last_name(self):
    return self._element.find_element_by_class_name('victim-surname').text

  @cached_property
  def image(self):
    try:
      return self._element.find_element_by_css_selector('.victim-photo a').get_attribute('href')
    except NoSuchElementException:
      return ''

  @cached_property
  def age(self):
    return self._details[0].text
  
  @cached_property
  def gender(self):
    return self._details[1].text

  @cached_property
  def date(self):
    return self._details[2].text

  @cached_property
  def description(self):
    return self._element.find_elements_by_css_selector('.victim-details div')[0].text

  @cached_property
  def google_url(self):
    return self._element.find_element_by_css_selector('#google-map a').get_attribute('href')

  @cached_property
  def _details(self):
    return self._element.find_elements_by_css_selector('.victim-details p')


class TorontoRecord(Record):
  RECORD_CONTAINER = '.case-details'
  ELEMENT_CLASS = TorontoRecordElement

  @property
  def date(self):
    return self._element.date.replace('Murdered on: ', '')

  @property
  def latitude(self):
    return self._latitude_longitude()[0]

  @property
  def longitude(self):
    return self._latitude_longitude()[1]

  def _latitude_longitude(self):
    try:
      google_url = self._element.google_url
      pattern = re.compile("(?<=ll=).*(?=&z)")
      match = pattern.search(google_url)

      return match.group(0).split(',') if match.group(0) else ['', '']
    except NoSuchElementException:
      return ['', '']

  def _get_name(self):
    first_name = self._element.first_name
    last_name = self._element.last_name.title()
    return ' '.join([first_name, last_name]).strip()

  def _get_age(self):
    return self._element.age.replace('Age: ', '')

  def _get_gender(self):
    return self._element.gender.replace('Gender: ', '')


class TorontoPoliceDepartmentScraper(Scraper):
  BASE_URL = 'https://www.torontopolice.on.ca/homicide/search.php'
  LINK_CONTAINER = '.timeline-event a'
  NAVIGATE_TO_LINKS = True
  PAGINATION_CLASS = None
  RECORD_CLASS = TorontoRecord
