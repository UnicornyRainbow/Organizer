#!/usr/bin/env python3

import gi
gi.require_version('Gtk','4.0')
from gi.repository import Gtk

import backend
from backend import app

class Ticket(Gtk.ApplicationWindow):
	def __init__(self, title, topic, effort, priority, filename):
		
		self.title = Gtk.Label(label = title, wrap = True, wrap_mode = 2)
		self.topic = Gtk.Label(label = topic, wrap = True, wrap_mode = 2)
		
		self.frame = Gtk.Frame()
		self.frame.set_name(filename)
		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 2)
		
		self.titleBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.titleButton = Gtk.Button(hexpand = True, child = self.title)
		self.titleBox.append(self.titleButton)
		self.topicBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, margin_start = 3)
		self.topicBox.append(self.topic)
		self.valBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,homogeneous = True, margin_start = 3)
		self.effort = Gtk.Label(label = effort)
		self.effortBox = Gtk.Box()
		self.effortBox.append(self.effort)
		self.priority = Gtk.Label(label = priority)
		self.priorityBox = Gtk.Box()
		self.priorityBox.append(self.priority)
		
		self.valBox.append(self.effortBox)
		self.valBox.prepend(self.priorityBox)
		
		self.statusBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.status = Gtk.ComboBoxText()
		self.status.append_text('Idea')
		self.status.append_text('To Do')
		self.status.append_text('Doing')
		self.status.append_text('Stopped')
		self.status.append_text('Done')
		self.statusBox.append(self.status)
		
		self.box.append(self.titleBox)
		self.box.append(self.topicBox)
		self.box.append(self.valBox)
		self.box.append(self.statusBox)
		self.frame.set_child(self.box)
		
		
		
		
class ticketDetails(Gtk.ApplicationWindow):
	def __init__(self, filename, title, topic, effort, priority, position, description):
		
		self.spacing = 10
		
		self.frame = Gtk.Frame(margin_top = self.spacing, margin_bottom = self.spacing)
		self.frame.set_name(filename)
		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.spacing, margin_start = self.spacing, margin_end = self.spacing, margin_top = self.spacing, margin_bottom = self.spacing)
		self.frame.set_size_request(380, -1)
		self.box.set_name(filename)
		
		#Create the necessary structure
		self.headerBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.infoBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.valBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.descriptionBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		
		#Populate the Window
		self.titleBox = Gtk.Box(hexpand = True)
		self.titleBox.append(Gtk.Label(use_markup = True, wrap = True, wrap_mode = 2, label = '<b><big><big>' + title + '</big></big></b>'))		
		self.close = Gtk.Button(label = 'Close')
		
		self.topic = Gtk.Box(hexpand = True)
		self.topic.append(Gtk.Label(use_markup = True, wrap = True, wrap_mode = 2, label = '<b>Topic: </b>' + topic))
		self.position = Gtk.Label(use_markup = True, label = '<b>Status: </b>')
		self.status = Gtk.ComboBoxText()
		self.status.append_text('Idea')
		self.status.append_text('To Do')
		self.status.append_text('Doing')
		self.status.append_text('Stopped')
		self.status.append_text('Done')
		self.setPosition(position)
		
		self.priority = Gtk.Box(hexpand = True)
		self.priority.append(Gtk.Label(use_markup = True, label = '<b>Priority: </b>' + priority))
		self.effort = Gtk.Label(use_markup = True, label = '<b>Effort: </b>' + effort)
		
		self.descriptionHeader = Gtk.Box()
		self.descriptionHeader.append(Gtk.Label(use_markup = True, label = '<b>Description: </b>'))
		self.description = Gtk.Box(hexpand = True)
		self.description.append(Gtk.Label(wrap = True, wrap_mode = 0, label = description))
		
		#Append everything
		self.headerBox.append(self.titleBox)
		self.headerBox.append(self.close)
		self.infoBox.append(self.topic)
		self.infoBox.append(self.position)
		self.infoBox.append(self.status)
		self.valBox.append(self.priority)
		self.valBox.append(self.effort)
		self.descriptionBox.append(self.descriptionHeader)
		self.descriptionBox.append(self.description)
		
		self.box.append(self.headerBox)
		self.box.append(self.infoBox)
		self.box.append(self.valBox)
		self.box.append(self.descriptionBox)
		self.frame.set_child(self.box)
		
	def setPosition(self, position):
		if position == 'Idea':
			self.status.set_active(0)
		elif position == 'To Do':
			self.status.set_active(1)
		elif position == 'Doing':
			self.status.set_active(2)
		elif position == 'Stopped':
			self.status.set_active(3)
		elif position == 'Done':
			self.status.set_active(4)
	
	


class ticketDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.set_modal(True)
		self.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Create', Gtk.ResponseType.OK)
		self.content = self.get_content_area()
		self.contentBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10, hexpand = True, vexpand = True)
		self.content.append(self.contentBox)
		self.title = Gtk.Entry(placeholder_text = 'Title')
		self.contentBox.append(self.title)
		self.topic = Gtk.Entry(placeholder_text = 'Topic')
		self.contentBox.append(self.topic)
		self.effort = Gtk.Entry(placeholder_text = 'Estimated Effort')
		self.contentBox.append(self.effort)
		self.priority = Gtk.Entry(placeholder_text = 'Priority')
		self.contentBox.append(self.priority)
		self.description = Gtk.Entry(placeholder_text = 'Enter a Description', vexpand = True)
		self.contentBox.append(self.description)
		self.show()
