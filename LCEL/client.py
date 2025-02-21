import requests
import streamlit as st

def get_groq_response(input_text):
    json_body = { 
        "input": {
            "language": "Hindi",
            "text": input_text
        },
        "config": {},
        "kwargs": {}
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chain/invoke",
            json=json_body
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return {}
    except ValueError:
        st.error("Failed to parse JSON response")
        return {}

# Streamlit interface


st.title("LLM Application Using LCEL")
input_text = st.text_input("Enter the text you want to convert to French")

if input_text:
    response = get_groq_response(input_text)
    
    if response:
        st.subheader("Translation Result:")
        
        # Extract translated text from the response structure
        translated_text = response.get('output', '')
        metadata = response.get('metadata', {})
        
        if translated_text:
            # Clean up the response formatting
            cleaned_text = translated_text.split("Let me know")[0].strip()
            st.success(f"**Translation:** {cleaned_text}")
            
            # Optional: Display metadata
            with st.expander("Show Metadata"):
                st.json(metadata)
        else:
            st.error("No translation found in response")