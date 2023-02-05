#!/usr/bin/env python3

import gi
import sys

gi.require_version('Adw', '1')

from gi.repository import Adw, Gio

from window import Window
from backend import App


class MyApp(Adw.Application):
	def __init__(self):
		Adw.Application.__init__(self, application_id="io.github.unicornyrainbow.organizer", flags=Gio.ApplicationFlags.FLAGS_NONE)

	def do_activate(self):
		win = self.props.active_window
		if not win:
			win: Window = Window(application=self)
		win.present()


App.check_valid_config()

app = MyApp()
app.run(sys.argv)
