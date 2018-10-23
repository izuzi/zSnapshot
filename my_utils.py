#coding=utf-8 
import functools
import sys
import threading
import time


class KThread(threading.Thread):
	def __init__(self, *args, **kwargs):
		threading.Thread.__init__(self, *args, **kwargs)
		self.killed = False

	def start(self):
		"""Start the thread."""
		self.__run_backup = self.run
		self.run = self.__run	  # Force the Thread to install our trace.
		threading.Thread.start(self)

	def __run(self):
		"""Hacked run function, which installs the
		trace."""
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, why, arg):
		if why == 'call':
		  return self.localtrace
		else:
		  return None

	def localtrace(self, frame, why, arg):
		if self.killed:
			if why == 'line':
				raise SystemExit()
		return self.localtrace

	def kill(self):
		self.killed = True


class TimeOutException(Exception):  
	pass
	
def time_limit(timeout):
	def decorator(func):
		def to_do(func, args, kwargs, result):
			result.append(func(*args, **kwargs))
		
		@functools.wraps(func)
		def wapper(*args, **kwargs):
			result = []
			_kwargs = {
				'func': func,
				'args': args,
				'kwargs': kwargs,
				'result': result
			}

			t = KThread(target=to_do, args=(), kwargs=_kwargs)
			t.start()
			t.join(timeout)

			if t.isAlive():
				t.kill()
				emsg="function(%s) execute timeout after %d second" % (func.__name__, timeout)
				raise TimeOutException(emsg)
			else:
				return result[0]

		return wapper
	return decorator