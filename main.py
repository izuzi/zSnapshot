import os
import sys
import json
import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado import httpclient

import my_worker
import my_downloader
import my_uploader
import my_queue

class MainHandler(tornado.web.RequestHandler):

	@gen.coroutine
	def get(self):
		self.set_header('content-type', 'text/plain')
	
		url = self.get_argument('url')
		
		if not url:
			self.write("#ERROR! url is null.")
			return
			
		my_queue.put(url)
	
		self.write(str(my_queue.q.qsize()))


if __name__ == "__main__":
	worker = my_worker.Worker()
	worker.start()
	
	application = tornado.web.Application([
		(r"/", MainHandler),
	])

	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(5050 or os.environ['PORT'])
	tornado.ioloop.IOLoop.current().start()




	

