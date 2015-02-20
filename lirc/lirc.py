from subprocess import call
import re

class Lirc:
	"""
	Parses the lircd.conf file and can send remote commands through irsend.
	"""
	codes = {}
	
	def __init__(self, conf):
		# Open the config file
		self.conf = open(conf, "rb")
		
		# Parse the config file
		self.parse()
		self.conf.close()
		

	def devices(self):
		"""
		Return a list of devices.
		"""
		return self.codes.keys()
	
	
	def parse(self):
		"""
		Parse the lircd.conf config file and create a dictionary.
		"""
		remote_name = None
		code_section = False
		
		for line in self.conf:
			# Convert tabs to spaces
			l = line.replace('\t',' ')

			# Skip comments
			if re.match('^\s*#',line):
				continue
			
			# Look for a 'begin remote' line
			if l.strip()=='begin remote':
				# Got the start of a remote definition
				remote_name = None
				code_section = False
					
			elif not remote_name and l.strip().find('name')>-1:
				# Got the name of the remote
				remote_name = l.strip().split(' ')[-1]
				if remote_name not in self.codes:
					self.codes[remote_name] = {}
				
			elif remote_name and l.strip()=='end remote':
				# Got to the end of a remote definition
				remote_name = None
				
			elif remote_name and l.strip()=='begin codes':
				code_section = True

			elif remote_name and l.strip()=='end codes':
				code_section = False
				
			elif remote_name and code_section:
				# Got a code key/value pair... probably
				fields = l.strip().split(' ')
				self.codes[remote_name][fields[0]] = fields[-1]

			
	def send_once(self, device_id, message):
		"""
		Send single call to IR LED.
		"""
		call(['irsend', 'SEND_ONCE', device_id, message])

				
if __name__ == "__main__":
	lirc = Lirc('/etc/lirc/lircd.conf')
	
	
