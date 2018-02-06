from paramiko import client

class ssh:
	client = None

	def __init__(self, address, username, password, caller):
		try:
			self.client = client.SSHClient()
			# if server is not in the known_host file
			self.client.set_missing_host_key_policy(client.AutoAddPolicy())
			self.client.connect(address, username=username, password=password, look_for_keys = False)
			caller.startCar.setText('Stop')
			caller.startCar.setStyleSheet('background-color: #243427')
			caller.car_on = True
		except:
			caller.startCar.setText('Offline')
			caller.startCar.setStyleSheet('background-color: #571B24')

	def sendCommand(self, command):
		try:
			#print(client)
			stdin, stdout, stderr = self.client.exec_command(command)
			#print(client)
			#while not stdout.channel.exit_status_ready():
		except:
			print ("Connection not opened")


