#!/usr/bin/python

def command(string):
	"""
	return mmsh command
	"""
	cmd = "mmsh %s" % string
	return cmd

def overview_cmd():
	"""
	mmsh overview
	"""
	return command("overview")

def infofail_cmd(vm_name):
	"""
	mmsh infofail [vm_name] 
	"""
	return command("infofail %s" % vm_name)

def inforecover_cmd(vm_name):
	"""
	mmsh inforecover [vm_name]
	"""
	return command("inforecover %s" % vm_name)

def infohost_cmd(vm_name, option):
	"""
	option: i/n

	mmsh infohost [option] [vm_name]
	"""
	return command("infohost -%s %s" % (option, vm_name))

def statehost_cmd(host_name):
	"""
	mmsh statehost [host_name]
	"""
	return command("statehost %s" % host_name)

def starthost_cmd(host_name):
	"""
	mmsh starthost [host_name]
	"""
	return command("starthost %s" % host_name)

def stophost_cmd(host_name):
	"""
	mmsh stophost [host_name]
	"""
	return command("stophost %s" % host_name)

def startwd_cmd(host_name):
	"""
	mmsh startwd [host_name]
	"""
	return command("startwd %s" % host_name)

def stopwd_cmd(host_name):
	"""
	mmsh stopwd [host_name]
	"""
	return command("stopwd %s" % host_name)

def statewd_cmd(host_name):
	"""
	mmsh statewd [host_name]
	"""
	return command("statewd %s" % host_name)

def stateshmgr_cmd(shmgr_name):
	"""
	mmsh stateshmgr [shmgr_name]
	"""
	return command("shmgr_name %s" % shmgr_name)

def stateipmc_cmd(host_name):
	"""
	mmsh stateipmc [host_name]
	"""
	return command("stateipmc %s" % host_name)
