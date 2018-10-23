from bs4 import BeautifulSoup

class Parser():

	def getAllResourceList(self, html):
		res_list = []
		image_list = self.getImageList(html)
		css_list = self.getCssList(html)
		js_list = self.getJsList(html)
		
		res_list.extend(image_list)
		res_list.extend(css_list)
		res_list.extend(js_list)
		
		return res_list
		

	def getImageList(self, html):
		if not html:
			return []
			
		soup = BeautifulSoup(html, 'html.parser')
		tags = soup.find_all('img')
		urls = []
		for img in tags:
			if 'data-src' in str(img):
				urls.append(img['data-src'])
			else:
				urls.append(img['src'])
		
		return urls
		
	def getCssList(self, html):
		if not html:
			return []
			
		soup = BeautifulSoup(html, 'html.parser')
		tags = soup.find_all('link')
		urls = []
		for css in tags:
			urls.append(css['href'])
		
		return urls
		
	def getJsList(self, html):
		if not html:
			return []
			
		soup = BeautifulSoup(html, 'html.parser')
		tags = soup.find_all('script')
		urls = []
		for js in tags:
			src = js.get('src', None)
			if src:
				urls.append(src)
		
		return urls