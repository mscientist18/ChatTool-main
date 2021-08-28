import socket
import threading
from tkinter import *
from tkinter import messagebox

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.name_widget = None
        self.room_id = None
        self.chat_area = None
        self.join_button = None
        self.send_button = None
        self.conn = None
        self.init_connection()
        self.init_GUI()

    def init_connection(self):
        self.conn = socket.socket()
        self.conn.connect(('localhost', 12345))

    def init_GUI(self):
        self.root.title("Chat Application")
        self.username_display()
        self.room_display()
        self.chat_box_display()
        self.chat_entry_display()

    def username_display(self):
        frame = Frame()
        Label(frame, text='Enter your Username:', font=("Serif", 16)).pack(side='left', padx=10)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
        frame.pack(side='top', anchor='nw')
    
    def room_display(self):
        frame = Frame()
        Label(frame, text='Enter Room ID to join:', font=("Serif", 16)).pack(side='left', padx=10)
        self.room_id = Entry(frame, width=50, borderwidth=2)
        self.room_id.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Join", width=10, command=self.client_join).pack(side='left')
        frame.pack(side='top', anchor='nw')

    def chat_box_display(self):
        frame = Frame()
        Label(frame, text='Messages:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_details_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_details_area.yview, orient=VERTICAL)
        self.chat_details_area.config(yscrollcommand=scrollbar.set)
        self.chat_details_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_details_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')
    
    def chat_entry_display(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w', padx=65)
        self.enter_text_widget = Text(frame, width=50, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', padx=65)
        self.send_button = Button(frame, text="Send", width=10, command=self.send_message).pack(side='left', anchor='nw')
        frame.pack(side='top')

    def client_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Error")
            return
        credentials = (self.name_widget.get() + '+' + self.room_id.get()).encode('utf-8')
        self.conn.send((credentials))
        self.name_widget.config(state = 'disabled')
        self.room_id.config(state = 'disabled')
        recieve_thread = threading.Thread(target = self.recieve_msg_server, args = ())
        recieve_thread.start()
        send_thread = threading.Thread(target = self.send_message, args = ())
        send_thread.start()

    def recieve_msg_server(self):
        while True:
            try:
                msg = self.conn.recv(4096).decode('utf-8')
                print(msg)
                if not msg:
                    break
                self.chat_details_area.insert('end', msg)
                self.chat_details_area.yview(END)
            except:
                print("Error")
                break
        self.conn.close()

    def send_message(self):
        if len(self.name_widget.get()) == 0 or len(self.room_id.get()) == 0:
            messagebox.showerror("Error")
            return
        if len(self.enter_text_widget.get(1.0, 'end')) == 0:
            messagebox.showerror("Error")
        username = self.name_widget.get() + ": "
        actual_msg = self.enter_text_widget.get(1.0, 'end')
        total_msg = (username + actual_msg).encode('utf-8')
        #print(len(actual_msg))
        #print(actual_msg, total_msg)
        if len(actual_msg) != 1:
            self.chat_details_area.insert('end', total_msg.decode('utf-8'))
            self.chat_details_area.yview(END)
            self.conn.send(total_msg)
            self.enter_text_widget.delete(1.0, 'end')


if __name__ == "__main__":
    root = Tk()
    gui_obj = ClientGUI(root)
    root.mainloop()