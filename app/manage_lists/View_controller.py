import os


class View_controller():
	def __init__(self):
		self.dir_models = 'models/'
		self.dirList = []

	def create_user_list(self):
		self.dirList = [ item for item in os.listdir(self.dir_models) if os.path.isdir(os.path.join(self.dir_models, item)) ]
		return self.dirList

	def create_command_list(self, user_selected):
		default_commands = ['start', 'alt', 'left 1', 'left 2', 'left 3', 'right 1', 'right 2', 'right 3']
		path = self.dir_models + user_selected + '/'
		commands_list = []
		for root, dirs, files in os.walk(path):
			for file in files:
				if file.endswith('pmdl'):
					commands_list.append(file)
				
		return commands_list




		
		

