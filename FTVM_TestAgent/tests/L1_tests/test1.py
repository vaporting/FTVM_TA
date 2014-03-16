import sys
import time
from testagent import TA_error

def run_test1():
  print "test1"
  time.sleep(1)
  raise TA_error.Assert_Error("test1 assert exception")
