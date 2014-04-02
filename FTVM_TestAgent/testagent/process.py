#/usr/bin/python
import data_dir
import FTsystem
import FTVM
import cmd_kill
import shell_server

def exec_L1_hostOS_crasher(parser):
	"""
	execute level 1 crasher in hostOS
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"])
	f_path = parser["HostOS_process_dir"]+"L1_crasher"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close()

def kill_vm_process(parser):
	"""
	kill vm process on hostOS
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"])
	pid = FTVM.get_pid(parser["vm_name"], parser["HostOS_ip"], ssh)
	cmd = cmd_kill.kill_cmd(pid, 9)
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close()
	

def exec_L1_vm_crasher(parser):
	"""
	execute level 1 crasher in vm 
	"""
	pass

def vm_start(parser):
	"""
	normaly start vm
	"""
	FTVM.start(parser["vm_name"], parser["HostOS_ip"])

def vm_ftstart(parser):
	"""
	ftstart vm
	"""
	FTVM.ftstart(parser["vm_name"], parser["HostOS_ip"], parser["level"])



