#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 21:34:59 2019

@author: laureanonisenbaum
"""

"""Test the wikitablescrape script on four articles."""

import os
import shutil

import wikitablescrape

# Delete previous output folder if it exists, then create a new one
try:
    shutil.rmtree("output")
except FileNotFoundError:
    pass


wikitablescrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population",
    output_name="cities",
)

wikitablescrape.scrape(
    url="https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area",
    output_name="areas",
)


# Move all CSV folders into a single 'output' folder
os.makedirs("output")
#shutil.move("./mountains", "./output")
shutil.move("./cities", "./output")
shutil.move("./areas", "./output")

