import streamlit as st
import requests
import base64
from io import BytesIO

# FastAPI server URL
API_URL = "http://127.0.0.1:8000/process_uploaded_file/"

def display_visualization(image_base64):
    """Displays base64-encoded image."""
    st.image(image_base64, use_column_width=True)

def upload_file(file):
    """Send file to FastAPI for processing."""
    try:
        # Prepare the request
        files = {'file': (file.name, file, file.type)}
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            result = response.json()
            # Display insights
            insights = result.get("insights", {})
            st.write(f"Number of rows: {insights.get('num_rows')}")
            st.write(f"Number of columns: {insights.get('num_columns')}")
            st.write(f"Column Names: {insights.get('column_names')}")
            st.write(f"Missing Values: {insights.get('missing_values')}")

            # Display visualizations (base64 images)
            visualizations = result.get("visualizations", {})
            for key, base64_image in visualizations.items():
                st.subheader(key.replace("_", " ").title())
                display_visualization(f"data:image/png;base64,{base64_image}")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("Data Insights with FastAPI and Streamlit")

    # File uploader
    file = st.file_uploader("Choose a CSV, Excel, or Text file", type=["csv", "xls", "xlsx", "txt"])
    
    if file:
        st.write("Uploading file...")
        upload_file(file)

if __name__ == "__main__":
    main()
