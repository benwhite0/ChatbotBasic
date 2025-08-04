# gui.py
import customtkinter as ctk
import threading
from chatbot import Chatbot

# Define modern color palettes
class Colors:
    USER_BUBBLE = "#007AFF"      # A vibrant blue for the user
    BOT_BUBBLE_DARK = "#3a3a3a"
    BOT_BUBBLE_LIGHT = "#E5E5EA"
    ERROR_BUBBLE = "#FF3B30"      # A standard iOS-style error red

class ChatInterface(ctk.CTkFrame):
    """
    A modern graphical user interface for the chatbot with iMessage-style bubbles.
    """
    def __init__(self, master, chatbot: Chatbot):
        super().__init__(master)
        self.chatbot = chatbot
        self.session_id = self.chatbot.start_new_session()
        self.message_bubbles = []  # Store (bubble_frame, label, sender, is_error)
        
        self.pack(fill="both", expand=True)
        self._create_widgets()
        
        # --- DEFINITIVE FIX for the initial message bug ---
        # self.after_idle() schedules the function to run when the GUI is finished
        # with its initial layout and is idle, guaranteeing all widgets have a valid size.
        self.after_idle(self._add_bot_welcome_message)

    def _create_widgets(self):
        """Creates and configures the UI widgets."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        self.new_chat_button = ctk.CTkButton(header, text="New Chat", command=self.start_new_chat)
        self.new_chat_button.pack(side="left")

        title_label = ctk.CTkLabel(header, text="Chatbot Assistant", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(side="left", expand=True, padx=20)
        
        # Remove 'System' from theme options
        self.theme_menu = ctk.CTkOptionMenu(header, values=["Dark", "Light"], command=self._on_theme_change)
        self.theme_menu.pack(side="right")

        # --- Chat History (Scrollable Frame for Bubbles) ---
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # --- Message Entry Area ---
        input_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message...")
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry.bind("<Return>", self._on_send_message)
        
        self.send_button = ctk.CTkButton(input_frame, text="Send", command=self._on_send_message, width=70)
        self.send_button.grid(row=0, column=1, sticky="e")
    
    def _add_bot_welcome_message(self):
        """Adds the initial greeting from the bot."""
        welcome_message = "Hello! How can I assist you today?"
        self._add_message_bubble(welcome_message, "bot")

    def _on_send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self._add_message_bubble(user_input, "user")
        self.entry.delete(0, "end")
        
        self.entry.configure(state="disabled")
        self.send_button.configure(state="disabled")

        # Add typing indicator
        self._show_typing_indicator()

        threading.Thread(target=self._get_bot_response, args=(user_input,), daemon=True).start()

    def _get_bot_response(self, user_input: str):
        response = self.chatbot.get_response(user_input, self.session_id)
        self.after(0, self._update_ui_with_response, response)

    def _update_ui_with_response(self, response: str):
        # Remove typing indicator
        self._hide_typing_indicator()
        is_error = "An API error occurred" in response or "An unexpected error occurred" in response
        self._add_message_bubble(response, "bot", is_error=is_error)

        self.entry.configure(state="normal")
        self.send_button.configure(state="normal")
        self.entry.focus()
    
    def _add_message_bubble(self, message: str, sender: str, is_error: bool = False):
        if sender == "user":
            anchor = "e"
            color = Colors.USER_BUBBLE
            text_color = "white"
        else: # bot
            anchor = "w"
            if is_error:
                color = Colors.ERROR_BUBBLE
                text_color = "white"
            else:
                is_dark = ctk.get_appearance_mode().lower() == "dark"
                color = Colors.BOT_BUBBLE_DARK if is_dark else Colors.BOT_BUBBLE_LIGHT
                text_color = "white" if is_dark else "black"

        bubble_frame = ctk.CTkFrame(self.chat_frame, fg_color=color, corner_radius=15)
        bubble_frame.pack(anchor=anchor, padx=10, pady=4, expand=False)

        # This will now have the correct width because this function is called after idle.
        max_width = max(self.chat_frame.winfo_width() * 0.75, 300)  # 300 is a reasonable minimum
        
        message_label = ctk.CTkLabel(
            bubble_frame,
            text=message,
            text_color=text_color,
            wraplength=max_width,
            justify="left"
        )
        message_label.pack(padx=10, pady=6)
        
        self.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

        # Store reference for theme updates
        self.message_bubbles.append((bubble_frame, message_label, sender, is_error))

    def _update_all_bubble_colors(self):
        is_dark = ctk.get_appearance_mode().lower() == "dark"
        for bubble_frame, label, sender, is_error in getattr(self, "message_bubbles", []):
            if sender == "user":
                color = Colors.USER_BUBBLE
                text_color = "white"
            else:
                if is_error:
                    color = Colors.ERROR_BUBBLE
                    text_color = "white"
                else:
                    color = Colors.BOT_BUBBLE_DARK if is_dark else Colors.BOT_BUBBLE_LIGHT
                    text_color = "white" if is_dark else "black"
            bubble_frame.configure(fg_color=color)
            label.configure(text_color=text_color)

    def _on_theme_change(self, mode):
        ctk.set_appearance_mode(mode)
        self._update_all_bubble_colors()
        # Also update typing indicator if present
        if hasattr(self, 'typing_indicator_bubble') and hasattr(self, 'typing_indicator_label'):
            is_dark = ctk.get_appearance_mode().lower() == "dark"
            color = Colors.BOT_BUBBLE_DARK if is_dark else Colors.BOT_BUBBLE_LIGHT
            text_color = "white" if is_dark else "black"
            self.typing_indicator_bubble.configure(fg_color=color)
            self.typing_indicator_label.configure(text_color=text_color)

    def start_new_chat(self):
        """Clears the chat history and starts a new session."""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
            
        self.session_id = self.chatbot.start_new_session()
        self._add_bot_welcome_message()
        self.message_bubbles.clear()

    def _show_typing_indicator(self):
        # Animated typing indicator for the bot
        self.typing_indicator_running = True
        self.typing_indicator_bubble = ctk.CTkFrame(self.chat_frame, fg_color=Colors.BOT_BUBBLE_DARK if ctk.get_appearance_mode().lower() == "dark" else Colors.BOT_BUBBLE_LIGHT, corner_radius=15)
        self.typing_indicator_bubble.pack(anchor="w", padx=10, pady=4, expand=False)
        self.typing_indicator_label = ctk.CTkLabel(self.typing_indicator_bubble, text="", text_color="white" if ctk.get_appearance_mode().lower() == "dark" else "black", font=ctk.CTkFont(size=13, slant="italic"))
        self.typing_indicator_label.pack(padx=10, pady=6)
        self._animate_typing_indicator()

    def _animate_typing_indicator(self):
        if not getattr(self, 'typing_indicator_running', False):
            return
        dots = getattr(self, 'typing_indicator_dots', 0)
        self.typing_indicator_label.configure(text="Typing" + "." * (dots % 4))
        self.typing_indicator_dots = (dots + 1) % 4
        self.after(400, self._animate_typing_indicator)

    def _hide_typing_indicator(self):
        self.typing_indicator_running = False
        if hasattr(self, 'typing_indicator_bubble'):
            self.typing_indicator_bubble.destroy()
            del self.typing_indicator_bubble
        self.typing_indicator_dots = 0