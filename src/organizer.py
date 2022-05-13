#!/usr/bin/env python3

import gi
import sys
gi.require_version('Adw', '1')
from gi.repository import Adw

import window
from window import window
import backend
from backend import app

class MyApp(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.connect('activate', self.on_activate)

	def on_activate(self, app):
		self.win = window(application = app)
		self.win.present()
	
app.checkValidConfig()
app2=MyApp(application_id='org.Unicorn.organizer')
app2.run(sys.argv)