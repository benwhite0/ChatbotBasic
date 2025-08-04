# Modern Chatbot with Custom Tkinter GUI using Langchain

A sleek, adaptable chatbot application featuring a modern graphical interface, animated typing indicator, and dynamic theme switching. Designed for ease of use, demonstration, and extension for a variety of applications such as customer support, personal assistants, and educational tools.

## Features
- **Modern GUI:** Built with CustomTkinter for a clean, professional look and smooth user experience.
- **Animated Typing Indicator:** Shows when the bot is generating a response, enhancing interactivity.
- **Dynamic Theme Switching:** Instantly switch between Light and Dark modes; all chat bubbles and UI elements update accordingly.
- **OpenAI Integration:** Connects to OpenAI for intelligent, context-aware responses (requires your API key).
- **Easy Customisation:** Modular codebase allows for straightforward changes to appearance, behaviour, and features.

## Installation
1. Ensure you have Python 3.8+ installed.
2. Clone the repository:
   ```sh
   git clone https://github.com/benwhite0/ChatbotBasic.git
   cd ChatbotBasic
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```sh
   python main.py
   ```
2. Enter your OpenAI API key when prompted.
3. Type your message and press "Send" or hit Enter to chat.
4. Use the theme menu to switch between Light and Dark modes at any time.

## Customisation
- **Themes & Appearance:** Easily adjust colours and fonts in `gui.py`.
- **Bot Behaviour:** Modify or extend logic in `chatbot.py`.
- **Add Features:** The modular design allows for integration of new features such as voice input, advanced conversation memory, or external APIs.

## Licence
This project is open source and available under the MIT Licence.
