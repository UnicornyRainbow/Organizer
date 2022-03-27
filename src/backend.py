#!/usr/bin/env python3

import os
import datetime


class app():
	
	#creates a new Ticket
	def createTicket(title='', topic='', effort='', priority='', description='', comments=''):
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
				if entry.is_file():					#hides folders
					if entry.name.endswith('.ticket') and not entry.name.startswith('.'):
						fileList.append(entry.name)
		return fileList
	
	#reads the contents in a ticket file
	def getTicketContent(file):
		dict={}
		path = app.readConfig('Location of Tickets')
		with open(path+'/'+file) as ticket:
			for line in ticket:
				line = line.strip('\n').split(': ')
				dict[line[0]] = line[1]
		return dict
		
	def editTicket(file, setting, content):
		allSettings = app.readTicket(file)
		for settings in allSettings:
			if settings[0] == setting:
				settings[1] = content
		with open(app.readConfig('Location of Tickets')+'/'+file, 'w') as ticket:
			for settings in allSettings:
				ticket.write(': '.join(settings) + '\n')
		
	def readTicket(file):
		allSettings = []
		with open(app.readConfig('Location of Tickets')+'/'+file, 'r') as ticket:
			for line in ticket:
				line = line.strip('\n').split(': ')
				allSettings.append(line)
		return(allSettings)
		
	#writes the config
	def setConfig(setting, content):
		allSettings = app.readConfig('allSettings')
		for settings in allSettings:
			if settings[0] == setting:
				settings[1] = content
		with open(os.path.dirname(__file__)+'/organizer.config', 'w') as config:
			for settings in allSettings:
				config.write(': '.join(settings) + '\n')
			
			
	#reads the config
	def readConfig(setting):
		allSettings = []
		with open(os.path.dirname(__file__)+'/organizer.config', 'r') as config:
			for line in config:
				line = line.strip('\n').split(': ')
				if setting == 'allSettings':
					allSettings.append(line)
				elif line[0] == setting:
					return(line[1])
		return(allSettings)
