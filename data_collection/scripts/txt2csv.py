#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:51:41 2017

@author: jaerock
"""

import sys
from progressbar import ProgressBar

def main():
    if len(sys.argv) != 2:
        print('Give me a file name.')
        return
    
    fname = sys.argv[1]
    csv_fname = fname.replace('.txt','.csv') 
 
    bar = ProgressBar()
    with open(fname) as in_file:
        with open(csv_fname, 'w') as out_file:
            for line in in_file:
                line = line.strip()
                if (line == ''):
                   continue
                fname, steering_angle, throttle = line.split()
                new_line = fname + ',' + steering_angle + ',' + throttle + '\n'
                out_file.write(new_line)

if __name__ == '__main__':
    main()