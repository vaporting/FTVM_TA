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

def infohost(vm_name):
	"""
	execute mmsh infohost [vm_name]
	"""
	cmd = cmd_mmsh.infohost_cmd(vm_name)
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip()




