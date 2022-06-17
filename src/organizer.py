#!/usr/bin/env python3

import gi
import sys
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio

import window
from window import window
import backend
from backend import app

class MyApp(Adw.Application):
	def __init__(self):
		Adw.Application.__init__(self, application_id="io.github.unicornyrainbow.organizer", flags=Gio.ApplicationFlags.FLAGS_NONE)

	def do_activate(self):
		win = self.props.active_window
		if not win:
			win = window(application=self)
		win.present()

app.checkValidConfig()
app2=MyApp()
app2.run(sys.argv)