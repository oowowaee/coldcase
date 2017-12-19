#!/usr/bin/env python
# -*- coding: utf-8 -*-

from address_finder import AddressFinder
import unittest

#1400 block of S. 37th St.
#2100 block of Sunset Drive W
#38th St. and Pacific Ave.
#frequented the area of Pacific Ave. S. and Portland Ave. in the City of Tacoma.  He was last seen in the area of 38th St. and Pacific Ave.

class TestAddressFinder(unittest.TestCase):
  def test_ignores_irrelevant_numbers(self):
    str = '38-year-old Jeremy Martin.  At 1:35 a.m. on Tuesday December 5th, 2017, his home located in the 1400 block of S. 37th St.'
    self.assertEqual(AddressFinder.find_addresses(str), '1400 block of S. 37th St.')

  def test_finds_address_with_direction_first(self):
    str = '1400 block of S. 37th St.'
    self.assertEqual(AddressFinder.find_addresses(str), '1400 block of S. 37th St.')

  def test_finds_address_with_direction(self):
    str = '2100 block of Sunset Drive W.'
    self.assertEqual(AddressFinder.find_addresses(str), '2100 block of Sunset Drive W.')

  def test_finds_intersections(self):
    str = '38th St. and Pacific Ave.'
    self.assertEqual(AddressFinder.find_addresses(str), '38th St. and Pacific Ave.')

  def test_finds_intersections(self):
    str = 'Pacific Ave. S. and Portland Ave.'
    self.assertEqual(AddressFinder.find_addresses(str), 'Pacific Ave. S. and Portland Ave.')

  def test_considers_context(self):
    str = 'frequented the area of Pacific Ave. S. and Portland Ave. in the City of Tacoma.  He was last seen in the area of 38th St. and Pacific Ave.'
    self.assertEqual(AddressFinder.find_addresses(str), '38th St. and Pacific Ave.')

  def test_considers_only_capitals(self):
    str = 'area of Sydenham Street & Creemore Avenue'
    self.assertEqual(AddressFinder.find_addresses(str), 'Sydenham Street & Creemore Avenue')

if __name__ == '__main__':
    unittest.main()