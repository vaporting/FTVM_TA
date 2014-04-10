from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_guestOS_crash(parser):
	"""
	test level 1 fault tolerant VM crash
	"""
	preprocess.preprocess(parser)
	process.exec_L1_vm_crasher(parser)
	Assert.vm_running_in_hostOS(parser)
	Assert.detect_fail_vm_crash(parser)
	Assert.recovery_vm_reboot(parser)