#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cached_property import cached_property
import pdb

# Wrapper for a Selenium Element
class RecordElement:
  def __init__(self, element):
    self._element = element
    self._image = None
    self._name = None
    self._location = None
    self._gender = None
    self._description = None
    self._latitude_longitude = None
    return

  # Prefill all values
  # As we'll lose access to the page element itself when navigating away from the page
  # precache all the requisite data fields
  def populate_fields(self):
    values = [name for name, value in vars(self.__class__).items() if isinstance(value, cached_property)]
    for value in values:
      getattr(self, value)

    self._element = None
    return

  @property
  def description(self):
    return self._description or ''
  
  @property
  def latitude_longitude(self):
    return self._latitude_longitude or ['', '']

  @property
  def image(self):
    return self._image or ''

  @property
  def date(self):
    return self._date or ''

  @property
  def name(self):
    return self._name or ''

  @property
  def gender(self):
    return self._gender or ''

  @property
  def age(self):
    return self._age or ''

  @property
  def location(self):
    return self._location or ''