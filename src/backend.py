#!/usr/bin/env python3

import os
import datetime
import xdg
import threading
from datetime import datetime


class app():

	def checkValidConfig():
		try:
			if os.path.exists(app.readConfig('Location of Tickets')):
				return
			else:
				app.setConfig('Location of Tickets', os.path.expanduser('~'))
		except Exception as e:
			if type(e) == FileNotFoundError:
				with open((xdg.xdg_config_home().__str__()+'/organizer.config'), "a+") as file:
					file.write(
						"Location of Tickets: /home/unicorn/Documents/tickets")

	#creates a new Ticket
	def createTicket(title='', topic='', effort='', priority='', description='', comments=''):
		description = description.replace('\n', '\\n')
		content = {'Title': title, 'Topic': topic, 'Effort': effort, 'Priority': priority, 'Description': description, 'Position': 'Idea', 'Comments': comments}
		id = str(datetime.datetime.now()).replace(' ', '_').replace('.', '_') + '.ticket'
		path = app.readConfig('Location of Tickets') + '/'
		with open(path + id, 'w') as ticket:
			for entry in content:
				ticket.write(entry + ': ' + content[entry] + '\n')
		

	#gets all the files in the current directory
	def getTickets():
		path = app.readConfig('Location of Tickets')
		fileList = []
		with os.scandir(path) as dirs:
			for entry in dirs:
				start = datetime.now()
				if entry.is_file():					#hides folders
					if entry.name.endswith('.ticket') and not entry.name.startswith('.'):
						fileList.append(entry.name)
		return fileList
	
	#reads the contents in a ticket file, good to get certain items
	def getTicketContent(file):
		dict={}
		path = app.readConfig('Location of Tickets')
		with open(path+'/'+file) as ticket:
			for line in ticket:
				line = line.strip('\n').split(': ')
				if len(line) > 2:
					line[1] = ': '.join(line[1:])
					del line[2:]
				if line[0] == 'Description':
					line[1] = line[1].replace('\\n', '\n')
				dict[line[0]] = line[1]
		return dict
		
	def editTicket(file, setting, content):
		allSettings = app.readTicket(file)
		for settings in allSettings:
			if settings[0] == setting:
				settings[1] = content
			if settings[0] == 'Description':
				settings[1] = settings[1].replace('\n', '\\n')
		with open(app.readConfig('Location of Tickets')+'/'+file, 'w') as ticket:
			for settings in allSettings:
				ticket.write(': '.join(settings) + '\n')

	#needed to edit ticket because dict cant be iterated
	def readTicket(file):
		allSettings = []
		with open(app.readConfig('Location of Tickets')+'/'+file, 'r') as ticket:
			for line in ticket:
				line = line.strip('\n').split(': ')
				if len(line) > 2:
					line[1] = ': '.join(line[1:])
					del line[2:]
				if line[0] == 'Description':
					line[1] = line[1].replace('\\n', '\n')
				allSettings.append(line)
		return(allSettings)
		
	#writes the config
	def setConfig(setting, content):
		allSettings = app.readConfig('allSettings')
		for settings in allSettings:
			if settings[0] == setting:
				settings[1] = content
		with open(xdg.xdg_config_home().__str__()+'/organizer.config', 'w') as config:
			for settings in allSettings:
				config.write(': '.join(settings) + '\n')
			
			
	#reads the config
	def readConfig(setting):
		allSettings = []
		with open(xdg.xdg_config_home().__str__()+'/organizer.config', 'r') as config:
			for line in config:
				line = line.strip('\n').split(': ')
				if setting == 'allSettings':
					allSettings.append(line)
				elif line[0] == setting:
					return(line[1])
		return(allSettings)
