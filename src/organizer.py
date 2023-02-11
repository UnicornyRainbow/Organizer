#!/usr/bin/env python3

import gi
import sys

gi.require_version('Adw', '1')

from gi.repository import Adw, Gio

from window import MainWindow
from backend import App


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        window = self.props.active_window
        if not window:
            window: MainWindow = MainWindow(application=self)

        window.mainBox.remove(window.mainBox.get_last_child())
        window.mainBox.remove(window.mainBox.get_first_child())
        window.popover.set_child(window.popoverBox)
        window.add_boards()
        window.present()


App.check_valid_config()

app = MyApp(application_id='io.github.unicornyrainbow.organizer', flags=Gio.ApplicationFlags.FLAGS_NONE)
app.run(sys.argv)
