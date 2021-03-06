from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_ft_vm_crash(parser):
	"""
	test level 1 fault tolerant VM crash
	"""
	preprocess.preprocess(parser)
	process.kill_vm_process(parser)
	Assert.vm_running_in_hostOS(parser)
	Assert.detect_fail_vm_crash(parser)
	Assert.recovery_vm_p_restart(parser)
