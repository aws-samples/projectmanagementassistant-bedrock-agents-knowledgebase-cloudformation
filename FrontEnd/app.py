import boto3
from botocore.exceptions import ClientError
import time
import streamlit as st
import json
import base64

from agent import get_bedrock_agent_response

REGION = "To be replaced with region from CF stack output"
st.set_page_config(page_title="Resource Management Assistant", layout="wide") 
st.title("Resource Management Assistant") 

bedrock = boto3.client('bedrock-runtime', region_name=REGION)

if "messages" not in st.session_state:
    st.session_state.messages = []
   
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
       # message_placeholder = st.empty()
        full_response = ""
        kbase_response = get_bedrock_agent_response(prompt)
        # Display assistant response in chat message container
        st.markdown(kbase_response)

    st.session_state.messages.append({"role": "assistant", "content": kbase_response})
        
    


