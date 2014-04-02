#!/usr/bin/python

def kill_cmd(pid ,sig_no = "15"):
	"""
	kill [sig_no] [pid]
	"""
	return "kill -%s %s" % (sig_no, pid)