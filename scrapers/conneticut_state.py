#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import Scraper
from record import Record
import re

class ConneticutRecord(Record):
  RECORD_CONTAINER = '.case-details'

  def _get_name(self, element):
    first_name = element.find_element_by_class_name('victim-name').text
    last_name = element.find_element_by_class_name('victim-surname').text.capitalize()
    return " ".join([first_name, last_name])

  def _get_image(self, element):
    return element.find_element_by_css_selector('.victim-photo a').get_attribute('href')

  def _get_location(self, element):
    return ''

  def _get_age(self, element):
    return element.find_elements_by_css_selector('.victim-details p')[0].text.replace('Age: ', '')

  def _get_gender(self, element):
    return element.find_elements_by_css_selector('.victim-details p')[1].text.replace('Gender: ', '')

  def _get_date(self, element):
    date_str = element.find_elements_by_css_selector('.victim-details p')[2].text.replace('Murdered on: ', '')
    # datetime.datetime.strptime(date_str, "%B %d, %Y")
    return date_str 

  def _get_description(self, element):
    return element.find_elements_by_css_selector('.victim-details div')[0].text

  def _get_latitude_longitude(self, element):
    google_url = element.find_element_by_css_selector('#google-map a').get_attribute('href')
    pattern = re.compile("(?<=ll=).*(?=&z)")
    match = pattern.search(google_url)

    return match.group(0).split(',') if match.group(0) else Record._get_latitude_longitude(self)

  def _get_manner_of_death(self, element):
    if 'gunshot' in self.description:
      return 'shooting'
    elif 'stab' in self.description:
      return 'stabbing'
    return ''

class ConneticutStateScraper(Scraper):
  BASE_URL = 'http://www.ct.gov/csao/cwp/view.asp?a=1798&q=291462'
  LINK_CONTAINER = '.timeline-event a'
  NAVIGATE_TO_LINKS = True
  PAGINATION_CLASS = None
  RECORDS_CONTAINER = '#timeline'
  RECORD_CLASS = ConneticutRecord
