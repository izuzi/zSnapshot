from sinastorage.bucket import SCSBucket,ACL
import sinastorage
import sys
from urllib.parse import urlparse
import time
import datetime


class Uploader():
	def __init__(self, host, accesskey, secretkey, bucket_name, remote_dir):
		self.host = host
		self.bucket_name = bucket_name
		self.remote_dir = remote_dir
		
		sinastorage.setDefaultAppInfo(accesskey, secretkey)
		self.handler = SCSBucket(self.bucket_name)
		
	def do(self, url, filepath_list, is_file = True):
		remote_list = {}
		sub_dir = self.get_subdir(url)
		
		if filepath_list:
			for _url, filepath, filename in filepath_list:
				if not filepath:
					continue
				
				filename = filename if filename else str(time.time()) + ".html"
				print("#INFO: uploader ", filename, sub_dir)
				sys.stdout.flush()
			
				remote_link = self.upload_file(filepath, filename, sub_dir, is_file)
				remote_list[_url] = remote_link
				
		return remote_list
	
	@my_utils.time_limit(5)	
	def upload_file(self, local_path, local_name, sub_dir = "", is_file = True):
	
		if not local_path or not local_name:
			return ""
			
		if sub_dir:
			sub_dir = sub_dir + "/"
			
		remote_path = self.remote_dir + "/" + sub_dir + local_name
		
		ret = self._upload_file(remote_path, local_path, is_file)
		self.set_acl(remote_path)
		
		return ret
		
	def _upload_file(self, remote_path, local_path, is_file = True):
		if is_file:
			ret = self.handler.putFile(remote_path, local_path)
		else:
			ret = self.handler.put(remote_path, local_path)
		return self.host + "/" + self.bucket_name + "/" + remote_path if ret else ""
		
	def set_acl(self, remote_path):
		acl = {}
		acl[ACL.ACL_GROUP_ANONYMOUSE] = [ACL.ACL_READ]
		acl[ACL.ACL_GROUP_CANONICAL] = [ACL.ACL_READ_ACP,ACL.ACL_WRITE_ACP]

		self.handler.update_acl(remote_path, acl)
		
	def get_subdir(self, url):
		url_p = urlparse(url)
		return url_p.hostname.replace(".", "_")
		
		