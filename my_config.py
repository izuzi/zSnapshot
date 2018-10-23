import configparser


class Config():
	def __init__(self, conf_path):
		self.conf = configparser.ConfigParser()
		self.conf.read(conf_path)
		
	def get(self, section, key):
		return self.conf.get(section, key)
