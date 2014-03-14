import sys
from testagent import TA_error
import time

def run_L1_ft_vm_crash():
  print "L1_ft_vm_crash"
  time.sleep(1)
  raise TA_error.Assert_Error("L1_ft_vm_crash assert exception")
