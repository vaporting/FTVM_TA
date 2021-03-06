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
import mmsh
import TA_error

def preprocess(parser):
  """
  when test case start, preprocess something
  param parser : is a dict, get from Test 
  """
  try:
    preprocess_hostOS(parser)
    #preprocess_backupOS(parser)
  except:
    pass


def preprocess_hostOS(parser):
  """
  preprocess HostOS
  """
  #preprocess_hostOS_hw(parser)
  #preprocess_hostOS_OS(parser)
  #preprocess_hostOS_wd(parser)
  preprocess_hostOS_FTsystem(parser)
  preprocess_hostOS_vm(parser)

def preprocess_backupOS(parser):
  """
  preprocess backupOS
  """
  #preprocess_backupOS_OS(parser)
  #preprocess_backupOS_FTsystem(parser)
  #preprocess_backupOS_vm(parser)

def preprocess_hostOS_hw(parser):
  """
  perprocess hostOS hardware part
  """
  if parser["pre_check_hostOS_hw"] == "yes":
    if mmsh.stateshmgr(parser["HostOS_shmgr_name"]) == "stop":
      raise TA_error.Preprocess_Error("HostOS hw shmgr stop")
    if mmsh.stateipmc(parser["HostOS_ipmc_name"]) == "stop":
      raise TA_error.Preprocess_Error("HostOS hw ipmc stop")

def preprocess_hostOS_OS(parser):
  """
  preprocess hostOS OS
  """
  if parser["pre_check_FT_hostOS"] == "yes":
    if parser["pre_FT_hostOS_status"] == "running":
      preprocess_hostOS_OS_boot(parser)
    elif parser["pre_FT_hostOS_status"] == "shutdown":
      preprocess_hostOS_OS_shutdown(parser)

def preprocess_hostOS_OS_boot(parser):
  """
  preprocess hostOS OS boot
  """
  if not FTOS.is_running(parser["HostOS_name"]):
    if FTOS.is_shutdown(parser["HostOS_name"]):
      status = FTOS.boot(parser["HostOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("HostOS OS boot command fail")
    time.sleep(float(parser["pre_hostOS_boot_time"]))
    if not FTOS.is_running(parser["HostOS_name"]):
      raise TA_error.Preprocess_Error("HostOS OS can not boot")
  

def preprocess_hostOS_OS_shutdown(parser):
  """
  preprocess hostOS OS shutdown
  """
  if not FTOS.is_shutdown(parser["HostOS_name"]):
    if FTOS.is_running(parser["HostOS_name"]):
      status = FTOS.shutdown(parser["HostOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("HostOS OS shutdown command fail")
    time.sleep(float(parser["pre_hostOS_shutdown_time"]))
    if not FTOS.is_shutdown(parser["HostOS_name"]):
      raise TA_error.Preprocess_Error("HostOS OS can not shutdown")

def preprocess_backupOS_OS(parser):
  """
  preprocess backupOS OS
  """
  if parser["pre_check_FT_hostOS"] == "yes":
    if parser["pre_FT_hostOS_status"] == "running":
      preprocess_hostOS_OS_boot(parser)
    elif parser["pre_FT_hostOS_status"] == "shutdown":
      pass

def preprocess_backupOS_OS_boot(parser):
  """
  preprocess backupOS OS boot
  """
  if not FTOS.is_running(parser["BackupOS_name"]):
    if FTOS.is_shutdown(parser["BackupOS_name"]):
      status = FTOS.boot(parser["BackupOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("BackupOS OS boot command fail")
    time.sleep(float(parser["pre_backupOS_boot_time"]))
    if not FTOS.is_running(parser["BackupOS_name"]):
      raise TA_error.Preprocess_Error("BackupOS OS can not boot")

def preprocess_hostOS_wd(parser):
  """
  preprocess watchdog for fault tolerant hardware part
  """
  if parser["pre_check_hostOS_hw"] == "yes":
    if mmsh.statewd(parser["HostOS_name"]) == "stop":
      status = mmsh.startwd(parser["HostOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("HostOS watchdog process can not start")
  

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
  if parser["pre_check_backupOS_FTsystem"] == "yes":
    ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"])
    status = FTsystem.get_status(ssh)
    if status == "not running" and parser["pre_backupOS_FTsystem_start"] == "yes":
      FTsystem.start(ssh)
      time.sleep(float(parser["pre_backupOS_FTsystem_start_time"]))
      if FTsystem.get_status(ssh) == "not running":
        ssh.close()
        raise TA_error.Preprocess_Error("backupOS FTsystem can not start")
    if status == "running" and parser["pre_backupOS_FTsystem_start"] == "no":
      FTsystem.stop(ssh)
      time.sleep(float(parser["pre_backupOS_FTsystem_start_time"]))
      if FTsystem.get_status(ssh) == "running":
        ssh.close()
        raise TA_error.Preprocess_Error("backupOS FTsystem can not stop")
    ssh.close()
  

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
  preprocess hostOS vm become shutdown
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

def preprocess_backupOS_vm(parser):
  """
  preprocess backupOS vm
  """
  if parser["pre_check_backupOS_VM"] == "yes":
    if parser["pre_backupOS_VM_status"] == "running":
      pass
      #preprocess_backupOS_vm_running(parser)
    elif parser["pre_backupOS_VM_status"] == "shut off":
      preprocess_backupOS_vm_shutdown(parser)
    elif parser["pre_backupOS_VM_status"] == "paused":
      pass

def preprocess_backupOS_vm_shutdown(parser):
  """
  preprocess backupOS vm become shutdown
  """
  if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"]):
    FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"])
    time.sleep(float(parser["pre_backupOS_VM_shutdown_time"]))
  elif FTVM.is_paused(parser["vm_name"], parser["BackupOS_ip"]):
    FTVM.resume(parser["vm_name"], parser["BackupOS_ip"])
    FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"])
    time.sleep(float(parser["pre_backupOS_VM_shutdown_time"]))
  if not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"]):
    raise TA_error.Preprocess_Error("backupOS %s can not shutdown" % parser["vm_name"])




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