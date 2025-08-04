# main.py
import customtkinter as ctk
import sys
from chatbot import Chatbot
from gui import ChatInterface
from config import load_api_key

class App(ctk.CTk):
    def __init__(self, chatbot: Chatbot):
        super().__init__()
        
        self.title("AI Chatbot")
        self.geometry("600x600")
        self.minsize(400, 500)

        # The chat interface now handles its own layout and header
        self.chat_interface = ChatInterface(self, chatbot=chatbot)

def main():
    """Main function to initialize and run the application."""
    api_key = load_api_key()
    root = None
    if not api_key:
        root = ctk.CTk()
        root.withdraw()
        dialog = ctk.CTkInputDialog(text="Please enter your OpenAI API Key or set it in the .env file as OPENAI_API_KEY:", title="API Key Required")
        api_key = dialog.get_input()
        if not api_key:
            print("No API key provided. Exiting.")
            root.destroy()
            sys.exit(1)
    else:
        root = ctk.CTk()
        root.withdraw()
    while True:
        try:
            chatbot = Chatbot(api_key=api_key)
            break
        except ValueError:
            dialog = ctk.CTkInputDialog(
                text="Invalid API key or connection error. Please check your key and try again.",
                title="Initialization Failed"
            )
            api_key = dialog.get_input()
            if not api_key:
                print("No valid API key provided. Exiting.")
                root.destroy()
                sys.exit(1)
    if root is not None:
        root.destroy()
    app = App(chatbot=chatbot)
    app.mainloop()

if __name__ == "__main__":
    main()