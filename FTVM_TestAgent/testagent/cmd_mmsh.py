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

def infohost_cmd(vm_name):
	"""
	mmsh infohost [vm_name]
	"""
	return command("infohost %s" % vm_name)

