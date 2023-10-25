import time
import requests
from decouple import config
import streamlit as st

# Read API key and API URL from .env file
api_key = config('API_KEY')
api_base = config('API_BASE')

st.title("Dalle -E OpenAI Image Generator (Streamlit)")

# Step 1: Submit the image generation job
def post_call(prompt):
    url = f"{api_base}/openai/images/generations:submit?api-version=2023-06-01-preview"

    headers = {
        'Content-Type': 'application/json',
        'api-key': f'{api_key}',
    }

    data = {
        'prompt': prompt,
        'size': "512x512",
        'n': 1,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 202:
        return response.json()["id"]  # returns image id
    else:
        return None

# Step 2: Check the job status and get the result
def get_call(operation_id):
    url = f"{api_base}/openai/operations/images/{operation_id}?api-version=2023-06-01-preview"

    headers = {
        'api-key': f'{api_key}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["result"]["data"][0]["url"]
    else:
        return None

# Streamlit UI
prompt = st.text_input("Enter your prompt:")
generate_button = st.button("Generate Image")

if generate_button:
    st.write("Generating image...")
    operation_id = post_call(prompt)

    if operation_id:
        progress_bar = st.empty()  # Create a placeholder for the progress bar
        for i in range(101):
            progress_bar.progress(i)
            time.sleep(1)

        # Step 2: Check the job status and get the result
        generated_image_url = get_call(operation_id)

        if generated_image_url:
            st.image(generated_image_url, caption="Generated Image", use_column_width=True)
        else:
            st.error("Failed to retrieve the generated image.")
    else:
        st.error("Failed to submit the image generation job.")
