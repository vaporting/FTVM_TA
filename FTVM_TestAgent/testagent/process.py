#/usr/bin/python
import data_dir
import FTsystem
import FTVM
import cmd_kill
import shell_server
import mmsh

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

def kill_libvirt_process(parser):
	"""
	kill libvirt process on hostOS
	"""
	ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"])
	pid = FTsystem.get_pid(ssh)
	cmd = cmd_kill.kill_cmd(pid, 9)
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close()
	
def kill_master_monitor_process(parser):
	"""
	kill master monitor process on hostOS
	"""
	pid = mmsh.get_pid()
	cmd = cmd_kill.kill_cmd(pid, 9)
	subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()

def exec_L1_vm_crasher(parser):
	"""
	execute level 1 crasher in vm 
	"""
	ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"])
	cmd = data_dir.OS_PROCESS_DIR+"L1_crasher"
	print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close()

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

def vm_shutdown(parser):
	"""
	shutdown vm
	"""
	FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"])



