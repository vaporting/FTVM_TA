import sys
from testagent import TA_error

def run_test1():
  print "test1"
  raise TA_error.Assert_Error("test1 assert exception")
