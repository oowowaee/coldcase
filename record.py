#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Record:
  FIELDS = ('name', 'description', 'location', 'image', 'source', 'gender', 'age', 'manner_of_death', 'date', 'latitude', 'longitude')

  @classmethod
  def include_record(cls, element):
    return True

  def __init__(self, element, **kwargs):
    self.description = self._get_description(element)

    self.name = self._get_name(element)
    self.location = self._get_location(element)
    self.date = self._get_date(element)
    self.image = self._get_image(element)
    self.gender = self._get_gender(element)
    self.age = self._get_age(element)
    self.latitude, self.longitude = self._get_latitude_longitude(element)
    self.manner_of_death = self._get_manner_of_death(element)
    self.source = kwargs.get('source', '')
    return

  def _get_description(self, element):
    return ''

  def _get_latitude_longitude(self, element):
    return ['', '']

  def _get_image(self, element):
    raise NotImplementedError

  def _get_name(self, element):
    raise NotImplementedError

  def _get_location(self, element):
    raise NotImplementedError

  def _get_date(self, element):
    raise NotImplementedError

  def _get_gender(self, element):
    raise NotImplementedError

  def _get_age(self, element):
    raise NotImplementedError

  def _get_manner_of_death(self, element):
    return self._determine_manner_of_death(self.description)

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

  def to_csv(self):
    return [getattr(self, field) for field in self.FIELDS]