from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages          # Reducer function.
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langchain_perplexity import ChatPerplexity


from dotenv import load_dotenv
load_dotenv()




# Initializing LLModel instance
llm_model = ChatPerplexity()

# Memory saver object
checkpointer = InMemorySaver()

# Defining state for our chatbot
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]      # gonna store HumanMsg and AIMsg



# Define the only task in the entire workflow: [START ---> chat_node ---> END]
def chat_node(state:ChatState):

    messages = state['messages']                     # take user input i.e. HumanMsg or previous chat history 

    llm_response = llm_model.invoke(messages)        # call llm to respond to the human-msg
    
    return {"messages": llm_response}                # update the state value with new response
 


# Graph - workflow
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)