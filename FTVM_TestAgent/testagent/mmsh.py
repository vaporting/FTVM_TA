#!/usr/bin/python
import cmd_mmsh
import subprocess

def overview():
	"""
	execute mmsh overview
	"""
	cmd = cmd_mmsh.overview_cmd()
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def infofail(vm_name):
	"""
	execute mmsh infofail [vm_name]
	"""
	cmd = cmd_mmsh.infofail_cmd(vm_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def inforecover(vm_name):
	"""
	execute mmsh inforecover [vm_name]
	"""
	cmd = cmd_mmsh.inforecover_cmd(vm_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def infohost(vm_name, option):
	"""
	execute mmsh infohost [option] [vm_name]

	return host ip/host name
	"""
	cmd = cmd_mmsh.infohost_cmd(vm_name, option)
	host, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print host.rstrip()
	return host.rstrip()

def statehost(host_name):
	"""
	execute mmsh statehost [host_name]

	return running/initializing/shutdown
	"""
	cmd = cmd_mmsh.statehost_cmd(host_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def starthost(host_name):
	"""
	execute starthost [host_name]

	return success/[nothing]
	"""
	cmd = cmd_mmsh.starthost_cmd(host_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def stophost(host_name):
	"""
	execute stophost [host_name]

	return success/[nothing]
	"""
	cmd = cmd_mmsh.starthost_cmd(host_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def startwd(host_name):
	"""
	execute startwd [host_name]

	return success/[nothing]
	"""
	cmd = cmd_mmsh.startwd_cmd(host_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def stopwd(host_name):
		"""
	execute stopwd [host_name]

	return success/[nothing]
	"""
	cmd = cmd_mmsh.startwd_cmd(host_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def statewd(host_name):
		"""
	execute statewd [host_name]

	return start/stop
	"""
	cmd = cmd_mmsh.statewd_cmd(host_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def stateshmgr(shmgr_name):
		"""
	execute stateshmgr [shmgr_name]

	return start/stop
	"""
	cmd = cmd_mmsh.statewd_cmd(shmgr_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()

def stateipmc(ipmc_name):
	"""
	execute stateipmc [ipmc_name]

	return start/stop
	"""
	cmd = cmd_mmsh.statewd_cmd(ipmc_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()


def get_pid():
	"""
	get master monitor pid
	"""
	pid_file_path = data_dir.MM_PID_DIR+"master_monitord.pid"
	cmd = "sudo cat %s" % pid_file_path
	pid, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	if error == "":
		return int(pid)
	return False




