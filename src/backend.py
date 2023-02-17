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

import os
import datetime
from datetime import datetime


class App:

    @staticmethod
    def check_valid_config():
        if __debug__:
            configfolder: str = "src/res"
            ticketfolder: str = "src/res/tickets"
        else:
            configfolder: str = os.environ.get("XDG_CONFIG_HOME")
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        try:
            if os.path.exists(ticketfolder + "/" + App.read_config('Current Board')):
                return
            else:
                os.makedirs(ticketfolder + "/" + App.read_config('Current Board'))
        except Exception as e:
            if type(e) == FileNotFoundError:
                with open((configfolder + '/organizer.config'), "w") as file:
                    file.write("Current Board: test")
                os.makedirs(ticketfolder + "/test")

    # gets all the files in the current directory
    @staticmethod
    def get_tickets():
        if __debug__:
            ticketfolder: str = "src/res/tickets"
        else:
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        path: str = ticketfolder + "/" + App.read_config('Current Board')
        filelist: list[str] = []
        with os.scandir(path) as dirs:
            for entry in dirs:
                if entry.is_file():  # hides folders
                    if entry.name.endswith('.ticket') and not entry.name.startswith('.'):
                        filelist.append(entry.name)
        return filelist

    # creates a new Ticket
    def create_ticket(title='', topic='', effort='', priority='', description='', comments=''):
        if __debug__:
            ticketfolder: str = "src/res/tickets"
        else:
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        description = description.replace('\n', '\\n')
        contents: dict[str, str] = {'Title': title,
                                    'Topic': topic,
                                    'Effort': effort,
                                    'Priority': priority,
                                    'Description': description,
                                    "Position": 'Idea',
                                    'Comments': comments}
        id: str = str(datetime.now()).replace(' ', '_').replace('.', '_') + '.ticket'
        path: str = ticketfolder + "/" + App.read_config('Current Board') + '/'
        with open(path + id, 'w') as ticket:
            for entry in contents:
                ticket.write(entry + ': ' + contents[entry] + '\n')

    # reads the contents in a ticket file, good to get certain items
    def get_ticket_content(file: str):
        if __debug__:
            ticketfolder: str = "src/res/tickets"
        else:
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        contents: dict[str, str] = {}
        path: str = ticketfolder + "/" + App.read_config('Current Board') + '/'
        with open(path + file) as ticket:
            for line in ticket:
                line = line.strip('\n').split(': ')
                if len(line) > 2:
                    content = ': '.join(line[1:])
                else:
                    content = line[1]
                if line[0] == 'Description':
                    content = line[1].replace('\\n', '\n')
                contents[line[0]] = content
        return contents

    def edit_ticket(file: str, setting: str, content: str):
        allsettings = App.read_ticket(file)
        if __debug__:
            ticketfolder: str = "src/res/tickets"
        else:
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        for settings in allsettings:
            if settings[0] == setting:
                settings[1] = content
            if settings[0] == 'Description':
                settings[1] = settings[1].replace('\n', '\\n')
        with open(ticketfolder + "/" + App.read_config('Current Board') + '/' + file, 'w') as ticket:
            for settings in allsettings:
                ticket.write(': '.join(settings) + '\n')

    # needed to edit ticket because dict cant be iterated
    def read_ticket(file: str):
        if __debug__:
            ticketfolder: str = "src/res/tickets"
        else:
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        allsettings: list[list[str]] = []
        with open(ticketfolder + "/" + App.read_config('Current Board') + '/' + file, 'r') as ticket:
            for line in ticket:
                line = line.strip('\n').split(': ')
                if len(line) > 2:
                    line[1] = ': '.join(line[1:])
                    del line[2:]
                if line[0] == 'Description':
                    line[1] = line[1].replace('\\n', '\n')
                allsettings.append(line)
        return allsettings

    # writes the config
    def set_config(setting: str, content: str):
        if __debug__:
            configfolder: str = "src/res"
        else:
            configfolder: str = os.environ.get("XDG_CONFIG_HOME")
        allsettings: list[list[str]] = App.read_config('allSettings')
        for settings in allsettings:
            if settings[0] == setting:
                settings[1] = content
        with open(configfolder + '/organizer.config', 'w') as config:
            for settings in allsettings:
                config.write(': '.join(settings) + '\n')

    # reads the config
    def read_config(setting: str):
        if __debug__:
            configfolder: str = "src/res"
        else:
            configfolder: str = os.environ.get("XDG_CONFIG_HOME")
        allsettings: list[list[str]] = []
        with open(configfolder + '/organizer.config', 'r') as config:
            for line in config:
                contents = line.strip('\n').split(': ')
                if setting == 'allSettings':
                    allsettings.append(contents)
                elif contents[0] == setting:
                    return contents[1]
        return allsettings

    @staticmethod
    def get_boards():
        boards: list[str] = []
        if __debug__:
            ticketfolder: str = "src/res/tickets"
        else:
            ticketfolder: str = os.environ.get("XDG_DATA_HOME") + "/tickets"
        with os.scandir(ticketfolder) as dir:
            for board in dir:
                boards.append(board.name)
        return boards
