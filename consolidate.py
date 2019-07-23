'''
Consolidates parallel corpus files using resource files

Requires resource files to have .en and .ne extensions for
English and Nepali resource files respectively

Requires resource files in corpus/ folder
Requires data-cleaning/functions.py

Creates train.en and train.ne on the same directory as this file

This script hasn't been properly tested
'''

from data_cleaning.functions import collect

collect('corpus/', 'train')