#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

from backend import App
from more_ui import Ticket, TicketDialog, TicketDetails


class Window(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # app3 = self.get_application()
        # sm = app3.get_style_manager()

        self.spacing = 10

        # window
        Gtk.Window.__init__(self, title='Organizer')
        self.set_default_size(960, 540)

        # Define the General structure of the Window

        # Header Bar
        self.headerbar = Adw.HeaderBar()
        self.set_titlebar(self.headerbar)
        # self.headerBar.set_show_start_title_buttons(True)
        # self.headerBar.set_show_end_title_buttons(True)
        self.title = Gtk.Label()
        self.title.set_label('Organizer')
        self.headerbar.set_title_widget(self.title)

        # Setup general window Structure
        self.mainbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_child(self.mainbox)

        # Box for Ticket columns and Headers
        self.bigbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, margin_start=self.spacing,
                              margin_end=self.spacing, margin_top=self.spacing, margin_bottom=self.spacing)
        self.mainbox.append(self.bigbox)
        self.testbox = Gtk.ScrolledWindow()
        self.titlebox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=self.spacing)
        self.bigbox.append(self.titlebox)
        # Scrollable box for the tickets
        self.ticketscroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.bigbox.append(self.ticketscroll)

        # Box for Ticket Details
        self.detailscroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True, margin_start=self.spacing,
                                               margin_end=self.spacing, margin_top=self.spacing,
                                               margin_bottom=self.spacing)
        self.detailscroll.set_size_request(380, -1)
        self.detailbox = Gtk.Box(vexpand=True, hexpand=True, orientation=Gtk.Orientation.HORIZONTAL,
                                 spacing=self.spacing)
        self.detailscroll.set_child(self.detailbox)

        # Populate the Header Bar

        # Create new Ticket
        self.newbutton = Gtk.Button()
        self.newicon = Gtk.Image.new_from_icon_name("document-new-symbolic")
        self.newbutton.set_child(self.newicon)
        self.newbutton.connect('clicked', self.new_ticket)
        self.headerbar.pack_start(self.newbutton)

        self.boardchooser = Gtk.ComboBoxText()
        self.add_boards()
        self.boardchooser.connect("changed", self.board_changed)
        self.headerbar.pack_start(self.boardchooser)

        # Button to test functions
        self.testbutton = Gtk.Button(label='test')
        self.testbutton.connect('clicked', self.tester)
        self.headerbar.pack_start(self.testbutton)

        # Hamburger Menu
        # Popover and Button
        self.popover = Gtk.Popover(position=Gtk.PositionType.BOTTOM)
        self.menubutton = Gtk.MenuButton(popover=self.popover, icon_name="open-menu-symbolic", primary=True)
        self.headerbar.pack_end(self.menubutton)
        # add a box to the Menu
        self.menubox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing)
        self.popover.set_child(self.menubox)
        # add Menu Items
        # self.menuBox.append(self.folderChooser)
        self.about = Gtk.Button(label='About', has_frame=False)
        self.about.connect('clicked', self.about_clicked)
        self.menubox.append(self.about)

        # Ticket Boxes
        self.columnwidth = 100
        self.ticketbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=self.spacing, homogeneous=True)
        self.ticketscroll.set_child(self.ticketbox)
        self.idea = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.idea.set_size_request(self.columnwidth, -1)
        self.ticketbox.append(self.idea)
        self.todo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.todo.set_size_request(self.columnwidth, -1)
        self.ticketbox.append(self.todo)
        self.doing = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.doing.set_size_request(self.columnwidth, -1)
        self.ticketbox.append(self.doing)
        self.stopped = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.stopped.set_size_request(self.columnwidth, -1)
        self.ticketbox.append(self.stopped)
        self.done = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=self.spacing, hexpand=True)
        self.done.set_size_request(self.columnwidth, -1)
        self.ticketbox.append(self.done)

        # Title of Ticket Categories
        self.idealabel = Gtk.Label(hexpand=True)
        self.idealabel.set_markup('<big><b>Idea</b></big>')
        self.todolabel = Gtk.Label(hexpand=True)
        self.todolabel.set_markup('<big><b>To Do</b></big>')
        self.doinglabel = Gtk.Label(hexpand=True)
        self.doinglabel.set_markup('<big><b>Doing</b></big>')
        self.stoppedlabel = Gtk.Label(hexpand=True)
        self.stoppedlabel.set_markup('<big><b>Stopped</b></big>')
        self.donelabel = Gtk.Label(hexpand=True)
        self.donelabel.set_markup('<big><b>Done</b></big>')

        self.titlebox.append(self.idealabel)
        self.idealabel.set_size_request(self.columnwidth, -1)
        self.titlebox.append(self.todolabel)
        self.todolabel.set_size_request(self.columnwidth, -1)
        self.titlebox.append(self.doinglabel)
        self.doinglabel.set_size_request(self.columnwidth, -1)
        self.titlebox.append(self.stoppedlabel)
        self.stoppedlabel.set_size_request(self.columnwidth, -1)
        self.titlebox.append(self.donelabel)
        self.donelabel.set_size_request(self.columnwidth, -1)

        # finally loads the Tickets for the first time
        self.get_tickets()

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

    def board_changed(self, widget: Gtk.ComboBoxText):
        App.set_config("Current Board", widget.get_active_text())
        self.reload_tickets()

    def close_details(self, widget):
        self.detailbox.remove(widget.get_parent().get_parent().get_parent())
        if self.detailbox.get_first_child() is None:
            self.mainbox.remove(self.detailscroll)

    def open_details(self, widget: Gtk.Button):
        if self.detailscroll.get_parent() is None:
            self.mainbox.append(self.detailscroll)
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
            for section in self.mainbox:
                if section == self.detailscroll:
                    for child in self.detailbox:
                        if child.get_name() == self.ticket.get_name():
                            self.close_details(child.get_first_child().get_first_child().get_first_child())
                            self.open_details(self.ticket.get_first_child().get_first_child().get_first_child())
        else:
            self.reload_tickets()

    # creates new Ticket
    def new_ticket(self, widget: Gtk.Button):
        dialog = TicketDialog(self)
        dialog.connect('response', self.on_ticket_response)

    def on_ticket_response(self, widget: TicketDialog, responseid):
        if responseid == Gtk.ResponseType.OK:
            desc = widget.description.get_buffer().get_text(widget.description.get_buffer().get_start_iter(),
                                                            widget.description.get_buffer().get_end_iter(), False)
            App.create_ticket(widget.title.get_text(), widget.topic.get_text(), widget.effort.get_text(), widget.priority.get_text(), desc)
            self.reload_tickets()
        widget.destroy()

    def about_clicked(self, widget: Gtk.Button):
        self.dialog = Gtk.AboutDialog(authors=['UnicornyRainbow'], artists=['UnicornyRainbow'],
                                      comments='Organize your work in a local and agile kanban board.',
                                      license_type=Gtk.License.GPL_3_0_ONLY, program_name='Organizer', version='1.0.0',
                                      website_label='Website', website='https://unicornyrainbow.github.io/Organizer/')
        self.dialog.set_logo_icon_name('io.github.unicornyrainbow.organizer')
        self.dialog.show()
