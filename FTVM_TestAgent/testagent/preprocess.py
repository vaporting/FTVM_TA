#!/usr/bin/python
import paramiko
import sys
import time
import cmd_service
import cmd_egrep
import shell_server
import FTsystem
import FTVM
import FTOS
import TA_error

def preprocess(parser):
  """
  when test case start, preprocess something
  param parser : is a dict, get from Test 
  """
  try:
    preprocess_hostOS(parser)
    #preprocess_backupOS(parser)
    #preprocess_vm(parser)
  except:
    pass


def preprocess_hostOS(parser):
  """
  preprocess HostOS
  """
  preprocess_hostOS_FTsystem(parser)
  preprocess_hostOS_vm(parser)

def preprocess_backupOS(parser):
  """
  preprocess backupOS
  """
  preprocess_backupOS_FTsystem(parser)
  

def preprocess_hostOS_FTsystem(parser):
  """
  preprocess HostOS FTsystem
  
  check FTsystem status 

  start/stop FTsystem

  raise exception if FTsystem can not start/stop
  """
  if parser["pre_check_hostOS_FTsystem"] == "yes":
    ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"])
    status = FTsystem.get_status(ssh)
    if status == "not running" and parser["pre_hostOS_FTsystem_start"] == "yes":
      FTsystem.start(ssh)
      time.sleep(float(parser["pre_hostOS_FTsystem_start_time"]))
      if FTsystem.get_status(ssh) == "not running":
        ssh.close()
        raise TA_error.Preprocess_Error("HostOS FTsystem can not start")
    if status == "running" and parser["pre_hostOS_FTsystem_start"] == "no":
      FTsystem.stop(ssh)
      time.sleep(float(parser["pre_hostOS_FTsystem_start_time"]))
      if FTsystem.get_status(ssh) == "running":
        ssh.close()
        raise TA_error.Preprocess_Error("HostOS FTsystem can not stop")
    ssh.close()


def preprocess_backupOS_FTsystem(parser):
  """
  preprocess backupOS FTsystem
  
  check FTsystem status 

  start/stop FTsystem

  raise exception if FTsystem can not start/stop
  """
  pass
  

def preprocess_hostOS_vm(parser):
  """
  preprocess hostOS vm
  """
  if parser["pre_check_hostOS_VM"] == "yes":
    if parser["pre_hostOS_VM_status"] == "running":
      preprocess_hostOS_vm_running(parser)
    elif parser["pre_hostOS_VM_status"] == "shut off":
      preprocess_hostOS_vm_shutdown(parser)
    elif parser["pre_hostOS_VM_status"] == "paused":
      pass


def preprocess_hostOS_vm_running(parser):
  """
  preprocess vm become running
  """
  if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
    prepocess_hostOS_vm_restart(parser)
    time.sleep(float(parser["pre_hostOS_VM_boot_time"]))
  elif FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"]):
    prepocess_hostOS_vm_start(parser)
    time.sleep(float(parser["pre_hostOS_VM_boot_time"]))
  if not FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
    raise TA_error.Preprocess_Error("HostOS %s can not start" % parser["vm_name"])

def prepocess_hostOS_vm_start(parser):
  """
  according to fault tolerant level, preprocess vm start
  """
  if parser["level"] == "0":
    FTVM.start(parser["vm_name"], parser["HostOS_ip"])
  else:
    FTVM.ftstart(parser["vm_name"], parser["HostOS_ip"], parser["level"])

def prepocess_hostOS_vm_restart(parser):
  """
  according to fault tolerant level, preprocess vm restart
  """
  if parser["level"] == "0":
    FTVM.restart(parser["vm_name"], parser["HostOS_ip"])
  else:
    FTVM.ftrestart(parser["vm_name"], parser["HostOS_ip"], parser["level"])

def preprocess_hostOS_vm_shutdown(parser):
  """
  preprocess vm become shutdown
  """
  if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
    FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"])
    time.sleep(float(parser["pre_hostOS_VM_shutdown_time"]))
  elif FTVM.is_paused(parser["vm_name"], parser["HostOS_ip"]):
    FTVM.resume(parser["vm_name"], parser["HostOS_ip"])
    FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"])
    time.sleep(float(parser["pre_hostOS_VM_shutdown_time"]))
  if not FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"]):
    raise TA_error.Preprocess_Error("HostOS %s can not shutdown" % parser["vm_name"])




if __name__ == '__main__':
  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect("140.115.53.42", username="ting", password="oolabting")
  #s_stdin, s_stdout, s_stderr = ssh.exec_command("service libvirt-bin status | egrep -oi '([0-9]+)$'")
  #print "output", s_stdout.read()
  s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo service libvirt-bin start")
  #print s_stdout.readlines()
  ssh.close()