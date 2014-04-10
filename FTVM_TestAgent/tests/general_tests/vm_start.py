from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_vm_start(parser):
	"""
	test vm start 
	"""
	#preprocess
	preprocess.preprocess(parser)
	#process
	process.vm_start(parser)
	#assert
	Assert.vm_running_in_hostOS(parser)
