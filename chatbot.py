import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

# Configure environment for API access
os.environ["OPENAI_API_KEY"] = getpass.getpass(prompt='Enter OpenAI API Key: ')

# Initialize the language model
model = ChatOpenAI(model="gpt-3.5-turbo")
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
     MessagesPlaceholder(variable_name="messages"),]
)
chain = prompt | model
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)
chain_with_history = RunnableWithMessageHistory(
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | chain,
    get_session_history,
    input_messages_key="messages",
)

def chat_with_bot(session_id, user_input):
    config = {"configurable": {"session_id": session_id}}
    response = chain_with_history.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config,
    )
    return response.content
