from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_hostOS_crash(parser):
	#preprocess
	preprocess.preprocess(parser)
	#process
	process.exec_crasher(parser)
	#assert
	Assert.detect_hostOS_crash(parser)
	Assert.do_recovery(parser)
	Assert.is_running_on_backup(parser)