import json
import urllib2
import my_utils


class Spider():
	def __init__(self):
		self.http_header   = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
							}

	@my_utils.time_limit(5)	
	def go(self, url):
		error = {}
		result = {}
		request = urllib2.Request(url, headers=self.http_header)
		response = None
		try:
			response = urllib2.urlopen(request, timeout=3)
			
			result['data'] = response.read()
			result['code'] = response.getcode()
			result['info'] = response.info()
			
			return result
		except Exception as e:
			if hasattr(e, 'code'):
				print('Error code:', e.code)
				error['code'] = e.code
			elif hasattr(e, 'reason'):
				print('Reason:', e.reason)
				error['reason'] = e.reason
		finally:
			if response:
				response.close()
				
			if error:
				result["error"] = str(error)
			return result
