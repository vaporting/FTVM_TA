#!/usr/bin/python
import paramiko
import cmd_service
import cmd_egrep

def get_status(ssh):
	"""
	get FTsystem status
	return running/not running
	"""
	cmd = cmd_egrep.extract_pid_cmd(cmd_service.status_cmd("libvirt-bin"))
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
	if s_stdout.read() == "":
		return "not running"
	return "running"

def start(ssh):
	"""
	start FTsystem
	"""
	cmd = cmd_service.start_cmd("libvirt-bin")
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	print s_stdout.read()

def stop(ssh):
	"""
	stop FTsystem
	"""
	cmd = cmd_service.stop_cmd("libvirt-bin")
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	print s_stdout.read()
