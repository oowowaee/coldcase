#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pdb

#1400 block of S. 37th St.
#2100 block of Sunset Drive W
#38th St. and Pacific Ave.
#frequented the area of Pacific Ave. S. and Portland Ave. in the City of Tacoma.  He was last seen in the area of 38th St. and Pacific Ave.
#911 call at 30 Titan Road
#4:05 a.m., police responded to shooting, on Meadowbank Road

class AddressFinder:
  STREET_SUFFIX = '(Avenue|Street|Road|Drive|St\.?|Rd\.?|Ave\.?)'
  DIRECTIONS = '(East|E\.?|West|W\.?|North|N\.?|South|S\.?)'
  STREET_NAME = '(([A-Z]|[0-9]+)[a-z\.]*\s){0,3}'

  @classmethod
  def find_addresses(cls, str):
    address_substring = "([0-9]+[a-z]*\s(block of )?)?{0}(\s{1})?{2}(\s{3})?".format(cls.STREET_NAME,
                                                                                     cls.DIRECTIONS,
                                                                                     cls.STREET_SUFFIX,
                                                                                     cls.DIRECTIONS)

    pattern1_string = "{0} (and|&|near) {1}".format(address_substring, address_substring)

    address_pattern = re.compile(address_substring)
    intersection_pattern = re.compile(pattern1_string)

    address = intersection_pattern.search(str)

    if not address:
      address = address_pattern.search(str)

    try:
      return address.group(0)
    except AttributeError:
      return ''