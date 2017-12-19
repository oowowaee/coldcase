#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pdb

#38-year-old
#38 year old
#38 years old

class AgeExtractor:

  @classmethod
  def find_age(cls, str):
    pattern1 = re.compile("([0-9]+)[\-\s]years?[\-\s]old")

    try:
      return pattern1.search(str).groups(0)[0]
    except AttributeError:
      return ''