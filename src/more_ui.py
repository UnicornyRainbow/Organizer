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
		self.titleButton = Gtk.Button()
		self.titleButton.set_hexpand(True)
		self.titleButton.set_child(self.title)
		self.titleBox.append(self.titleButton)
		self.topicBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		self.topicBox.set_margin_start(3)
		self.topicBox.append(self.topic)
		self.valBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,homogeneous = True)
		self.valBox.set_margin_start(3)
		self.effort = Gtk.Label()
		self.effort.set_label(effort)
		self.effortBox = Gtk.Box()
		self.effortBox.append(self.effort)
		self.priority = Gtk.Label()
		self.priority.set_label(priority)
		self.priorityBox = Gtk.Box()
		self.priorityBox.append(self.priority)
		
		self.valBox.append(self.effortBox)
		self.valBox.prepend(self.priorityBox)
		
		self.statusBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.status = Gtk.ComboBoxText()
		self.status.append_text('Idea')
		self.status.append_text('To Do')
		self.status.append_text('In Progress')
		self.status.append_text('Stopped')
		self.status.append_text('Done')
		self.statusBox.append(self.status)
		
		self.box.append(self.titleBox)
		self.box.append(self.topicBox)
		self.box.append(self.valBox)
		self.box.append(self.statusBox)
		self.frame.set_child(self.box)


class ticketDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Create', Gtk.ResponseType.OK)
		self.content = self.get_content_area()
		self.contentBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
		self.content.append(self.contentBox)
		self.contentBox.set_hexpand(True)
		self.contentBox.set_vexpand(True)
		self.title = Gtk.Entry()
		self.title.set_placeholder_text('Title')
		self.title.set_max_length(100)
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
		self.description.set_vexpand(True)
		self.contentBox.append(self.description)
		self.show()
