#!/usr/bin/python
import subprocess


def command(string):
	"""
	return egrep command
	"""
	cmd = "egrep %s" % string
	return cmd

def extract_pid_cmd(cmd):
	"""
	extract pid by egrep
	"""
	grep_cmd = command("-oi '([0-9]+)$'") 
	"""
	origin cmd :grep -oi '([0-9]+)$'
	if you want use subprocess.Popen to run cmd you must to change '([0-9]+)$' to ([0-9]+)$
	"""
	new_cmd = "%s | %s" % (cmd, grep_cmd)
	return new_cmd



if __name__ == '__main__':
	cmd = extract_pid_cmd("service libvirt-bin status")
	print cmd
	output, error = subprocess.Popen("service libvirt-bin status".split(), stdout=subprocess.PIPE).communicate()
	print output
	#output = subprocess.check_output("service libvirt-bin status | egrep -oi '([0-9]+)$'", shell=True, stderr=subprocess.STDOUT,)
	#print "output: "+output
	p1 = subprocess.Popen("service libvirt-bin status".split(), stdout=subprocess.PIPE)
	#p2 = subprocess.Popen(["egrep","-oi", "([0-9]+)$"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p2 = subprocess.Popen("egrep -oi ([0-9]+)$".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	print p2.communicate()[0].rstrip()
	

