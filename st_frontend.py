import streamlit as st
from langchain_core.messages import HumanMessage

from langgraph_backend import chatbot        # importing out chatbot we made

CONFIG = {"configurable":{"thread_id":"1"}}



if "msg_history" not in st.session_state:
    st.session_state["msg_history"] = []             # a session i.e. a dictionary created
                                                    # key - "msg_history" which expects a list of messages 

#{'role': 'user', 'content': 'user query'}
#{'role': 'assistant', 'content': 'llm response to query'}


for msg in st.session_state['msg_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])


user_input = st.chat_input("Ask your chatbot")

if user_input:                                   # meaning when user hits "Enter" button.
# adding the message to message_history
    st.session_state["msg_history"].append({"role":"user",
                                            "content":user_input})
    with st.chat_message("user"):
        st.text(user_input)


    response = chatbot.invoke({"messages": [HumanMessage(user_input)]}, config=CONFIG)


    chatbot_response = response['messages'][-1].content
# add the message to message_history
    st.session_state["msg_history"].append({"role":"assistant",
                                           "content":chatbot_response})
    with st.chat_message("assistant"):
        st.text(chatbot_response)