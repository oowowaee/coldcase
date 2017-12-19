#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pdb

#1400 block of S. 37th St.
#2100 block of Sunset Drive W
#38th St. and Pacific Ave.
#frequented the area of Pacific Ave. S. and Portland Ave. in the City of Tacoma.  He was last seen in the area of 38th St. and Pacific Ave.

class AddressFinder:
  STREET_NAMES = '(St\.|Rd\.|Ave\.|Avenue|Street|Road|Drive)'
  DIRECTIONS = '(East|E\.|West|W\.|North|N\.|South|S\.)'

  @classmethod
  def find_addresses(cls, str):
    address_substring = "[0-9]*([A-Z][^\s]*\s){{1,3}}{0}(\s{1})?".format(cls.STREET_NAMES, cls.DIRECTIONS)
    pattern1_string = "[0-9]+([^\s]*\s){{1,8}}{0}(\s{1})?".format(cls.STREET_NAMES, cls.DIRECTIONS)
    pattern2_string = "{0} (and|&) {1}".format(address_substring, address_substring)

    pattern1 = re.compile(pattern1_string)
    pattern2 = re.compile(pattern2_string)

    address = pattern1.search(str)

    if not address:
      address = pattern2.search(str)

    try:
      return address.group(0)
    except AttributeError:
      return ''