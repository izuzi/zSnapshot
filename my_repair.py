import re
import urlparse


def repair_data(url, html, remote_list):
	if not url:
		return html 
		
	if not html:
		return html

	if not remote_list:
		return html 
	
	html = _repair_data(url, html)
	
	for (k, v) in remote_list.items():
		html = html.replace(k, v, 100)
	
	return html
	
def _repair_data(url, html):
	hostname = get_hostname(url)
	path = get_path(url)
	
	html=html.decode('utf-8')
	
	pattern = re.compile(r'herf="//(.*?)"|herf=\'//(.*?)\'')
	html = re.sub(pattern, 'herf="http://\g<1>"', html)
	
	pattern = re.compile(r'src="//(.*?)"|src=\'//(.*?)\'')
	html = re.sub(pattern, 'src="http://\g<1>"', html)
	
	pattern = re.compile(r'herf="/(.*?)"|herf=\'/(.*?)\'')
	html = re.sub(pattern, 'herf="http://'+hostname+'/\g<1>"', html)
	
	pattern = re.compile(r'src="/(.*?)"|src=\'/(.*?)\'')
	html = re.sub(pattern, 'src="http://'+hostname+'/\g<1>"', html)
	
	pattern = re.compile(r'herf="./(.*?)"|herf=\'./(.*?)\'')
	html = re.sub(pattern, 'herf="http://'+path+'/\g<1>"', html)
	
	pattern = re.compile(r'src="./(.*?)"|src=\'./(.*?)\'')
	html = re.sub(pattern, 'src="http://'+path+'/\g<1>"', html)
	
	pattern = re.compile(r'herf="([^http://])(.*?)"|herf=\'([^http://])(.*?)\'')
	html = re.sub(pattern, 'herf="http://'+path+'/\g<1>\g<2>"', html)

	try:	
		pattern = re.compile(r'src="([^http://])(.*?)"|src=\'([^http://])(.*?)\'')
		html = re.sub(pattern, 'src="http://'+path+'/\g<1>\g<2>"', html)
	except Exception as e:
		print("#WARN: _repair_data error, %s, %s", url, str(e))

	return html
	
	
def get_hostname(url):
	url_p = urlparse.urlparse(url)
	hostname = url_p.hostname
	
	return hostname
	
def get_path(url):
	path = url.replace("http://", "").replace("https://", "")

	slash_pos = path.rfind("/")
	if slash_pos >= 0:
		path = path[0:slash_pos]
		
	return path
	
	
	
