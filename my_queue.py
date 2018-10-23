from queue import Queue
import sys


q = Queue(100)

def put(data):
	return q.put(data)
	
def get():
	try:
		data = q.get_nowait()
		return data
	except Exception as e:
		return False