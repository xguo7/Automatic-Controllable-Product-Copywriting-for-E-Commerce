#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:24:53 2021

@author: xiaojie.guo
"""
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("task", type=str, default="split")
parser.add_argument("data_path", type=str, help="data path")
parser.add_argument("save_path", type=str, help="save path")
parser.add_argument("-n", type=int, default=8, help="process num to use")
parser.add_argument("--debug", type=int, default=-1, help="load little data")
parser.add_argument("--delimiters", type=list, default=["！", "。", "；"], help="load little data")

args = parser.parse_args()

