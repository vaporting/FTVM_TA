

def run_L1_hostOS_crash(parser):
	#preprocess
	preprocess.preprocess(parser)
	#process
	process.exec_crasher(parser)
	#assert
	Assert.detect_hostOS_crash(parser)
	Assert.do_recovery(parser)
	Assert.is_running_on_backup(parser)
	#postprocess
	postprocess.postprocess(parser)