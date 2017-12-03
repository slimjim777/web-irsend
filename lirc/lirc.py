from subprocess import call
import re

class Lirc:
	"""
	Parses the lircd.conf file and can send remote commands through irsend.
	"""
	codes = {}

	def __init__(self, conf):
		# Open the config file
		self.conf = open(conf, 'r')

		# Parse the config file
		self.parse()
		self.conf.close()


	@property
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

		for l in self.conf:
			# Convert (multiple) tabs to spaces
			l = re.sub(r'[ \t]+', ' ', l)
			# Remove comments
			l = re.sub(r'#.*', '', l)
			# Remove surrounding whitespaces
			l = l.strip()

			# Look for a 'begin remote' line
			if l == 'begin remote':
				# Got the start of a remote definition
				remote_name = None
				code_section = False

			elif not remote_name and l.startswith('name '):
				# Got the name of the remote
				remote_name = l.split(' ')[1]
				if remote_name not in self.codes:
					self.codes[remote_name] = set()

			elif remote_name and l == 'end remote':
				# Got to the end of a remote definition
				remote_name = None

			elif remote_name and (l == 'begin codes' or l == 'begin raw_codes'):
				code_section = True

			elif remote_name and (l == 'end codes' or l == 'end raw_codes'):
				code_section = False

			elif remote_name and code_section and l.startswith('name '):
				fields = l.split(' ')
				self.codes[remote_name].add(fields[1])


	def send_once(self, device_id, message):
		"""
		Send single call to IR LED.
		"""
		call(['irsend', 'SEND_ONCE', device_id, message])


if __name__ == "__main__":
	lirc = Lirc('/etc/lirc/lircd.conf')
