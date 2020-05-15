import socket
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

"""
class Network():
    def __init__(self, gui):
        
    # Define sending function
    def send(self, msg):
        msg = msg.encode('utf-8')
        msg_len = len(msg)
        self.s.send((f"{msg_len:< {self.HEADER}}").encode('utf-8'))
        self.s.send(msg)

        # set up a tread for listening to the server
    def recieve(self):
        msg = self.s.recv(100).decode('utf-8')
        self.gui.tv.set_text(msg + "\n")

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        thread = threading.Thread(target=self.recieve)
        thread.start()
"""

class Messenger(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Messenger")
        self.box = Gtk.Box(orientation='vertical', spacing=2)
        self.btn_box = Gtk.Box(orientation='horizontal', spacing=2)
        self.strg = ""

        self.my_title = Gtk.Label(label='Messenger')
        self.text = Gtk.Entry()
        self.send_btn = Gtk.Button(label='Send', expand=True)
        self.clear = Gtk.Button(label='Clear', expand=True)
        self.tv = Gtk.TextView()

        self.text_buffer = self.tv.get_buffer()
        self.tv.set_size_request(-1, 300)
        self.tv.set_wrap_mode(Gtk.WrapMode.WORD)

        self.send_btn.connect("clicked", self.enter_or_clear)
        self.clear.connect("clicked", self.enter_or_clear)

        self.btn_box.add(self.send_btn)
        self.btn_box.add(self.clear)

        self.box.add(self.my_title)
        self.box.add(self.text)
        self.box.add(self.btn_box)
        self.box.add(self.tv)
        self.add(self.box)

        # The Network
         # Network Constants
        self.HOST = '192.168.1.22'
        self.PORT = 1234
        self.HEADER = 10
        self.DISCONNECT_MSG = '!DISCONNECT'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.thread = threading.Thread(target=self.recieve)
        self.thread.start()
    
    def recieve(self):
        while True:
            msg = self.s.recv(100).decode('utf-8')
            self.strg = self.strg + msg + "\n"
            self.text_buffer.set_text(self.strg)
            print("Got another message: " + msg)
    
    def sendmsg(self, msg):
        print(msg)
        msg = msg.encode('utf-8')
        msg_len = len(msg)
        self.s.send((f"{msg_len:< {self.HEADER}}").encode('utf-8'))
        self.s.send(msg)
    
    def enter_or_clear(self, widget):
        res = widget.get_property("label")
        if res == 'Send':
            self.sendmsg(self.text.get_text())
        else:
            self.text_buffer.set_text("")

win = Messenger()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()