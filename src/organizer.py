#!/usr/bin/env python3

import gi
import sys
gi.require_version('Adw', '1')
from gi.repository import Adw

import window
from window import window

class MyApp(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.connect('activate', self.on_activate)

	def on_activate(self, app):
		self.win = window(application = app)
		self.win.present()
	


app2=MyApp(application_id='org.Unicorn.Organizer')
app2.run(sys.argv)

	
#click Ticket to open details in side window Detail Window
	#close button
	#change position
	#show infos(title, topic, description etc...)
	#show Ticket id?
	#add comments
	#edit previously entered values
	#Button to delete Ticket
#setting for topic and choose them via dropdown
#delete old Tickets(maybe only on startup?)
	#dont really delete them, make hidden files
	#setting when to delete
