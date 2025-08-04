# chatbot.py
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from openai import OpenAIError

class Chatbot:
    """
    A chatbot class that encapsulates the LangChain logic for a conversation.
    """
    def __init__(self, api_key: str):
        """
        Initializes the Chatbot with an OpenAI API key.

        Args:
            api_key (str): The OpenAI API key.
        
        Raises:
            ValueError: If the API key is invalid or an authentication error occurs.
        """
        try:
            self.model = ChatOpenAI(model="gpt-4o", openai_api_key=api_key)
            # Test the key by making a small call
            self.model.invoke([HumanMessage(content="test")])
        except OpenAIError as e:
            raise ValueError(f"Invalid API Key or connection error: {e}") from e

        self.store = {}
        
        # A more conversational and friendly prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a friendly and helpful AI assistant. Answer questions in a conversational and concise manner."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])

        self.runnable = prompt | self.model

        self.chain = RunnableWithMessageHistory(
            self.runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        """
        Retrieves the chat history for a given session ID.
        """
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def get_response(self, user_input: str, session_id: str) -> str:
        """
        Gets a response from the chatbot for a given user input and session.

        Args:
            user_input (str): The input from the user.
            session_id (str): The unique ID for the current chat session.

        Returns:
            str: The chatbot's response or an error message.
        """
        if not user_input:
            return "Please enter a message."

        config = {"configurable": {"session_id": session_id}}
        
        try:
            # Add a welcome message on the first interaction of a session
            history = self.get_session_history(session_id)
            if not history.messages:
                # This could be a place to inject a welcome message, but we'll do it in the UI
                pass

            response = self.chain.invoke({"input": user_input}, config=config)
            return response.content
        except OpenAIError:
            return "Invalid API key or connection error. Please check your key and try again."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def start_new_session(self) -> str:
        """
        Starts a new chat session and returns a new session ID.
        """
        return str(uuid.uuid4())