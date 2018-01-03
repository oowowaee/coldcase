#!/usr/bin/env python
# -*- coding: utf-8 -*-

from address_finder import AddressFinder
from age_extractor import AgeExtractor
from record_element import RecordElement
import pdb

# Wraps the extracted page data.
class Record:
  RECORD_CLASS = None               # CSS Class for container wrapping an individual record
  ELEMENT_CLASS = RecordElement

  @classmethod
  def from_element(cls, element, **kwargs):
    element = cls.ELEMENT_CLASS(element)
    record = cls(element)

    if cls.include_record(element):
      record.source = kwargs.get('source', '')
      element.populate_fields()
      return record
    return None

  @classmethod
  def include_record(cls, element):
    return True

  def __init__(self, element):
    self._element = element
    self.source = ''
    if self.multiple:
      self.name = 'Multiple'
      self.gender = ''
      self.age = ''
    else:
      self.name = self._get_name()
      self.gender = self._get_gender()
      self.age = self._get_age()
    return

  @property
  def multiple(self):
    return False

  @property
  def description(self):
    return self._element.description.replace('\n', '  ')

  @property
  def identifier(self):
    return ''
  
  @property
  def latitude(self):
    return ''

  @property
  def longitude(self):
    return ''

  @property
  def image(self):
    return self._element.image

  @property
  def date(self):
    return self._element.date

  @property
  def location(self):
    return AddressFinder.find_addresses(self.description)

  @property
  def manner_of_death(self):
    return self._determine_manner_of_death(self.description)

  def _get_age(self):
    return AgeExtractor.find_age(self.description)

  def _get_name(self):
    return self._element.name

  def _get_gender(self):
    if 'male' in self.description:
      return 'Male'
    elif 'female' in self.description:
      return 'Female'
    elif 'his' in self.description:
      return 'Male'
    elif 'her' in self.description:
      return 'Female'
    elif 'woman' in self.description:
      return 'Female'
    return ''

  def _determine_manner_of_death(self, text):
    text = text.lower()

    if 'gunshot' in text or 'shooting' in text or 'shot' in text:
      return 'shooting'
    elif 'stab' in text:
      return 'stabbing'
    elif 'hit and run' in text or 'hit & run' in text:
      return 'hit and run'
    elif 'fire' in text or 'arson' in text:
      return 'fire'
    return ''

  def to_array(self, fields):
    return [getattr(self, field) for field in fields]