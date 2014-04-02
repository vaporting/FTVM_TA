from testagent import preprocess
from testagent import postprocess



def run_L1_preprocess_test(parser):
	#print parser
	preprocess.preprocess(parser)
	#print "after preprocess"
	postprocess.postprocess(parser)