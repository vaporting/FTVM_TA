#!/usr/bin/python


def command(string):
	"""
	return service command
	"""
	cmd = "service %s" % string
	return cmd


def status_cmd(ser_name):
	"""
	service [ser_name] status
	"""
	return command("%s status" % ser_name)

def start_cmd(ser_name):
	"""
	service [ser_name] start
	"""
	return command("%s start" % ser_name)

def stop_cmd(ser_name):
	"""
	service [ser_name] stop
	"""
	return command("%s stop" % ser_name)



if __name__ == '__main__':
	print status_cmd("libvirt-bin")