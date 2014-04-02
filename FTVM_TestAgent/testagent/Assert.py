#/usr/bin/python
import time
import shell_server
import FTVM
import FTsystem
import mmsh
import TA_error


def vm_running_in_hostOS(parser):
	"""
	vm is running in hostOS or not

	cfg var: ast_vm_running_wait_time

	return True/raise exception
	"""
	if "ast_vm_running_wait_time" in parser.keys():
		time.sleep(int(parser["ast_vm_running_wait_time"]))
	if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"]):
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not running on hostOS" % parser["vm_name"])

def vm_shudown_in_hostOS(parser):
	"""
	vm is running in hostOS or not

	return True/raise exception
	"""
	if FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"]):
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not shutdown on hostOS" % parser["vm_name"])

def vm_running_in_backupOS(parser):
	"""
	vm is running in backupOS or not

	return True/False
	"""
	pass


def FTsystem_running_in_hostOS(parser):
	"""
	FTsystem is running in hostOS or not

	return True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"])
	if FTsystem.get_status(ssh) == "running":
		return True
	raise TA_error.Assert_Error("FTsystem is not running on hostOS")

def detect_fail(parser):
	"""
	FTsystem find fail or not

	return True/raise exception
	"""
	if mmsh.infofail(parser["vm_name"]) != "no fail":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no fail on hostOS" % parser["vm_name"])

def detect_no_fail(parser):
	"""
	FTsystem find no fail or not

	return True/raise exception
	"""
	if mmsh.infofail(parser["vm_name"]) == "no fail":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has fail on hostOS" % parser["vm_name"])

def detect_fail_vm_crash(parser):
	"""
	FTsystem find fail and fail is vm crash or not

	return True/raise exception
	"""
	if "ast_vm_crash_time" in parser.keys():
		time.sleep(int(parser["ast_vm_crash_time"]))
	if mmsh.infofail(parser["vm_name"]) == "vm crash":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has not detect vm crash on hostOS" % parser["vm_name"])

def detect_fail_os_crash(parser):
	"""
	FTsystem find fail and fail is vm crash or not

	return True/raise exception
	"""
	if mmsh.infofail(parser["vm_name"]) == "vm os crash":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has not detect vm os crash" % parser["vm_name"])

def do_recovery(parser):
	"""
	FTsystem do recovery or not

	return True/raise exception
	"""
	if mmsh.inforecover(parser["vm_name"]) != "no recover":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery" % parser["vm_name"])


def no_recovery(parser):
	"""
	FTsystem no recover or not

	return True/raise exception
	"""
	if mmsh.inforecover(parser["vm_name"]) == "no recover":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has recovery" % parser["vm_name"])

def recovery_vm_p_restart(parser):
	"""
	FTsystem recover vm process restart or not

	return True/raise exception
	"""
	if "ast_vm_p_restart_time" in parser.keys():
		time.sleep(int(parser["ast_vm_p_restart_time"]))
	if mmsh.inforecover(parser["vm_name"]) == "vm process restart":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery : vm process restart" % parser["vm_name"])

def recovery_vm_reboot(parser):
	"""
	FTsystem recover vm reboot or not

	return True/raise exception
	"""
	if mmsh.inforecover(parser["vm_name"]) == "vm reboot":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery : vm reboot" % parser["vm_name"])




if __name__ == '__main__':
	print mmsh.inforecover("VM1")