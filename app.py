import streamlit as st  
import requests  
import PyPDF2  
import io  
from PIL import Image  
import pytesseract  
import pdf2image  
  
# Function to extract insights using the Phi-3.5-Vision  
def extract_insights_phi_vision(pdf_data):  
    endpoint = "https://phi-test-2-ilewd.eastus2.inference.ml.azure.com/score"  
    headers = {  
        'Content-Type': 'application/json',  
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjdBNDFBNjY3MkFBRUZDNTM4Q0YxRTE2M0I5QzE1QzA1Qjk3MjcyRTgiLCJ0eXAiOiJKV1QifQ.eyJjYW5SZWZyZXNoIjoiRmFsc2UiLCJ3b3Jrc3BhY2VJZCI6IjQxZDEwYTVkLTBkZTEtNDA2MC04N2MzLTIxNjg1OWEwNWY3NyIsInRpZCI6IjRkNDM0M2M2LTA2N2EtNDc5NC05MWYzLTVjYjEwMDczZTViNCIsIm9pZCI6ImQ5ODU1ODc1LTExODAtNGFhMC1hNjU1LTU4Nzg1NWNkYzM3ZSIsImFjdGlvbnMiOiJbXCJNaWNyb3NvZnQuTWFjaGluZUxlYXJuaW5nU2VydmljZXMvd29ya3NwYWNlcy9vbmxpbmVFbmRwb2ludHMvc2NvcmUvYWN0aW9uXCJdIiwiZW5kcG9pbnROYW1lIjoicGhpLXRlc3QtMi1pbGV3ZCIsInNlcnZpY2VJZCI6InBoaS10ZXN0LTItaWxld2QiLCJleHAiOjE3Mjk5NjM5MDEsImlzcyI6ImF6dXJlbWwiLCJhdWQiOiJhenVyZW1sIn0.L2K7Sdc9Y1V1KNbE7fwO3Y2XGPubQ-cVA_-DCKoGewEM9fx3UrHL9G4yTXTc8_AG3YppIIIkun5e_S1mRsItBMzRb5efbV8kHZ62denGtw2ur8gmAixPhSx-YdmNXyYHVkjiE88oau9mi9cfcgtIXBB627Rz5FdUdPtTLCoRV8FY3ggp7EhzT9t0U2JbDZV7AWfgu5zhAExctThAnOCcmveQR3nuo-KwyUjJrHnmMbxp0tkAjAH8YOLo0dj7tFrm7UixXcK0EVBAVru24mRgPI6o8e65HLkU3cVjSlc4nbFp6w0chfSvl35CZWYd8fdObgpuUkAfk3zdbKjQQsJQoA'  
    }  
  
    insights = []  
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))  
    for page_num, page in enumerate(pdf_reader.pages):  
        page_text = page.extract_text()  
  
        # If text is not extracted, use OCR  
        if not page_text.strip():  
            st.write(f"Using OCR for Page {page_num + 1}")  
            images = pdf2image.convert_from_bytes(pdf_data, first_page=page_num+1, last_page=page_num+1)  
            page_text = ''  
            for image in images:  
                page_text += pytesseract.image_to_string(image)  
  
        data = {  
            "messages": [  
                {"role": "system", "content": "Extract essential text and image insights:"},  
                {"role": "user", "content": f"Text: {page_text}"}  
            ]  
        }  
          
        # Log the request data  
        st.write(f"Request Data for Page {page_num + 1}:", data)  
  
        try:  
            response = requests.post(endpoint, headers=headers, json=data)  
            response.raise_for_status()  
  
            # Debug: Print the full response  
            st.write(f"Response for Page {page_num + 1}:", response.json())  
  
            # Extract and store the content  
            response_data = response.json()  
            content = response_data.get('message', {}).get('content', 'No content found')  
            insights.append((page_num + 1, content))  
  
        except requests.exceptions.RequestException as e:  
            st.error(f"Error on page {page_num + 1}: {str(e)}")  
    return insights  
  
# Streamlit App  
st.title("PDF Insight Extraction App")  
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")  
  
if uploaded_file is not None:  
    pdf_data = uploaded_file.read()  
  
    with st.spinner("Extracting insights using Phi-3.5-Vision..."):  
        insights_phi = extract_insights_phi_vision(pdf_data)  
  
        # Display the insights for each page  
        for page_num, content in insights_phi:  
            st.write(f"### Insights for Page {page_num}")  
            st.write(content)  
