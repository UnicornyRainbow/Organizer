#!/usr/bin/env python3

import os
import datetime
import gi
import sys
gi.require_version('Gtk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class Ticket(Gtk.Window):
	def __init__(self, title, topic, effort, priority):
		self.frame = Gtk.Frame()
		self.frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
		self.box.set_border_width(10)
		
		self.titleBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.title = Gtk.Label()
		self.title.set_label(title)
		self.titleBox.pack_start(self.title, False, True, 0)
		self.topicBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.topic = Gtk.Label()
		self.topic.set_label(topic)
		self.topicBox.pack_start(self.topic, False, True, 0)
		self.valBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.effort = Gtk.Label()
		self.effort.set_label(effort)
		self.priority = Gtk.Label()
		self.priority.set_label(priority)
		
		self.valBox.pack_start(self.effort, False, True, 0)
		self.valBox.pack_end(self.priority, False, True, 0)
		
		self.statusBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.status = Gtk.ComboBoxText()
		self.status.append_text('Idea')
		self.status.append_text('To Do')
		self.status.append_text('In Progress')
		self.status.append_text('On Hold/Waiting')
		self.status.append_text('Done')
		self.status.connect('changed', self.moveTo)
		self.statusBox.pack_start(self.status, True, True, 0)
		
		self.box.add(self.titleBox)
		self.box.add(self.topicBox)
		self.box.add(self.valBox)
		self.box.add(self.statusBox)
		self.frame.add(self.box)
		
		#self.idea.add(self.box)
		
	def moveTo(self, widget):
		file = widget.get_active_text()
		if file == 'Idea':
			pass
		elif file == 'To Do':
			pass
		elif file == 'In Progress':
			pass
		elif file == 'On Hold/Waiting':
			pass
		elif file == 'Done':
			pass
		
	def getFile(self):
		pass
		
	def setFile(self):
		pass
		
	def setDescription(self):
		pass
		
	def setComment(self):
		pass


class app():
	
	#creates a new Ticket
	def createTicket(title, topic, effort, priority, description):
		content = {'Title': title, 'Topic': topic, 'Effort': effort, 'Priority': priority, 'Description': description}
		id = str(datetime.datetime.now()).replace(' ', '_').replace('.', '_') + '.ticket'
		path = app.readConfig('Location of Tickets') + '/'
		with open(path + id, 'w') as ticket:
			for entry in content:
				ticket.write(entry + ': ' + content[entry] + '\n')
		#app.getTickets()
	
	#gets all the files in the current directory
	def getTickets():
		path = app.readConfig('Location of Tickets')
		fileList = []
		with os.scandir(path) as dirs:
			for entry in dirs:
				if entry.is_file():					#hides folders
					if entry.name.endswith('.ticket') and not entry.name.startswith('.'):
						fileList.append(entry.name)
			
		print(fileList)				
		#return fileList
		
	#writes the config
	def setConfig(setting, content):
		allSettings = app.readConfig('allSettings')
		for settings in allSettings:
			if settings[0] == setting:
				settings[1] = content
		with open('board.config', 'w') as config:
			for settings in allSettings:
				config.write(': '.join(settings) + '\n')
			
			
	#reads the config
	def readConfig(setting):
		allSettings = []
		with open('board.config', 'r') as config:
			for line in config:
				line = line.strip().split(': ')
				if setting == 'allSettings':
					allSettings.append(line)
				elif line[0] == setting:
					return(line[1])
		return(allSettings)

class window(Gtk.ApplicationWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)#'Codey', 960, 540, **kwargs)
		
		app3 = self.get_application()
		sm = app3.get_style_manager()
		sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
		
		#window
		Gtk.Window.__init__(self, title='Organizer')
		self.set_default_size(-1, 540)

		
		#Define the General structure of the Window

		#Header Bar
		self.headerBar = Gtk.HeaderBar()
		self.set_titlebar(self.headerBar)
		self.headerBar.set_show_title_buttons(True)
		self.title = Gtk.Label()
		self.title.set_label('Organizer')
		self.headerBar.set_title_widget(self.title)
		
		#Setup general window Structure
		self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		self.set_child(self.mainBox)
		
		self.bigBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.mainBox.append(self.bigBox)
		self.titleBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		self.bigBox.append(self.titleBox)

		#Scrollable box for the tickets
		self.scrolledWindow = Gtk.ScrolledWindow()
		self.scrolledWindow.set_vexpand(True)
		self.scrolledWindow.set_hexpand(True)
		self.bigBox.append(self.scrolledWindow)
		
		#Window For Ticket Details
		self.detailBox = Gtk.Box()
		self.mainBox.prepend(self.detailBox)
		


		#Populate the Header Bar

		#Create new Ticket
		self.newButton = Gtk.Button()
		self.newIcon = Gtk.Image.new_from_icon_name("document-new-symbolic")
		self.newButton.set_child(self.newIcon)
		self.newButton.connect('clicked', self.newTicket)
		self.headerBar.pack_start(self.newButton)

		#Hamburger Menu
		#Popover and Button
		self.popover = Gtk.Popover()
		self.popover.set_position(Gtk.PositionType.BOTTOM)
		self.menuButton = Gtk.MenuButton(popover=self.popover)
		self.menuIcon = Gtk.Image.new_from_icon_name("open-menu-symbolic")
		#self.menuButton.set_child(self.menuIcon)
		self.headerBar.pack_end(self.menuButton)
		#add a box to the Menu
		self.menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.popover.set_child(self.menuBox)
		#add Menu Items 
		self.folderChooser = Gtk.Button()
		self.folderIcon = Gtk.Image.new_from_icon_name('folder-open-symbolic')
		self.folderChooser.set_child(self.folderIcon)
		self.folderChooser.connect('clicked', self.folderClicked)
		self.menuBox.append(self.folderChooser)

		
		#Ticket Boxes
		self.ticketBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
		self.scrolledWindow.set_child(self.ticketBox)
		self.idea = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.idea.set_size_request(143, -1)
		self.ticketBox.append(self.idea)
		self.todo = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.todo.set_size_request(143, -1)
		self.ticketBox.append(self.todo)
		self.inProgress = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.inProgress.set_size_request(143, -1)
		self.ticketBox.append(self.inProgress)
		self.onHold = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.onHold.set_size_request(143, -1)
		self.ticketBox.append(self.onHold)
		self.done = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.done.set_size_request(143, -1)
		self.ticketBox.append(self.done)
		
		#Title of Ticket Categories
		self.ideaLabel = Gtk.Label()
		self.ideaLabel.set_markup('<big><b>Idea</b></big>')
		self.todoLabel = Gtk.Label()
		self.todoLabel.set_markup('<big><b>To Do</b></big>')
		self.inProgressLabel = Gtk.Label()
		self.inProgressLabel.set_markup('<big><b>In Progress</b></big>')
		self.onHoldLabel = Gtk.Label()
		self.onHoldLabel.set_markup('<big><b>On Hold/Waiting</b></big>')
		self.doneLabel = Gtk.Label()
		self.doneLabel.set_markup('<big><b>Done</b></big>')
		
		self.titleBox.append(self.ideaLabel)
		self.ideaLabel.set_size_request(143, -1)
		self.titleBox.append(self.todoLabel)
		self.todoLabel.set_size_request(143, -1)
		self.titleBox.append(self.inProgressLabel)
		self.inProgressLabel.set_size_request(143, -1)
		self.titleBox.append(self.onHoldLabel)
		self.onHoldLabel.set_size_request(143, -1)
		self.titleBox.append(self.doneLabel)
		self.doneLabel.set_size_request(143, -1)
		
		
		
	#opens dialog to choose folder to look in
	def folderClicked(self, widget):
		dialog = Gtk.FileChooserDialog(title='Select a Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
		dialog.set_transient_for(self)
		dialog.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
		dialog.connect('response', self.on_dialog_response)
		dialog.show()
		
	def on_dialog_response(self, widget, response_id):
		if response_id == Gtk.ResponseType.OK:
			app.setConfig('Location of Tickets', widget.get_file().get_path())
		widget.destroy()
		
		
	#creates new Ticket
	def newTicket(self, widget):
		dialog = ticketDialog(self)
		dialog.connect('response', self.on_ticket_response)
		
	def on_ticket_response(self, widget, response_id):
		if response_id == Gtk.ResponseType.OK:
			app.createTicket(widget.title.get_text(), widget.topic.get_text(), widget.effort.get_text(), widget.priority.get_text(), widget.description.get_text())
		widget.destroy()
		
class ticketDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Create', Gtk.ResponseType.OK)
		self.content = self.get_content_area()
		self.contentBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		#self.contentBox.set_border_width(10)
		self.content.append(self.contentBox)
		self.title = Gtk.Entry()
		self.title.set_placeholder_text('Title')
		self.contentBox.append(self.title)
		self.topic = Gtk.Entry()
		self.topic.set_placeholder_text('Topic')
		self.contentBox.append(self.topic)
		self.effort = Gtk.Entry()
		self.effort.set_placeholder_text('Estimated Effort')
		self.contentBox.append(self.effort)
		self.priority = Gtk.Entry()
		self.priority.set_placeholder_text('Priority')
		self.contentBox.append(self.priority)
		self.description = Gtk.Entry()
		self.description.set_placeholder_text('Enter a Description')
		self.contentBox.append(self.description)
		self.show()
		
		
	#move ticket with dropdown
	#save and load tickets, add ticket id(maybe show id in frame?)
	#click Ticket to open details in side window
	#add description(entered in when created)
	#add comments
	#setting for topic and choose them via dropdown
	#setting to choose where tickets saved

class MyApp(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.connect('activate', self.on_activate)

	def on_activate(self, app):
		self.win = window(application = app)
		self.win.present()
	

#window = window()
#window.connect('delete-event', Gtk.main_quit)
#window.show_all()
#Gtk.main()
app2=MyApp(application_id='org.Unicorn.Codey')
app2.run(sys.argv)
