#!/usr/bin/python

import os
import sys
import time
import imp
import math
import data_dir
import cartesian_config
import TA_error
import macro

IGNORE_CHAR = ['#', ' ', '\n']
n_tests_total = 0
n_tests_fail = 0
n_tests_error = 0
n_tests_not_existed = 0

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

def extract_macro(parser):
  """
  extract macro form parse
  parrser is  a dict ex:{"example" : 123}
  return list
  """
  mac_ele_list = []
  mac_num = parser["mac_num"]
  if parser["mac_use"] == "all":
    mac_num = int(parser["mac_num"])
    for i in range(1, mac_num+1):
      ele = set_macro_ele(parser, i)
      mac_ele_list.append(ele)
  else:
    """
    assign macro number not all
    """
    mac_no_list = parser["mac_use"].split()
    for no in mac_no_list:
      ele = set_macro_ele(parser, int(no))
      mac_ele_list.append(ele)
  return mac_ele_list

def set_macro_ele(parser, ele_no):
  return {"mac_no": ele_no
        , "mac_name": parser["mac_"+str(ele_no)]
        , "mac_ori": parser["mac_"+str(ele_no)+"_ori"]
        , "mac_ori_assert": parser["mac_"+str(ele_no)+"_ori_assert"]
        , "lower_bound": int(parser["mac_"+str(ele_no)+"_lower_bound"])
        , "lower_bound_assert": parser["mac_"+str(ele_no)+"_lower_bound_assert"]
        , "upper_bound": int(parser["mac_"+str(ele_no)+"_upper_bound"])
        , "upper_bound_assert": parser["mac_"+str(ele_no)+"_upper_bound_assert"]}



class Test(object):
  def __init__(self, test_info):
    self.test_cfg_path = test_info["test_cfg_dir"]+test_info["test_name"]+".cfg"  
    self.test_dir = test_info["test_dir"]
    self.test_name = test_info["test_name"]
    self.FTlevel = test_info["FTlevel"]
    self.parser = {}
    self.flag = 0
    self.macro = test_info["macro"]
    self.macro_ele_list = []
    self.macro_list = [] #use to store each element's value can be changed 
    self.macro_assert = True

    self.main()

  def __setattr__(self, name, value):
    object.__setattr__(self, name, value)
    #if name == "macro_list":
    #  print self.macro_list
    if name == "macro_list" and self.macro == "open" and self.flag == 1:
      #print self.macro_list
      self._macro_list_change()
      self.flag = 0


  def set_macro_list(self, macro_list):
    self.macro_list = macro_list
  def set_flag(self, flag):
    self.flag = flag

  def _set_run_func(self):
    """
    load module from test and get entry run func
    """
    f, p, d = imp.find_module(self.test_name, [self.test_dir])
    test_module = imp.load_module(self.test_name, f, p , d)
    f.close()
    run_func = getattr(test_module, "run_%s" % self.test_name)
    return run_func
    

  def _macro_list_change(self):
    """
    when macro list change 
    """
    self._update_parser()
    self._update_macro_assert()
    self.run()

  def _update_parser(self):
    """
    update parser by macro_list
    """
    for i in range(0, len(self.macro_ele_list)):
      self.parser[self.macro_ele_list[i]["mac_name"]] = str(self.macro_list[i])

  def _update_macro_assert(self):
    """
    update macro assert result
    """
    self.macro_assert = True
    is_ori = True
    for i in range(0, len(self.macro_ele_list)):
      if self.macro_list[i] != int(self.macro_ele_list[i]["mac_ori"]):
        is_ori = False
        break
    if not is_ori:
      for i in range(0, len(self.macro_ele_list)):
        if int(self.macro_ele_list[i]["mac_ori"]) > self.macro_list[i]:
          if self.macro_ele_list[i]["lower_bound_assert"] == "False":
            self.macro_assert = False
            break
        else:
          if self.macro_ele_list[i]["upper_bound_assert"] == "False":
            self.macro_assert = False
            break


  def _parse_test_cfg(self):
    """
    parse test cfg
    """
    try:
      self.parser = cartesian_config.Parser(self.test_cfg_path).get_dicts().next()
    except Exception, e:
      raise Exception("test case : "+self.test_name+", cfg file problem")

  def run(self):
    #run test case
    global n_tests_fail
    try:
      try:
        t_begin = time.time()
        run_func = self._set_run_func()
        run_func()
      finally:
        t_end = time.time()
        t_elapsed = t_end - t_begin
    except TA_error.Assert_Error, e:
      #test case failed
      n_tests_fail += 1
      print_fail(self.test_name,t_elapsed)
      print e.content
    except TA_error.Preprocess_Error, e:
      #preprocess has some problems
      n_tests_fail += 1
      print_error(self.test_name,t_elapsed)
      print e.content
    except TA_error.Process_Error, e:
      #process has some problems
      n_tests_fail += 1
      print_error(self.test_name,t_elapsed)
      print e.content
    except TA_error.Postprocess_Error, e:
      #postprocess has some problems
      print e.content

  def main(self):
    self._parse_test_cfg()  #parse test cfg file
    if self.macro == "open":
      #print "open"
      self.macro_ele_list = extract_macro(self.parser)
      macro.new_macro(self.macro_ele_list,self)
    else:
      """
      no macro, only run once
      """
      self.run()

def transfer_co_to_tests_list(f_name, tests_list):
  """
  transfer *.co content to tests_list
  """
  f = open(os.path.join(data_dir.COMBINATION_TESTS_DIR, f_name+".co"),'r')
  line = f.readline().rstrip('\n')
  file_type = ""
  test_dir = ""
  test_cfg_dir = ""
  macro_type = "close"
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
    elif line == "!m":
      macro_type = "open"
    elif line == "!m!":
      macro_type = "close"
    else:
      if not line[0] in IGNORE_CHAR:
        if file_type == "co":
          transfer_co_to_tests_list(line, tests_list)
        else:
          tests_list.append(
            set_test_dict(
            line, test_dir, test_cfg_dir, file_type, macro_type))
    line = f.readline().rstrip('\n')




def set_test_dict(test_name, test_dir, test_cfg_dir, FTlevel, macro = "close"):
  """
  set test dict
  macro :default is "close"
  """
  #print macro
  return {"test_name": test_name, "test_dir": test_dir
    , "test_cfg_dir": test_cfg_dir, "FTlevel": FTlevel, "macro": macro}


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
  print("test name: "+test_name+" "+bcolors.PASS + "PASS" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_fail(test_name, time):
  print("test name: "+test_name+" "+bcolors.FAIL + "FAIL" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_error(test_name, time):
  print("test name: "+test_name+" "+bcolors.ERROR + "ERROR" +
                 bcolors.ENDC + " (%.2f s)" % time)


def run_tests(options):
  """
  accroding to tests_list to run all tests
  """
  test_lists = set_tests_list(options)
  for test in test_lists:
    if check_test_exist(test):
          t = Test(test)
    else:
      n_tests_not_existed += 1





def old_run_tests (options):
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



if __name__ == "__main__":
  parser = cartesian_config.Parser("../tests/L1_tests/cfg/test1.cfg").get_dicts().next()
  mac_ele_list = extract_macro(parser)
  #print mac_ele_list
  macro.macro(mac_ele_list)




