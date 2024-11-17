import streamlit as st
from predibase import Predibase, FinetuningConfig, DeploymentConfig
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API token from environment variables
api_key = os.getenv('PREDIBASE_API_TOKEN')

# Initialize Predibase API client with the API token
pb = Predibase(api_token=api_key)

# Streamlit app UI
st.title("AI Teacher Assistant")

# Input fields for user customization
adapter_id = st.text_input("Enter adapter ID:", value="조교ai/1")
deployment_id = st.text_input("Enter deployment ID:", value="solar-pro-preview-instruct")
api_key = st.text_input("Enter API Key:", value=api_key)
max_new_tokens = st.slider("Select max new tokens:", 1, 4096, 100)
temperature = st.slider("Select temperature:", 0.0, 1.0, 0.1)
user_input = st.text_area("Enter your question:")

# Function to generate a response using Predibase
def generate_response(user_input, deployment_id, adapter_id, max_new_tokens, temperature, api_key):
    try:
        pb = Predibase(api_token=api_key)
        lorax_client = pb.deployments.client(deployment_id)
        response = lorax_client.generate(user_input, adapter_id=adapter_id, max_new_tokens=max_new_tokens, temperature=temperature)
        return response.generated_text.split(":")[1]
    except Exception as e:
        return f"Error: {str(e)}"

# When the user submits input
if st.button('Ask'):
    if user_input:
        with st.spinner("Generating response..."):
            response = generate_response(user_input, deployment_id, adapter_id, max_new_tokens, temperature, api_key)
        st.write("AI Response:")
        st.write(response)
    else:
        st.write("Please enter some text.")
