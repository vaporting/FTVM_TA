#!/usr/bin/python
import subprocess
import time
import data_dir
import shell_server
import cmd_virsh

def get_vm_status(vm_name, ip=""):
	"""
	check vm check vm status 
	return status (running/paused/shut off)
	"""
	cmd = cmd_virsh.domstate_cmd(vm_name, ip)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	#print status.rstrip()
	#print "error :",error
	return status.rstrip()

def is_running(vm_name, ip=""):
	if get_vm_status(vm_name, ip) == "running":
		return True
	return False

def is_shutoff(vm_name, ip=""):
	if get_vm_status(vm_name, ip) == "shut off":
		return True
	return False

def is_paused(vm_name, ip=""):
	if get_vm_status(vm_name, ip) == "paused":
		return True
	return False

def start(vm_name, ip=""):
	"""
	start vm, when vm status is shutoff 
	"""
	if is_shutoff(vm_name, ip):
		cmd = cmd_virsh.start_cmd(vm_name, ip)
		subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()

def ftstart(vm_name, ip="", level="1"):
	"""
	ftstart vm, when vm status is shutoff
	"""
	if is_shutoff(vm_name, ip):
		cmd = cmd_virsh.ftstart_cmd(vm_name, ip, level)
		subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()

def shutdown(vm_name, ip=""):
	"""
	shutdown vm, when vm status is running
	"""
	if is_running(vm_name, ip):
		cmd = cmd_virsh.shutdown_cmd(vm_name, ip)
		#print "cmd : "+cmd
		subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()

def resume(vm_name, ip=""):
	"""
	resume vm, when vm status is paused
	"""
	if is_paused(vm_name, ip):
		cmd = cmd_virsh.paused_cmd(vm_name, ip)
		subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()

def restart(vm_name, ip=""):
	"""
	restart vm
	"""
	shutdown(vm_name, ip)
	t_begin = time.time()
	while time.time() < (t_begin+70):
		time.sleep(1)
		if is_shutoff(vm_name, ip) == True:
			time.sleep(1)
			start(vm_name, ip)
			break

def ftrestart(vm_name, ip="", level="1"):
	"""
	ftrestart vm
	"""
	shutdown(vm_name, ip)
	t_begin = time.time()
	while time.time() < (t_begin+70):
		time.sleep(1)
		if is_shutoff(vm_name, ip) == True:
			time.sleep(1)
			ftstart(vm_name, ip, level)
			break

def get_pid(vm_name, ip, ssh):
	"""
	get vm process id in OS
	"""
	pid_file_path = data_dir.VM_PID_DIR+vm_name+".pid"
	cmd = "sudo cat %s" % pid_file_path
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
	pid = s_stdout.read()
	if pid != "":
		return int(pid)
	return False

	




if __name__ == '__main__':
	"""
	if get_vm_status("VM1", "140.115.53.42") != "running":
		start("VM1", "140.115.53.42")
	get_vm_status("VM1", "140.115.53.42")
	"""
	#print "start"
	#if get_vm_status("VM1", "140.115.53.42") == "running":
		#print "in"
	#get_vm_status("VM1", "140.115.53.42")
	#print is_shutoff("VM1", "140.115.53.42")
	#restart("VM1", "140.115.53.42")
	#shutdown("VM1", "140.115.53.42")
	ssh = shell_server.get_ssh("140.115.53.42", "ting", "oolabting")
	print get_pid("VM1", "140.115.53.42", ssh)
