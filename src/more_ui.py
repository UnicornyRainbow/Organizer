#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '4.0')
# gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

from backend import App


class Ticket(Gtk.ApplicationWindow):
	def __init__(self, title: str, topic: str, effort: str, priority: str, filename: str):

		self.title = Gtk.Label(label=title, wrap=True, wrap_mode=2)
		self.topic = Gtk.Label(label=topic, wrap=True, wrap_mode=2)

		self.frame = Gtk.Frame()
		self.frame.set_name(filename)
		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

		self.titlebox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.titlebutton = Gtk.Button(hexpand=True, child=self.title)
		self.titlebox.append(self.titlebutton)
		self.topicbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin_start=3)
		self.topicbox.append(self.topic)
		self.valbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True, margin_start=3)
		self.effort = Gtk.Label(label=effort)
		self.effortbox = Gtk.Box()
		self.effortbox.append(self.effort)
		self.priority = Gtk.Label(label=priority)
		self.prioritybox = Gtk.Box()
		self.prioritybox.append(self.priority)

		self.valbox.append(self.effortbox)
		self.valbox.prepend(self.prioritybox)

		self.statusbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.status = Gtk.ComboBoxText()
		self.status.append_text('Idea')
		self.status.append_text('To Do')
		self.status.append_text('Doing')
		self.status.append_text('Stopped')
		self.status.append_text('Done')
		self.statusbox.append(self.status)

		self.box.append(self.titlebox)
		self.box.append(self.topicbox)
		self.box.append(self.valbox)
		self.box.append(self.statusbox)
		self.frame.set_child(self.box)


class Comment(Gtk.ApplicationWindow):
	def __init__(self, comment: str):
		
		self.frame = Gtk.Frame()
		self.box = Gtk.Box(margin_start=5, margin_end=5)
		self.box.append(Gtk.Label(label=comment, wrap=True, wrap_mode=2))
		self.frame.set_child(self.box)
		
		
class TicketDetails(Gtk.ApplicationWindow):
	def __init__(self, filename: str, title: str, topic: str, effort: str, priority: str, position: str, description: str):

		self.spacing = 10

		self.frame = Gtk.Frame(margin_top=self.spacing, margin_bottom=self.spacing)
		self.frame.set_name(filename)
		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, margin_start=self.spacing, margin_end=self.spacing, margin_top=self.spacing, margin_bottom=self.spacing)
		self.frame.set_size_request(380, -1)
		self.box.set_name(filename)

		# Create the necessary structure
		self.headerbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.infobox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.valbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.descriptionbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.entercommentbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=self.spacing)
		self.commentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing)

		# Populate the Window
		self.titlebox = Gtk.Box(hexpand=True)
		self.titlebox.append(Gtk.Label(use_markup=True, wrap=True, wrap_mode=2, label='<b><big><big>' + title + '</big></big></b>'))
		self.close = Gtk.Button(label='Close')

		self.topic = Gtk.Box(hexpand=True)
		self.topic.append(Gtk.Label(use_markup=True, wrap=True, wrap_mode=2, label='<b>Topic: </b>' + topic))
		self.position = Gtk.Label(use_markup=True, label='<b>Status: </b>')
		self.status = Gtk.ComboBoxText()
		self.status.append_text('Idea')
		self.status.append_text('To Do')
		self.status.append_text('Doing')
		self.status.append_text('Stopped')
		self.status.append_text('Done')
		self.set_position(position)

		self.priority = Gtk.Box(hexpand=True)
		self.priority.append(Gtk.Label(use_markup=True, label='<b>Priority: </b>' + priority))
		self.effort = Gtk.Label(use_markup=True, label='<b>Effort: </b>' + effort)

		self.descriptionheader = Gtk.Box()
		self.descriptionheader.append(Gtk.Label(use_markup=True, label='<b>Description: </b>'))
		self.description = Gtk.Box(hexpand=True)
		self.description.append(Gtk.Label(wrap=True, wrap_mode=0, label=description))

		self.entercomment = Gtk.Entry(placeholder_text='Enter a Comment', hexpand=True)
		self.submit = Gtk.Button(label='Submit')
		self.submit.connect('clicked', self.submit_comment)

		# Append everything
		self.headerbox.append(self.titlebox)
		self.headerbox.append(self.close)
		self.infobox.append(self.topic)
		self.infobox.append(self.position)
		self.infobox.append(self.status)
		self.valbox.append(self.priority)
		self.valbox.append(self.effort)
		self.descriptionbox.append(self.descriptionheader)
		self.descriptionbox.append(self.description)
		self.entercommentbox.append(self.entercomment)
		self.entercommentbox.append(self.submit)
		self.get_comments()
		
		self.box.append(self.headerbox)
		self.box.append(self.infobox)
		self.box.append(self.valbox)
		self.box.append(self.descriptionbox)
		self.box.append(self.entercommentbox)
		self.box.append(self.commentbox)
		self.frame.set_child(self.box)
		
	def set_position(self, position: str):
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

	def submit_comment(self, widget: Gtk.Button):
		self.enteredcomment: str = self.entercomment.get_text()
		if self.enteredcomment != '':
			self.comment = Comment(self.enteredcomment)
			self.commentbox.prepend(self.comment.frame)
			self.comments: str = App.get_ticket_content(self.frame.get_name())['Comments']
			if self.comments == '':
				self.comments: list[str] = []
			else:
				self.comments: list[str] = self.comments.split('|')
			self.comments.append(self.enteredcomment)
			self.comments: str = '|'.join(self.comments)
			App.edit_ticket(self.frame.get_name(), 'Comments', self.comments)
			self.entercomment.set_text('')

	def get_comments(self):
		self.comments: str = App.get_ticket_content(self.frame.get_name())['Comments']
		self.comments: list[str] = self.comments.split('|')
		for item in self.comments:
			if item != '':
				self.comment = Comment(item)
				self.commentbox.prepend(self.comment.frame)


class TicketDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self)
		self.set_transient_for(parent)
		self.set_default_size(300, 400)
		self.set_modal(True)
		self.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Create', Gtk.ResponseType.OK)
		self.content: Gtk.Box = self.get_content_area()
		self.contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, hexpand=True, vexpand=True, margin_top=5, margin_start=5, margin_end=5)
		self.content.append(self.contentbox)
		self.title = Gtk.Entry(placeholder_text='Title')
		self.contentbox.append(self.title)
		self.topic = Gtk.Entry(placeholder_text='Topic')
		self.contentbox.append(self.topic)
		self.effort = Gtk.Entry(placeholder_text='Estimated Effort')
		self.contentbox.append(self.effort)
		self.priority = Gtk.Entry(placeholder_text='Priority')
		self.contentbox.append(self.priority)
		self.frame = Gtk.Frame()
		self.description = Gtk.TextView(vexpand=True, left_margin=5, right_margin=5, accepts_tab=False)
		self.description.set_wrap_mode(2)
		self.frame.set_child(self.description)
		self.contentbox.append(self.frame)
		self.show()
