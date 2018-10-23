import my_spider
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import sys


class Downloader():

	def __init__(self, filedir):
		self.filedir = filedir
		self.spider = my_spider.Spider()
	
	def start(self, url_list):
		if not url_list:
			return False
	
		filename_list = []

		if not url_list:
			return False
	
		filename_list = []
	
		for url in url_list:
			data = self.action(url)
			filename_list.append(data)
		
		return filename_list

		
		
	def action(self, url):
	
		rsp = self.spider.go(url)
		if not rsp:
			return url, "", ""
			
		if not isinstance(rsp, (dict)) or rsp.get('error') or rsp.get('code') != 200:
			return url, "", ""
			
		content = rsp.get('data')
		filename = self.get_filename(url)
		
		filepath = self.save_file(filename, content)
		if not filepath:
			return url, "", ""
			
		print("#INFO: save_file, ", url, filename)
		sys.stdout.flush()
		return url, filepath, filename
	
	
	def get_filename(self, url):
		if not url:
			return False
		
		question_pos = url.find("?")
		if question_pos >= 0:
			url = url[0:question_pos]
			
		slash_pos = url.rfind("/")
		if slash_pos >= 0:
			url = url[slash_pos+1:]
			
		return url;
	
	
	def get_filesuffix(self, get_filename):
		if not get_filename:
			return False
			
		dot_pos = get_filename.find(".")
		if dot_pos == -1:
			return False
	
		return get_filename[dot_pos+1:]
		
		
	def save_file(self, filename, content):
		if not filename or not content:
			return False
	
		filesuffix = self.get_filesuffix(filename)
		if not filesuffix:
			return False
		
		is_bin = filesuffix == 'jpg' or filesuffix == 'jpeg' or filesuffix == 'gif' or filesuffix == 'png' or filesuffix == 'webp' or filesuffix == 'ico'
		filepath = self.filedir + filename
	
		try:
			type = 'wb' #if is_bin else 'w'

			with open(filepath, type) as f:
				f.write(content)
		except Exception as e:
			print("#ERROR! save_file.", filename, filesuffix, e)
			return False
		return filepath

	