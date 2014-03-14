#!/usr/bin/python

import os
import sys
import time
import imp
import data_dir
import cartesian_config
import TA_error

IGNORE_CHAR = ['#', ' ', '\n']

class Bcolors(object):

    """
    Very simple class with color support.
    copied by virttest standalone_test.py
    """

    def __init__(self):
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.end = '\033[0m'
        self.HEADER = self.blue
        self.PASS = self.green
        self.SKIP = self.yellow
        self.FAIL = self.red
        self.ERROR = self.red
        self.WARN = self.yellow
        self.ENDC = self.end
        allowed_terms = ['linux', 'xterm', 'xterm-256color', 'vt100',
                         'screen', 'screen-256color']
        term = os.environ.get("TERM")
        if (not os.isatty(1)) or (not term in allowed_terms):
            self.disable()

    def disable(self):
        self.blue = ''
        self.green = ''
        self.yellow = ''
        self.red = ''
        self.end = ''
        self.HEADER = ''
        self.PASS = ''
        self.SKIP = ''
        self.FAIL = ''
        self.ERROR = ''
        self.ENDC = ''

# Instantiate bcolors to be used in the functions below.
bcolors = Bcolors()


class Test(object):
  def __init__(self, test_info):
    self.test_cfg_path = test_info["test_cfg_dir"]+test_info["test_name"]+".cfg"  
    self.test_dir = test_info["test_dir"]
    self.test_name = test_info["test_name"]
    self.FTlevel = test_info["FTlevel"]
    self.parser = {}

  def parse_test_cfg(self):
    """
    parse test cfg
    """
    try:
      self.parser = cartesian_config.Parser(self.test_cfg_path).get_dicts().next()
    except Exception, e:
      raise Exception("test case : "+self.test_name+", cfg file problem")

  def run(self):
    self.parse_test_cfg()
    #run test case
    f, p, d = imp.find_module(self.test_name, [self.test_dir])
    test_module = imp.load_module(self.test_name, f, p , d)
    f.close()
    run_func = getattr(test_module, "run_%s" % self.test_name)
    run_func()
    #end run 

def transfer_co_to_tests_list(f_name, tests_list):
  """
  transfer *.co content to tests_list
  """
  f = open(os.path.join(data_dir.COMBINATION_TESTS_DIR, f_name+".co"),'r')
  line = f.readline().rstrip('\n')
  file_type = ""
  test_dir = ""
  test_cfg_dir = ""
  while line:
    if line == "!co":
      file_type = "co"
    elif line == "!0":
      file_type = '0'
      test_dir = data_dir.GENERAL_TESTS_DIR
      test_cfg_dir = data_dir.GENERAL_TESTS_CFG_DIR
    elif line == "!1":
      file_type = '1'
      test_dir = data_dir.L1_TESTS_DIR
      test_cfg_dir = data_dir.L1_TESTS_CFG_DIR
    elif line == "!2":
      file_type = '2'
      test_dir = data_dir.L2_TESTS_DIR
      test_cfg_dir = data_dir.L2_TESTS_CFG_DIR
    else:
      if not line[0] in IGNORE_CHAR:
        if file_type == "co":
          transfer_co_to_tests_list(line, tests_list)
        else:
          tests_list.append(
            set_test_dict(
            line, test_dir, test_cfg_dir, file_type))
    line = f.readline().rstrip('\n')




def set_test_dict(test_name, test_dir, test_cfg_dir, FTlevel):
  """
  set test dict
  """
  return {"test_name": test_name, "test_dir": test_dir
    , "test_cfg_dir": test_cfg_dir, "FTlevel": FTlevel}


def set_tests_list(options):
  """
  set all tests in tests_list in this round

  """
  tests_list = []
  if options.comb != None:
    """
    multiple test cases
    """
    transfer_co_to_tests_list(options.comb, tests_list)
  if options.comb == None and options.FTlevel != None:
    """
    only one test case
    """
    test = {}
    if options.FTlevel == '0':
      test = set_test_dict(options.test, data_dir.GENERAL_TESTS_DIR
        ,data_dir.GENERAL_TESTS_CFG_DIR,options.FTlevel)
    if options.FTlevel == '1':
      test = set_test_dict(options.test, data_dir.L1_TESTS_DIR
        , data_dir.L1_TESTS_CFG_DIR, options.FTlevel)
    if options.FTlevel == '2':
      test = set_test_dict(options.test, data_dir.L2_TESTS_DIR
        , data_dir.L2_TESTS_CFG_DIR, options.FTlevel)
    tests_list.append(test)
  return tests_list

def check_test_exist(test):
  """
  check test exist or not
  return true/false
  """
  for f in os.listdir(test["test_dir"]):
    if f.endswith(".py") and (f == test["test_name"]+".py"):
      return True
  return False

def print_pass(test_name, time):
  print("test : "+test_name+" "+bcolors.PASS + "PASS" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_fail(test_name, time):
  print("test : "+test_name+" "+bcolors.FAIL + "FAIL" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_error(test_name, time):
  print("test : "+test_name+" "+bcolors.ERROR + "ERROR" +
                 bcolors.ENDC + " (%.2f s)" % time)

def run_tests (options):
  """
  accroding to tests_list to run all tests
  """
  test_start_time = time.strftime('%Y-%m-%d-%H.%M.%S')
  n_tests_total = 0 #test case total number
  n_tests_run_total = 0
  n_tests_fail = 0
  n_tests_error = 0
  n_tests_not_existed = 0
  test_lists = set_tests_list(options)
  for test in test_lists:
    test_passed = False
    n_tests_total += 1
    try:
      try:
        if check_test_exist(test):
          t = Test(test)
          t_begin = time.time()
          test_passed = t.run()
        else:
          n_tests_not_existed += 1
      finally:
        t_end = time.time()
        t_elapsed = t_end - t_begin
    except TA_error.Assert_Error, e:
      #test case failed
      n_tests_fail += 1
      print_fail(t.test_name,t_elapsed)
      print e.content
    except TA_error.Preprocess_Error, e:
      #preprocess has some problems
      n_tests_fail += 1
      print_error(t.test_name,t_elapsed)
      print e.content
    except TA_error.Process_Error, e:
      #process has some problems
      n_tests_fail += 1
      print_error(t.test_name,t_elapsed)
      print e.content
    except TA_error.Postprocess_Error, e:
      #postprocess has some problems
      print e.content


  





