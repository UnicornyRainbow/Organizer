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

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

from backend import App
from more_ui import Ticket, TicketDetails

if __debug__:
    uipath = "src/res/organizer.ui"
else:
    uipath = "/app/bin/organizer.ui"


@Gtk.Template(filename=uipath)
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    mainBox: Gtk.Box = Gtk.Template.Child()
    popover: Gtk.Popover = Gtk.Template.Child()
    popoverBox: Gtk.Box = Gtk.Template.Child()
    newTicketFlap: Adw.Flap = Gtk.Template.Child()
    title: Gtk.Entry = Gtk.Template.Child()
    topic: Gtk.Entry = Gtk.Template.Child()
    effort: Gtk.Entry = Gtk.Template.Child()
    priority: Gtk.Entry = Gtk.Template.Child()
    description: Gtk.TextView = Gtk.Template.Child()
    bigbox: Gtk.Box = Gtk.Template.Child()
    ticketscroll: Gtk.Box = Gtk.Template.Child()
    ticketbox: Gtk.Box = Gtk.Template.Child()
    idea: Gtk.Box = Gtk.Template.Child()
    todo: Gtk.Box = Gtk.Template.Child()
    doing: Gtk.Box = Gtk.Template.Child()
    stopped: Gtk.Box = Gtk.Template.Child()
    done: Gtk.Box = Gtk.Template.Child()
    detailscroll: Gtk.ScrolledWindow = Gtk.Template.Child()
    detailbox: Gtk.Box = Gtk.Template.Child()
    boardchooser: Gtk.ComboBoxText() = Gtk.Template.Child()
    aboutDialog: Adw.AboutWindow = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def on_destroy(self, *args):
        Gtk.main_quit()

    @Gtk.Template.Callback()
    def tester(self, widget):
        pass

    def add_boards(self):
        boards = App.get_boards()
        for board in boards:
            self.boardchooser.append_text(board)
        self.boardchooser.set_active(boards.index(App.read_config("Current Board")))

    def get_tickets(self):
        files = App.get_tickets()
        for file in files:
            content = App.get_ticket_content(file)
            self.newticket = Ticket(content['Title'], content['Topic'], content['Effort'], content['Priority'], file)
            if content['Position'] == 'Idea':
                self.newticket.status.set_active(0)
                self.idea.append(self.newticket.frame)
            elif content['Position'] == 'To Do':
                self.newticket.status.set_active(1)
                self.todo.append(self.newticket.frame)
            elif content['Position'] == 'Doing':
                self.newticket.status.set_active(2)
                self.doing.append(self.newticket.frame)
            elif content['Position'] == 'Stopped':
                self.newticket.status.set_active(3)
                self.stopped.append(self.newticket.frame)
            elif content['Position'] == 'Done':
                self.newticket.status.set_active(4)
                self.done.append(self.newticket.frame)
            self.newticket.status.connect('changed', self.move_ticket)
            self.newticket.titlebutton.connect('clicked', self.open_details)

    def reload_tickets(self):
        while self.idea.get_first_child():
            self.idea.remove(self.idea.get_first_child())
        while self.todo.get_first_child():
            self.todo.remove(self.todo.get_first_child())
        while self.doing.get_first_child():
            self.doing.remove(self.doing.get_first_child())
        while self.stopped.get_first_child():
            self.stopped.remove(self.stopped.get_first_child())
        while self.done.get_first_child():
            self.done.remove(self.done.get_first_child())
        self.get_tickets()

    @Gtk.Template.Callback()
    def board_changed(self, widget: Gtk.ComboBoxText):
        App.set_config("Current Board", widget.get_active_text())
        self.reload_tickets()

    def close_details(self, widget):
        self.detailbox.remove(widget.get_parent().get_parent().get_parent())
        if self.detailbox.get_first_child() is None:
            self.mainBox.remove(self.detailscroll)

    def open_details(self, widget: Gtk.Button):
        if self.detailscroll.get_parent() is None:
            self.mainBox.append(self.detailscroll)
        file: str = widget.get_parent().get_parent().get_parent().get_name()
        content = App.get_ticket_content(file)
        self.ticketdetails = TicketDetails(file, content['Title'], content['Topic'], content['Effort'],
                                           content['Priority'], content['Position'], content['Description'])
        self.detailbox.append(self.ticketdetails.frame)
        self.ticketdetails.status.connect('changed', self.move_ticket)
        self.ticketdetails.close.connect('clicked', self.close_details)

    def move_ticket(self, widget: Gtk.ComboBoxText):
        self.category: str = widget.get_active_text()
        self.ticket: Gtk.Frame = widget.get_parent().get_parent().get_parent()
        App.edit_ticket(self.ticket.get_name(), 'Position', self.category)
        if self.ticket.get_parent().get_parent() == self.ticketbox:
            self.ticket.get_parent().remove(self.ticket)
            if self.category == "Idea":
                self.idea.append(self.ticket)
            elif self.category == "To Do":
                self.todo.append(self.ticket)
            elif self.category == "Doing":
                self.doing.append(self.ticket)
            elif self.category == "Stopped":
                self.stopped.append(self.ticket)
            elif self.category == "Done":
                self.done.append(self.ticket)
            for section in self.mainBox:
                if section == self.detailscroll:
                    for child in self.detailbox:
                        if child.get_name() == self.ticket.get_name():
                            self.close_details(child.get_first_child().get_first_child().get_first_child())
                            self.open_details(self.ticket.get_first_child().get_first_child().get_first_child())
        else:
            self.reload_tickets()

    # creates new Ticket
    @Gtk.Template.Callback()
    def new_ticket(self, widget: Gtk.Button):
        self.newTicketFlap.set_reveal_flap(not self.newTicketFlap.get_reveal_flap())
        self.title.set_text("")
        self.topic.set_text("")
        self.effort.set_text("")
        self.priority.set_text("")
        self.description.set_buffer(Gtk.TextBuffer())

    @Gtk.Template.Callback()
    def create_ticket_clicked(self, widget: Gtk.Button):
        desc = self.description.get_buffer().get_text(self.description.get_buffer().get_start_iter(),
                                                            self.description.get_buffer().get_end_iter(), False)
        App.create_ticket(self.title.get_text(), self.topic.get_text(), self.effort.get_text(), self.priority.get_text(), desc)
        self.newTicketFlap.set_reveal_flap(False)
        self.title.set_text("")
        self.topic.set_text("")
        self.effort.set_text("")
        self.priority.set_text("")
        self.description.set_buffer(Gtk.TextBuffer())
        self.reload_tickets()

    def on_ticket_response(self, widget, responseid):
        if responseid == Gtk.ResponseType.OK:
            desc = widget.description.get_buffer().get_text(widget.description.get_buffer().get_start_iter(),
                                                            widget.description.get_buffer().get_end_iter(), False)
            App.create_ticket(widget.title.get_text(), widget.topic.get_text(), widget.effort.get_text(), widget.priority.get_text(), desc)
            self.reload_tickets()
        widget.destroy()

    @Gtk.Template.Callback()
    def about_clicked(self, *args):
        self.aboutDialog.show()
