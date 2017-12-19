#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pdb

#1400 block of S. 37th St.
#2100 block of Sunset Drive W
#38th St. and Pacific Ave.
#frequented the area of Pacific Ave. S. and Portland Ave. in the City of Tacoma.  He was last seen in the area of 38th St. and Pacific Ave.

class AddressFinder:

  @classmethod
  def find_addresses(cls, str):
    pattern1 = re.compile("[0-9]+.*(St\.|Rd\.|Ave\.|Avenue|Street|Road|Drive)(East|E\.|West|W\.|North|N\.|South|\S.)")
    try:
      return pattern1.search(str).group(0)
    except AttributeError:
      return ''