import my_config
import my_spider
import my_parser
import my_downloader
import my_uploader
import my_queue
import time
import threading
import sys
import urlparse
import my_repair


class Worker():
	def __init__(self):
	
		self.config = my_config.Config("config.txt")
		
		self.local_file_dir = self.config.get("BASE", "local_file_dir")
		self.sina_storage_host = self.config.get("BASE", "sina_storage_host")
		self.sina_storage_accesskey = self.config.get("BASE", "sina_storage_accesskey")
		self.sina_storage_secretkey = self.config.get("BASE", "sina_storage_secretkey")
		self.sina_storage_bucket_name = self.config.get("BASE", "sina_storage_bucket_name")
		self.sina_storage_bucket_dir = self.config.get("BASE", "sina_storage_bucket_dir")
	
		print("%s, %s, %s, %s, %s, %s" % (self.local_file_dir, self.sina_storage_host, self.sina_storage_accesskey, self.sina_storage_secretkey, self.sina_storage_bucket_name,self.sina_storage_bucket_dir))
		
		self.spider = my_spider.Spider()
		self.parser = my_parser.Parser()
		self.downloader = my_downloader.Downloader(self.local_file_dir)
		self.uploader = my_uploader.Uploader(self.sina_storage_host, self.sina_storage_accesskey, self.sina_storage_secretkey, self.sina_storage_bucket_name,self.sina_storage_bucket_dir)
	
	def start(self):
		for i in range(1):
			t = threading.Thread(target=self.do, args=(i,))
			t.start()
	
	def aciton(self, url):
		if not url:
			return False
			
		result = self.spider.go(url)
		if not result:
                        print "#ERROR: result is null, url is %s", url
                        return False
		if result.get('code') != 200 or result.get('error', ''):
			#print "#ERROR: url is %s, code is %d, error is %s" % (url, result.get('code', 0), result.get('error', '')
			print result.get('code', 0), result.get('error', '')
			return False
			
		print("#INFO: url is ", url)
			
		html = result.get('data')
		res_list = self.parser.getAllResourceList(html)
		
		print("#INFO: res_list is ", str(res_list))
		sys.stdout.flush()
		
		filepath_list = self.downloader.start(res_list)
		
		print("#INFO: filepath_list is ", str(filepath_list))
		sys.stdout.flush()
		
		if not filepath_list:
			return False
		
		remote_list = self.uploader.do(url, filepath_list)
		
		print("#INFO: remote_list is ", str(remote_list))
		sys.stdout.flush()
		
		html = my_repair.repair_data(url, html, remote_list)
		remote_html = self.uploader.do(url, [(url, html, "")], False)
		
		print("#INFO: remote_html is ", url, remote_html)
		sys.stdout.flush()
		
		return url, remote_html
		
	
	def do(self, i):

		while True:

			data = my_queue.get()

			if data == False:
				#print("#INFO: thread %s, queue is empty" % i)
				#sys.stdout.flush()
				time.sleep(1)
				continue
			print("#INFO: data, %s" % data)		
	
			self.aciton(data)
			sys.stdout.flush()


			
		
		
		
			
