#/usr/bin/python
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
import mmsh

def postprocess(parser):
	"""
	when testing done, postprocess something
	param parser : is a dict, get from Test 
	"""
	postprocess_hostOS(parser)

def postprocess_hostOS(parser):
	"""
	postprocess hostOS
	"""
	#postprocess_hostOS_OS(parser)
	postprocess_hostOS_FTsystem(parser)
	postprocess_hostOS_vm(parser)
	
def postprocess_backupOS(parser):
	"""
	postprocess backupOS
	"""
	postprocess_backupOS_vm(parser)

def postprocess_hostOS_OS(parser):
	"""
	postprocess hostOS OS
	"""
	if parser["pos_hostOS_shutdown"] == "yes":
		if mmsh.statehost(parser["HostOS_name"]) != "shutdown":
			mmsh.stophost(parser["HostOS_name"])
			time.sleep(float(parser["pos_hostOS_shutdown_time"]))
	if mmsh.statehost(parser["HostOS_name"]) != "shutdown":
		raise TA_error.Postprocess_Error("HostOS can not shutdown")


def postprocess_hostOS_FTsystem(parser):
	"""
	postprocess HostOS FTsystem

	check FTsystem status 

	start/stop FTsystem

	raise exception if FTsystem can not start/stop
	"""
	if parser["pos_check_hostOS_FTsystem"] == "yes":
		ssh = shell_server.get_ssh(parser["HostOS_ip"]
															, parser["HostOS_usr"]
															, parser["HostOS_pwd"])
	status = FTsystem.get_status(ssh)
	if status == "not running" and parser["pos_hostOS_FTsystem_start"] == "yes":
		FTsystem.start(ssh)
		time.sleep(float(parser["pos_hostOS_FTsystem_start_time"]))
		if FTsystem.get_status(ssh) == "not running":
			ssh.close()
			raise TA_error.Postprocess_Error("HostOS FTsystem can not start")
	if status == "running" and parser["pos_hostOS_FTsystem_start"] == "no":
		FTsystem.stop(ssh)
		time.sleep(float(parser["pos_hostOS_FTsystem_start_time"]))
		if FTsystem.get_status(ssh) == "running":
			ssh.close()
			raise TA_error.Postprocess_Error("HostOS FTsystem can not stop")
	ssh.close()


def postprocess_hostOS_vm(parser):
	"""
	postprocess hostOS vm
	"""
	if parser["pos_check_hostOS_VM"] == "yes":
		if parser["pos_hostOS_VM_status"] == "running":
			postprocess_hostOS_vm_running(parser)
		elif parser["pos_hostOS_VM_status"] == "shut off":
			postprocess_hostOS_vm_shutdown(parser)
		elif parser["pos_hostOS_VM_status"] == "paused":
			pass

def postprocess_hostOS_vm_running(parser):
	"""
	postrocess vm become running
	"""
	if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
		FTVM.restart(parser["vm_name"], parser["HostOS_ip"])
	elif FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"]):
		FTVM.start(parser["vm_name"], parser["HostOS_ip"])
	time.sleep(float(parser["pos_hostOS_VM_boot_time"]))
	if not FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
		raise TA_error.Postprocess_Error("HostOS %s can not start" % parser["vm_name"])

def postprocess_hostOS_vm_shutdown(parser):
	"""
	postprocess vm become shutdown
	"""
	if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
		FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"])
	elif FTVM.is_paused(parser["vm_name"], parser["HostOS_ip"]):
		FTVM.resume(parser["vm_name"], parser["HostOS_ip"])
		FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"])
	time.sleep(float(parser["pos_hostOS_VM_shutdown_time"]))
	#print FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"])
	if not FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"]):
		raise TA_error.Postprocess_Error("HostOS %s can not shutdown" % parser["vm_name"])

def postprocess_backupOS_vm(parser):
	"""
	postprocess backupOS vm
	"""
	if parser["pos_check_backupOS_VM"] == "yes":
		if parser["pos_backupOS_VM_status"] == "running":
			#postprocess_backupOS_vm_running(parser)
			pass
		elif parser["pos_backupOS_VM_status"] == "shut off":
			postprocess_backupOS_vm_shutdown(parser)
		elif parser["pos_backupOS_VM_status"] == "paused":
			pass

def postprocess_backupOS_vm_shutdown(parser):
	"""
	postprocess backupOS vm shutdown
	"""
	if FTVM.is_running(parser["vm_name"], parser["backupOS_ip"]):
		FTVM.shutdown(parser["vm_name"], parser["backupOS_ip"])
	elif FTVM.is_paused(parser["vm_name"], parser["backupOS_ip"]):
		FTVM.resume(parser["vm_name"], parser["backupOS_ip"])
		FTVM.shutdown(parser["vm_name"], parser["backupOS_ip"])
	time.sleep(float(parser["pos_backupOS_VM_shutdown_time"]))
	if not FTVM.is_shutoff(parser["vm_name"], parser["backupOS_ip"]):
		raise TA_error.Postprocess_Error("backupOS %s can not shutdown" % parser["vm_name"])