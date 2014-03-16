#!/usr/bin/python
import sys
import os
import round_test


class T_setattr(object):
  def __init__(self):
    self.list = []
    self.flag = 0
  
  def __setattr__(self, name, value):
    object.__setattr__(self, name, value)
    if name == "flag" and self.flag == 1:
      print self.list
      
  

def macro(m_list, flag, r_list = [], index = 0):
  ele = m_list[index]
  cur_val = ele["lower_bound"]
  while cur_val <= ele["upper_bound"]:
    r_list.append(cur_val)
    if ele == m_list[len(m_list)-1]:
      flag = 1
      #print r_list,"\n"
    else:
      macro(m_list, flag, r_list, index+1)
    r_list.pop()
    cur_val += 1

def new_macro(m_list, test, r_list = [], index = 0):
  ele = m_list[index]
  cur_val = ele["lower_bound"]
  while cur_val <= ele["upper_bound"]:
    r_list.append(cur_val)
    if ele == m_list[len(m_list)-1]:
      test.set_flag(1)
      test.set_macro_list(r_list)
      #print r_list,"\n"
    else:
      new_macro(m_list, test, r_list, index+1)
    r_list.pop()
    cur_val += 1

def evo_macro(m_list, evo_list , index = 0):
  ele = m_list[index]
  cur_val = ele["lower_bound"]
  while cur_val <= ele["upper_bound"]:
    r_list.append(cur_val)
    if ele == m_list[len(m_list)-1]:
      print r_list,"\n"
    else:
      macro(m_list, r_list, index+1)
    r_list.pop()
    cur_val += 1

if __name__ == '__main__':
  #m_list = [{"lower" : 99, "upper" : 101}, {"lower" : 99, "upper" : 101}, {"lower" : 19, "upper" : 21}]
  m_list = [{"lower_bound" : 99, "upper_bound" : 100}, {"lower_bound" : 19, "upper_bound" : 20}]
  r_list = []
  macro(m_list,r_list)
  print "r_list : ",r_list,"\n"
  t = T_setattr()
  print t.list
  #macro(m_list,t.list)
