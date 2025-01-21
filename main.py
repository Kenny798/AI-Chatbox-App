import requests
import json
import streamlit as st
import os

# Streamlit automatically handles secrets, so no need for dotenv

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "b1d0b075-93a0-4a76-96d8-4ebddd02017d"
FLOW_ID = "dcf9c611-857d-493a-b822-aa8d0a2437cd"
APPLICATION_TOKEN = st.secrets["APP_TOKEN"]  # Access token from Streamlit secrets
ENDPOINT = "default"

# API function
def run_flow(message: str, input_type: str = "chat", output_type: str = "chat") -> dict:
    """Run a LangFlow using the API."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}?stream=false"

    payload = {
        "input_value": message,
        "input_type": input_type,
        "output_type": output_type,
    }
    
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

# Streamlit App
def main():
    st.title("🤖 Chat Interface") 

    message = st.text_input("💬 Ask Something")  # 

    # Button to run the flow
    if st.button("🚀 Answer"):  
        if not message.strip():
            st.error("⚠️ Please enter a valid message.")  
            return
        
        try:
            with st.spinner("⏳ Running Flow..."):  
                response = run_flow(message)
            
            # Extract response text safely
            try:
                response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No response text.")
                st.markdown(f"✅ **Response:** {response_text}")  # Emoji added to the response label
            except Exception as e:
                st.error("❌ Invalid response structure from the API.")  # Emoji added to the error message
        except Exception as e:
            st.error(f"❌ Error: {e}")  # Emoji added to the general error message

if __name__ == "__main__":
    main()
