#!/usr/bin/python
"""
Record the data directory path
ex: root_path  
"""
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(_current_dir, "../")
TESTS_DIR = os.path.join(ROOT_DIR, "tests/")
TESTS_CFG_DIR = os.path.join(TESTS_DIR, "cfg/")
GENERAL_TESTS_DIR = os.path.join(TESTS_DIR, "general_tests/")
GENERAL_TESTS_CFG_DIR = os.path.join(GENERAL_TESTS_DIR, "cfg/")
L1_TESTS_DIR = os.path.join(TESTS_DIR, "L1_tests/")
L1_TESTS_CFG_DIR = os.path.join(L1_TESTS_DIR, "cfg/")
L2_TESTS_DIR = os.path.join(TESTS_DIR, "L2_tests/")
L2_TESTS_CFG_DIR = os.path.join(L2_TESTS_DIR, "cfg/")
COMBINATION_TESTS_DIR = os.path.join(TESTS_DIR, "combination_tests/")




if __name__ == "__main__":
  print ROOT_DIR,"\n"
  print TESTS_DIR,"\n"
  print TESTS_CFG_DIR,"\n"
  print L1_TESTS_DIR,"\n"
  print L1_TESTS_CFG_DIR,"\n"
  print L2_TESTS_DIR,"\n"
  print L2_TESTS_CFG_DIR,"\n"
  print COMBINATION_TESTS_DIR,"\n"
  print os.path.abspath(__file__)

