import streamlit as st
from utils import save_uploaded_file, summarize_pdf


st.set_page_config(
    page_title="IWRT-Summarizer",
    page_icon="🧨",
    layout="wide",
)


# Main Page
st.image("assets/IWTR-LOGO.png", width=300)
st.title("Welcome to IWTR")

# select summarize mode
st.sidebar.title("Royal commands👑")
summarize_mode = st.sidebar.radio("Select Mode", ["Text Summarize", "Reimagine"])

# info
st.sidebar.write("---")
st.sidebar.info("Upload a PDF book, and this app will provide a summary of each chapter using LangChain.")

# Handle selection
if summarize_mode == "Text Summarize":
    st.header(f"{summarize_mode} selected! Words are better few.")
elif summarize_mode == "Reimagine":
    st.header(f"{summarize_mode} selected! One image is more than a thousand words.")



# File uploader and summarization trigger
uploaded_file = st.file_uploader("Choose a PDF book file", type="pdf")
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    
    with st.spinner("Processing the PDF..."):
        # Summarize the PDF
        if summarize_mode == "Text Summarize":
            summaries = summarize_pdf(file_path)
        elif summarize_mode == "Reimagine":
            summaries = summarize_pdf(file_path)

        st.header("Chapter Summaries")
        # Display the summaries in Streamlit
        for chapter_title, summary in summaries.items():
            with st.expander(chapter_title):
                st.write(summary)

        st.write("I'm done Summarizing your Highness👑")

