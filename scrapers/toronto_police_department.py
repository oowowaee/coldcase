#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper import SeleniumScraper
from record import Record

class TorontoRecord(Record):
  RECORD_CONTAINER = '.case-details'

  def __init__(self):
    return

class TorontoPoliceDepartmentScraper(SeleniumScraper):
  BASE_URL = 'https://www.torontopolice.on.ca/homicide/search.php'
  LINK_CONTAINER = '.timeline-event a'
  NAVIGATE_TO_LINKS = True
  PAGINATION_CLASS = None
  RECORDS_CONTAINER = '#timeline'
  RECORD_CLASS = TorontoRecord
