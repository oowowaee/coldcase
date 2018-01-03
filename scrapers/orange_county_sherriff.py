#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import Scraper
from record import Record
from record_element import RecordElement

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from dateutil.relativedelta import relativedelta
from cached_property import cached_property
import re
import pdb
import datefinder

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
    body = element.body.lower()
    return body.startswith('Unknown') or body.startswith('Unidentified')

  @property
  def image(self):
    image_src = self._element.image
    return '' if image_src in ['https://www.ocso.com/Portals/0/UnresolvedHomicides/photo-not-available.jpg',
                               'https://www.ocso.com/Portals/0/UnresolvedHomicides/',
                               'https://www.ocso.com/Portals/0/UnresolvedHomicides/DOE.png'] else image_src

  @property
  def location(self):
    pattern = re.compile('(?<=Location:).*?(?=\n)')
    return pattern.search(self._element.body).group(0).strip()

  @cached_property
  def date(self):
    # There is at least one case where the murder date is listed incorrectly,
    # so try to read it from the description first
    
    dates = datefinder.find_dates(self.description)

    try:
      try:
        date = dates.next()
      except StopIteration:
        pattern = re.compile('(?<=Date Murdered:).*?(?=\n)')
        date = pattern.search(self._element.body).group(0).strip()
        date = datetime.strptime(date, '%m/%d/%Y')

      return date.strftime('%B %d, %Y')

    except ValueError:
      pdb.set_trace()
      return ''

  @cached_property
  def description(self):
    pattern = re.compile('(?<=Description:).*?(?=\n\nSubmit)')
    return pattern.search(self._element.body).group(0).strip()

  def _get_name(self):
    pattern = re.compile('.*?(?=\n)')
    return pattern.match(self._element.body).group(0).strip()

  def _get_gender(self):
    try:
      pattern = re.compile('(?<=Sex:).*?(?=\n)')
      gender = pattern.search(self._element.body).group(0).strip()    
      return 'Male' if gender[0] == 'M' else 'Female'
    except IndexError:
      # There is a record lacking a gender
      return ''

  def _get_age(self):
    pattern = re.compile('(?<=Age:).*?(?=Race)')
    age = pattern.search(self._element.body).group(0).strip()

    # Unfortunately age field is sometimes wrong and set as 0
    if age == '0':
      pattern = re.compile('(?<=DOB:).*?(?=\n)')
      dob = pattern.search(self._element.body).group(0).strip()
      try:   
        dob = datetime.strptime(dob, '%m/%d/%Y')
      except ValueError:
        # Zafer Barkasie lacks a DOB
        return ''
      date = datetime.strptime(self.date, '%B %d, %Y')
      age = relativedelta(date, dob).years

    return age


class OrangeCountySherriffScraper(Scraper):
  BASE_URL = 'https://www.ocso.com/Crime-Information/Unresolved-Homicide'
  LINK_CONTAINER = 'a[id*="__lnk_"]'
  NAVIGATE_TO_LINKS = True
  PAGINATION_SELECTOR = 'a[id$="lnkNext"]'
  RECORDS_CONTAINER = '#unsolved-homicides'
  RECORD_CLASS = OrangeCountySherriffRecord

  def scrape(self):
    self._get_initial_page()
    self._visit_image_links()

  # Navigate to each image link on the page
  # When we run out of links, increment the page counter, navigate to the
  # next page and start again.
  # When no next link exists any longer, we're done!
  def _visit_image_links(self, page = 0):
    link_idx = 0

    print 'page {0}'.format(page)

    # We go too fast sometimes, so wait until all the js has finished and the
    # page we're on is marked as such
    wait = WebDriverWait(self._browser, 5)
    element = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.CommandButton'), str(page + 1)))

    try:
      while True:
        link_class = 'a[id$="__lnk_{0}"]'.format(link_idx)
        el = self._browser.find_element_by_css_selector(link_class)
        self._scroll_up_from_element(el)
        el.click()
        print 'Scraping record {0}'.format(link_idx)
        self._harvest_link_information()
        link_idx += 1
    except NoSuchElementException:
      if self._navigate_to_next_page(True):
        self._visit_image_links(page + 1)
    return

  def _harvest_link_information(self):
    self._add_record()
    el = self._browser.find_element_by_link_text('<< Return')
    self._scroll_up_from_element(el)
    el.click()
    return