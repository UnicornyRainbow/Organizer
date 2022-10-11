#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from backend import app
from more_ui import Ticket, ticketDialog, ticketDetails


class window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app3 = self.get_application()
        sm = app3.get_style_manager()

        self.spacing = 10

        # window
        Gtk.Window.__init__(self, title='Organizer')
        self.set_default_size(960, 540)

        # Define the General structure of the Window

        # Header Bar
        self.headerBar = Gtk.HeaderBar()
        self.set_titlebar(self.headerBar)
        self.headerBar.set_show_title_buttons(True)
        self.title = Gtk.Label()
        self.title.set_label('Organizer')
        self.headerBar.set_title_widget(self.title)

        # Setup general window Structure
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_child(self.mainBox)

        # Box for Ticket columns and Headers
        self.bigBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, margin_start=self.spacing,
                              margin_end=self.spacing, margin_top=self.spacing, margin_bottom=self.spacing)
        self.mainBox.append(self.bigBox)
        self.testbox = Gtk.ScrolledWindow()
        self.titleBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=self.spacing)
        self.bigBox.append(self.titleBox)
        # Scrollable box for the tickets
        self.ticketScroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.bigBox.append(self.ticketScroll)

        # Box for Ticket Details
        self.detailScroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True, margin_start=self.spacing,
                                               margin_end=self.spacing, margin_top=self.spacing,
                                               margin_bottom=self.spacing)
        self.detailScroll.set_size_request(380, -1)
        self.detailBox = Gtk.Box(vexpand=True, hexpand=True, orientation=Gtk.Orientation.HORIZONTAL,
                                 spacing=self.spacing)
        self.detailScroll.set_child(self.detailBox)

        # Populate the Header Bar

        # Create new Ticket
        self.newButton = Gtk.Button()
        self.newIcon = Gtk.Image.new_from_icon_name("document-new-symbolic")
        self.newButton.set_child(self.newIcon)
        self.newButton.connect('clicked', self.newTicket)
        self.headerBar.pack_start(self.newButton)

        self.boardChooser = Gtk.ComboBoxText()
        self.addBoards()
        self.boardChooser.connect("changed", self.boardChanged)
        self.headerBar.pack_start(self.boardChooser)

        # Button to test functions
        self.testButton = Gtk.Button(label='test')
        self.testButton.connect('clicked', self.tester)
        self.headerBar.pack_start(self.testButton)

        # Hamburger Menu
        # Popover and Button
        self.popover = Gtk.Popover(position=Gtk.PositionType.BOTTOM)
        self.menuButton = Gtk.MenuButton(popover=self.popover, icon_name="open-menu-symbolic", primary=True)
        self.headerBar.pack_end(self.menuButton)
        # add a box to the Menu
        self.menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing)
        self.popover.set_child(self.menuBox)
        # add Menu Items
        self.folderChooser = Gtk.Button(label='Select Board', has_frame=False)
        self.folderChooser.connect('clicked', self.folderClicked)
        # self.menuBox.append(self.folderChooser)
        self.about = Gtk.Button(label='About', has_frame=False)
        self.about.connect('clicked', self.aboutClicked)
        self.menuBox.append(self.about)

        # Ticket Boxes
        self.columnWidth = 100
        self.ticketBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=self.spacing, homogeneous=True)
        self.ticketScroll.set_child(self.ticketBox)
        self.idea = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.idea.set_size_request(self.columnWidth, -1)
        self.ticketBox.append(self.idea)
        self.todo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.todo.set_size_request(self.columnWidth, -1)
        self.ticketBox.append(self.todo)
        self.doing = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.doing.set_size_request(self.columnWidth, -1)
        self.ticketBox.append(self.doing)
        self.stopped = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.stopped.set_size_request(self.columnWidth, -1)
        self.ticketBox.append(self.stopped)
        self.done = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.done.set_size_request(self.columnWidth, -1)
        self.ticketBox.append(self.done)

        # Title of Ticket Categories
        self.ideaLabel = Gtk.Label(hexpand=True)
        self.ideaLabel.set_markup('<big><b>Idea</b></big>')
        self.todoLabel = Gtk.Label(hexpand=True)
        self.todoLabel.set_markup('<big><b>To Do</b></big>')
        self.doingLabel = Gtk.Label(hexpand=True)
        self.doingLabel.set_markup('<big><b>Doing</b></big>')
        self.stoppedLabel = Gtk.Label(hexpand=True)
        self.stoppedLabel.set_markup('<big><b>Stopped</b></big>')
        self.doneLabel = Gtk.Label(hexpand=True)
        self.doneLabel.set_markup('<big><b>Done</b></big>')

        self.titleBox.append(self.ideaLabel)
        self.ideaLabel.set_size_request(self.columnWidth, -1)
        self.titleBox.append(self.todoLabel)
        self.todoLabel.set_size_request(self.columnWidth, -1)
        self.titleBox.append(self.doingLabel)
        self.doingLabel.set_size_request(self.columnWidth, -1)
        self.titleBox.append(self.stoppedLabel)
        self.stoppedLabel.set_size_request(self.columnWidth, -1)
        self.titleBox.append(self.doneLabel)
        self.doneLabel.set_size_request(self.columnWidth, -1)

        # finally loads the Tickets for the first time
        self.getTickets()

    def tester(self, widget):
        pass

    def boardChanged(self, widget):
        app.setConfig("Current Board", widget.get_active_text())
        self.reloadTickets()

    def addBoards(self):
        boards = app.getBoards()
        for board in boards:
            self.boardChooser.append_text(board)
        self.boardChooser.set_active(boards.index(app.readConfig("Current Board")))

    def closeDetails(self, widget):
        self.detailBox.remove(widget.get_parent().get_parent().get_parent())
        if self.detailBox.get_first_child() == None:
            self.mainBox.remove(self.detailScroll)

    def openDetails(self, widget):
        if self.detailScroll.get_parent() == None:
            self.mainBox.append(self.detailScroll)
        file = widget.get_parent().get_parent().get_parent().get_name()
        content = app.getTicketContent(file)
        self.ticketDetails = ticketDetails(file, content['Title'], content['Topic'], content['Effort'],
                                           content['Priority'], content['Position'], content['Description'])
        self.detailBox.append(self.ticketDetails.frame)
        self.ticketDetails.status.connect('changed', self.moveTicket)
        self.ticketDetails.close.connect('clicked', self.closeDetails)

    def moveTicket(self, widget):
        self.category = widget.get_active_text()
        self.ticket = widget.get_parent().get_parent().get_parent()
        app.editTicket(self.ticket.get_name(), 'Position', self.category)
        if self.ticket.get_parent().get_parent() == self.ticketBox:
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
                if section == self.detailScroll:
                    for child in self.detailBox:
                        if child.get_name() == self.ticket.get_name():
                            self.closeDetails(child.get_first_child().get_first_child().get_first_child())
                            self.openDetails(self.ticket.get_first_child().get_first_child().get_first_child())
        else:
            self.reloadTickets()

    # opens dialog to choose folder to look in
    def folderClicked(self, widget):
        dialog = Gtk.FileChooserDialog(title='Select a Folder', action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.set_transient_for(self)
        dialog.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
        dialog.connect('response', self.on_dialog_response)
        dialog.show()

    def on_dialog_response(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            app.setConfig('Location of Tickets', widget.get_file().get_path())
            self.reloadTickets()
        widget.destroy()

    def getTickets(self):
        files = app.getTickets()
        for file in files:
            content = app.getTicketContent(file)
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
            self.newticket.status.connect('changed', self.moveTicket)
            self.newticket.titleButton.connect('clicked', self.openDetails)

    def reloadTickets(self):
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
        self.getTickets()

    # creates new Ticket
    def newTicket(self, widget):
        dialog = ticketDialog(self)
        dialog.connect('response', self.on_ticket_response)

    def on_ticket_response(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            desc = widget.description.get_buffer().get_text(widget.description.get_buffer().get_start_iter(),
                                                            widget.description.get_buffer().get_end_iter(), False)
            app.createTicket(widget.title.get_text(), widget.topic.get_text(), widget.effort.get_text(),
                             widget.priority.get_text(), desc)
            self.reloadTickets()
        widget.destroy()

    def aboutClicked(self, widget):
        self.dialog = Gtk.AboutDialog(authors=['UnicornyRainbow'], artists=['UnicornyRainbow'],
                                      comments='Organize your work in a local and agile kanban board.',
                                      license_type=Gtk.License.GPL_3_0_ONLY, program_name='Organizer', version='1.0.0',
                                      website_label='Website', website='https://unicornyrainbow.github.io/Organizer/')
        self.dialog.set_logo_icon_name('organizer')
        self.dialog.show()
