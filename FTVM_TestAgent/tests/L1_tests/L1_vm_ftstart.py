from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_vm_ftstart(parser):
	"""
	test vm start 
	"""
	#preprocess
	preprocess.preprocess(parser)
	#process
	process.vm_start(parser)
	#assert
	Assert.vm_running_in_hostOS(parser)
	#postprocess
	postprocess.postprocess(parser)