#!/usr/bin/env python
# -*- coding: utf-8 -*-

from address_finder import AddressFinder
import unittest

class TestAddressFinder(unittest.TestCase):
  def test_ignores_irrelevant_numbers(self):
    str = '38-year-old Jeremy Martin.  At 1:35 a.m. on Tuesday December 5th, 2017, his home located in the 1400 block of S. 37th St.'
    self.assertEqual(AddressFinder.find_addresses(str), '1400 block of S. 37th St.')

  def test_finds_address_with_direction_first(self):
    str = '1400 block of S. 37th St.'
    self.assertEqual(AddressFinder.find_addresses(str), str)

  def test_finds_address_with_direction(self):
    str = '2100 block of Sunset Drive W.'
    self.assertEqual(AddressFinder.find_addresses(str), str)

  def test_finds_intersections(self):
    str = '38th St. and Pacific Ave.'
    self.assertEqual(AddressFinder.find_addresses(str), str)

  def test_finds_intersections(self):
    str = 'Pacific Ave. S. and Portland Ave.'
    self.assertEqual(AddressFinder.find_addresses(str), str)

  @unittest.skip("Context is a future concern")
  def test_considers_context(self):
    str = 'frequented the area of Pacific Ave. S. and Portland Ave. in the City of Tacoma.  He was last seen in the area of 38th St. and Pacific Ave.'
    self.assertEqual(AddressFinder.find_addresses(str), '38th St. and Pacific Ave.')

  def test_considers_only_capitals(self):
    str = 'area of Sydenham Street & Creemore Avenue'
    self.assertEqual(AddressFinder.find_addresses(str), 'Sydenham Street & Creemore Avenue')

  def test_ignores_911_calls(self):
    str = '911 call at 30 Titan Road'
    self.assertEqual(AddressFinder.find_addresses(str), '30 Titan Road')

  def test_ignores_punctuation(self):
    str = '4:05 a.m., police responded to shooting, on Meadowbank Road near Keane Avenue'
    self.assertEqual(AddressFinder.find_addresses(str), 'Meadowbank Road near Keane Avenue')

  def test_finds_roadway(self):
    str = 'police responded to an emergency call in the area of Lake Shore Boulevard E and Don Roadway'
    self.assertEqual(AddressFinder.find_addresses(str), 'Lake Shore Boulevard E and Don Roadway')

  def test_finds_westway(self):
    str = 'Wincott Drive and The Westway'
    self.assertEqual(AddressFinder.find_addresses(str), str)

  def test_tinds_way(self):
    str = 'a motel room in the abandoned Rainier Motel building located in the 9800 block of South Tacoma Way in '
    self.assertEqual(AddressFinder.find_addresses(str), '9800 block of South Tacoma Way')

  def test_finds_bridge(self):
    str = 'seen alive on Thursday March 31st, 2005.  Mason’s vehicle was found a week later on April 6th, 2005, in the City of Tacoma.  On October 23rd, 2005, the remains of Michelle Mason were found in blackberry bushes below the 34th St. Bridge.'
    self.assertEqual(AddressFinder.find_addresses(str), '34th St. Bridge')

if __name__ == '__main__':
    unittest.main()