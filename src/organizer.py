#!/usr/bin/env python3

# Organizer
#     Copyright (C) 2023  UnicornyRainbow
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
