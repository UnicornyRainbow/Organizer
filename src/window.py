#!/usr/bin/env python3

import gi
gi.require_version('Gtk','4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import backend
import more_ui
from backend import app
from more_ui import Ticket, ticketDialog

class window(Gtk.ApplicationWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		app3 = self.get_application()
		sm = app3.get_style_manager()
		sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
		
		self.spacing = 10
		
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
		self.mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = self.spacing)
		self.set_child(self.mainBox)
		
		self.bigBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.bigBox.set_margin_start(self.spacing)
		self.bigBox.set_margin_end(self.spacing)
		self.bigBox.set_margin_top(self.spacing)
		self.bigBox.set_margin_bottom(self.spacing)
		self.mainBox.append(self.bigBox)
		self.testbox = Gtk.ScrolledWindow()
		self.titleBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = self.spacing)
		self.bigBox.append(self.titleBox)

		#Scrollable box for the tickets
		self.scrolledWindow = Gtk.ScrolledWindow()
		self.scrolledWindow.set_vexpand(True)
		self.scrolledWindow.set_hexpand(True)
		self.bigBox.append(self.scrolledWindow)
		
		
		

		#Populate the Header Bar

		#Create new Ticket
		self.newButton = Gtk.Button()
		self.newIcon = Gtk.Image.new_from_icon_name("document-new-symbolic")
		self.newButton.set_child(self.newIcon)
		self.newButton.connect('clicked', self.newTicket)
		self.headerBar.pack_start(self.newButton)

		#Button to test functions
		self.testButton = Gtk.Button()
		self.testButton.set_label('test')
		self.testButton.connect('clicked', self.tester)
		self.headerBar.pack_start(self.testButton)

		#Hamburger Menu
		#Popover and Button
		self.popover = Gtk.Popover()
		self.popover.set_position(Gtk.PositionType.BOTTOM)
		self.menuButton = Gtk.MenuButton(popover=self.popover)
		self.menuIcon = Gtk.Image.new_from_icon_name("open-menu-symbolic")
		#self.menuButton.set_child(self.menuIcon)
		self.headerBar.pack_end(self.menuButton)
		#add a box to the Menu
		self.menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing)
		self.popover.set_child(self.menuBox)
		#add Menu Items 
		self.folderChooser = Gtk.Button()
		self.folderIcon = Gtk.Image.new_from_icon_name('folder-open-symbolic')
		self.folderChooser.set_child(self.folderIcon)
		self.folderChooser.connect('clicked', self.folderClicked)
		self.menuBox.append(self.folderChooser)

		
		#Ticket Boxes
		self.columnWidth = 180#118
		self.ticketBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = self.spacing, homogeneous = True)
		self.scrolledWindow.set_child(self.ticketBox)
		self.idea = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.idea.set_size_request(self.columnWidth, -1)
		self.idea.set_hexpand(True)
		self.ticketBox.append(self.idea)
		self.todo = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.todo.set_size_request(self.columnWidth, -1)
		self.todo.set_hexpand(True)
		self.ticketBox.append(self.todo)
		self.inProgress = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.inProgress.set_size_request(self.columnWidth, -1)
		self.inProgress.set_hexpand(True)
		self.ticketBox.append(self.inProgress)
		self.stopped = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.stopped.set_size_request(self.columnWidth, -1)
		self.stopped.set_hexpand(True)
		self.ticketBox.append(self.stopped)
		self.done = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing)
		self.done.set_size_request(self.columnWidth, -1)
		self.done.set_hexpand(True)
		self.ticketBox.append(self.done)
		
		#Title of Ticket Categories
		self.ideaLabel = Gtk.Label()
		self.ideaLabel.set_markup('<big><b>Idea</b></big>')
		self.todoLabel = Gtk.Label()
		self.todoLabel.set_markup('<big><b>To Do</b></big>')
		self.inProgressLabel = Gtk.Label()
		self.inProgressLabel.set_markup('<big><b>In Progress</b></big>')
		self.stoppedLabel = Gtk.Label()
		self.stoppedLabel.set_markup('<big><b>Stopped</b></big>')
		self.doneLabel = Gtk.Label()
		self.doneLabel.set_markup('<big><b>Done</b></big>')
		
		self.titleBox.append(self.ideaLabel)
		self.ideaLabel.set_size_request(self.columnWidth, -1)
		self.ideaLabel.set_hexpand(True)
		self.titleBox.append(self.todoLabel)
		self.todoLabel.set_size_request(self.columnWidth, -1)
		self.todoLabel.set_hexpand(True)
		self.titleBox.append(self.inProgressLabel)
		self.inProgressLabel.set_size_request(self.columnWidth, -1)
		self.inProgressLabel.set_hexpand(True)
		self.titleBox.append(self.stoppedLabel)
		self.stoppedLabel.set_size_request(self.columnWidth, -1)
		self.stoppedLabel.set_hexpand(True)
		self.titleBox.append(self.doneLabel)
		self.doneLabel.set_size_request(self.columnWidth, -1)
		self.doneLabel.set_hexpand(True)
		
		#finally loads the Tickets for the first time
		self.getTickets()
		
		
		
	def tester(self, widget):
		print(self)
		
	
	def openTicket(self, widget):
		self.detailBox = Gtk.Box()
		self.detailBox.set_size_request(100, -1)
		self.mainBox.append(self.detailBox)
		
	def moveTicket(self, widget):
		self.category = widget.get_active_text()
		self.ticket = widget.get_parent().get_parent().get_parent()
		app.editTicket(self.ticket.get_name(), 'Position', self.category)
		self.reloadTickets()
		
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
		
		
	def getTickets(self):
		files = app.getTickets()
		for file in files:
			content = app.getTicketContent(file)
			self.newticket = Ticket(content['Title'], content['Topic'], content['Effort'], content['Priority'], file)
			if content['Position'] == 'Idea':
				self.newticket.status.set_active(0)
				self.idea.append(self.newticket.frame)
			elif content['Position'] == 'To Do':
				self.newticket.status.set_active(1)
				self.todo.append(self.newticket.frame)
			elif content['Position'] == 'In Progress':
				self.newticket.status.set_active(2)
				self.inProgress.append(self.newticket.frame)
			elif content['Position'] == 'Stopped':
				self.newticket.status.set_active(3)
				self.stopped.append(self.newticket.frame)
			elif content['Position'] == 'Done':
				self.newticket.status.set_active(4)
				self.done.append(self.newticket.frame)
			self.newticket.status.connect('changed', self.moveTicket)
			self.newticket.titleButton.connect('clicked', self.openTicket)
			
			
	def reloadTickets(self):
		while self.idea.get_first_child():
			self.idea.remove(self.idea.get_first_child())
		while self.todo.get_first_child():
			self.todo.remove(self.todo.get_first_child())
		while self.inProgress.get_first_child():
			self.inProgress.remove(self.inProgress.get_first_child())
		while self.stopped.get_first_child():
			self.stopped.remove(self.stopped.get_first_child())
		while self.done.get_first_child():
			self.done.remove(self.done.get_first_child())
		self.getTickets()
	
		
	#creates new Ticket
	def newTicket(self, widget):
		dialog = ticketDialog(self)
		dialog.connect('response', self.on_ticket_response)
	def on_ticket_response(self, widget, response_id):
		if response_id == Gtk.ResponseType.OK:
			app.createTicket(widget.title.get_text(), widget.topic.get_text(), widget.effort.get_text(), widget.priority.get_text(), widget.description.get_text())
			self.reloadTickets()
		widget.destroy()
