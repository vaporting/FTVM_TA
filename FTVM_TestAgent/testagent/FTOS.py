#!/usr/bin/python
import subprocess
import time
import data_dir
import shell_server
import mmsh

def get_OS_status(OS_name):
	"""
	get OS status

	status : running / shutdown / initializing
	"""
	return mmsh.statehost(OS_name).rstrip()

def is_running(OS_name):
	"""
	return True (if OS is running)/False (if OS isn't running)
	"""
	if get_OS_status(OS_name) == "running":
		return True
	return False

def is_shutdown(OS_name):
	"""
	return True (if OS is shutdown)/False (if OS isn't shutdown)
	"""
	if get_OS_status(OS_name) == "shutdown":
		return True
	return False

def boot(OS_name):
	"""
	boot OS

	return success / [nothing]
	"""
	return mmsh.starthost(OS_name)

def shutdown(OS_name):
	"""
	shutdown OS

	return success / [nothing]
	"""
	return mmsh.stophost(OS_name)

