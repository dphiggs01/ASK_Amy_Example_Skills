import time
import logging

logger = logging.getLogger()

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logger.debug("***** function {} took {:5.4f} ms".format(f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

