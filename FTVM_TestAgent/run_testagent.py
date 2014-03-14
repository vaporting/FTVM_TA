#!/usr/bin/python
"""
test agent begin file 
"""
import sys
import os
import optparse
from testagent import data_dir
from testagent import round_test

SUPPORTED_TEST_FT_LEVEL = ['0', '1', '2']

class TestAgentParser(optparse.OptionParser):
  """
  set command line format
  """
  def __init__(self):
    optparse.OptionParser.__init__(self, usage='Usage: %prog [options]')
    
    general = optparse.OptionGroup(self, "general")
    general.add_option("-l", action="store", dest="FTlevel", 
      help="Choose test type (%s) 0 : general, 1: level1, 2: level2" %
      ", ".join(SUPPORTED_TEST_FT_LEVEL))
    general.add_option("--test", action="store", dest="test",
      default="",help=('exampe: --tests "HostOS_crashss"'))
    general.add_option("-c", action="store", dest="comb", 
      help=("example -c FTLevel1"))
    self.add_option_group(general)


class TestAgentRunner(object):
  """
  Class representing the execution of the Test Agent runner
  """
  def __init__(self):
    self.option_parser = TestAgentParser()
    self.options, self.args = self.option_parser.parse_args()
    
  
  def main(self):
    """
    main point of execution of the test runner
    """
    round_test.run_tests(self.options)
    #print round_test.set_tests_list(self.options)



if __name__ == "__main__":
  runner = TestAgentRunner()
  runner.main()
  """
  from testagent import cartesian_config
  parser = cartesian_config.Parser("./tests/L1_tests/cfg/L1_ft_vm_crash.cfg")
  a = parser.get_dicts().next()
  print parser.get_dicts().next(),"\n"
  print a[0]['pre_check_FT_hostOS_boot'],"\n\n"
  print os.listdir(data_dir.TESTS_CFG_DIR),"\n"

  for f in os.listdir(data_dir.TESTS_CFG_DIR):
    if f.endswith(".cfg"):
      print f,"\n"
  """
