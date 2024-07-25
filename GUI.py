import tkinter as tk
from tkinter import Frame, Scrollbar, Text, Entry, Button, Menu
import threading
from chatbot import chat_with_bot

class ChatInterface(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.session_id = "session123"
        self.init_window()

    def init_window(self):
        self.master.title("ChatBot")
        self.master.config(bg='#2C2C2C')

        menu = Menu(self.master)
        self.master.config(menu=menu)
        theme_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Dark", command=lambda: self.change_theme('#333333', '#FFFFFF'))
        theme_menu.add_command(label="Light", command=lambda: self.change_theme('#FFFFFF', '#000000'))

        self.text_frame = Frame(self.master, bg='#2C2C2C')
        self.text_frame.pack(expand=True, fill='both')

        self.scrollbar = Scrollbar(self.text_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.text_box = Text(self.text_frame, yscrollcommand=self.scrollbar.set, state='disabled', wrap='word',
                             bg='#333333', fg='#FFFFFF', font='Verdana 10')
        self.text_box.pack(expand=True, fill='both')
        self.scrollbar.config(command=self.text_box.yview)

        self.entry_frame = Frame(self.master, bg='#2C2C2C')
        self.entry_frame.pack(fill='x', ipady=5)

        self.entry_field = Entry(self.entry_frame, bg='#333333', fg='#FFFFFF', insertbackground='#FFFFFF', font='Verdana 10')
        self.entry_field.pack(fill='x', padx=10, pady=10)
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = Button(self.entry_frame, text="Send", command=self.send_message, font='Verdana 10 bold',
                                  bg='#555555', fg='#FFFFFF', relief='flat')
        self.send_button.pack(side='right', padx=10, pady=10)

    def change_theme(self, bg_color, text_color):
        self.text_frame.config(bg=bg_color)
        self.text_box.config(bg=bg_color, fg=text_color)
        self.entry_frame.config(bg=bg_color)
        self.entry_field.config(bg=bg_color, fg=text_color, insertbackground=text_color)
        self.send_button.config(bg='#555555', fg=text_color)

    def send_message(self, event=None):
        message = self.entry_field.get()
        if message:
            self.update_chat(f"You: {message}\n", 'user')
            self.entry_field.delete(0, 'end')
            self.display_typing_indicator()
            threading.Thread(target=self.get_response, args=(message,)).start()

    def display_typing_indicator(self):
        self.update_chat("Bot is typing...\n", 'typing')
        self.text_box.after(500, lambda: self.text_box.delete('end-1c linestart', 'end'))

    def get_response(self, message):
        response = chat_with_bot(self.session_id, message)
        self.text_box.delete('end-1c linestart', 'end')
        formatted_response = f"Bot: {response}\n"
        self.update_chat(formatted_response, 'bot')

    def update_chat(self, message, sender):
        self.text_box.config(state='normal')
        self.text_box.insert('end', message)
        self.text_box.config(state='disabled')
        self.text_box.yview('end')

root = tk.Tk()
app = ChatInterface(root)
app.pack(expand=True, fill='both')
root.mainloop()
