#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pdb
import glob
import re
import os

class Record:
  FIELDS = ('name', 'location', 'source', 'gender', 'age', 'manner_of_death', 'date')

  def __init__(self):
    return