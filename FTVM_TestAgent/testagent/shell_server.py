#!/usr/bin/python
import paramiko
import socket
import TA_error


def get_ssh(ip, usr, pwd, t_out=5):
	"""
	return a ssh object
	"""
	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, username=usr, password=pwd,timeout=t_out)
		return ssh
	except paramiko.BadHostKeyException, e:
		print str(e)
		raise TA_error.Shell_server_Error(str(e))
	except paramiko.AuthenticationException, e:
		print str(e)
		raise TA_error.Shell_server_Error(str(e))
	except paramiko.SSHException, e:
		print str(e)
		raise TA_error.Shell_server_Error(str(e))
	except (socket.error, socket.timeout) as e:
		print "socket except : "+str(e)
		raise TA_error.Shell_server_Error(str(e))

