import streamlit as st
import io
from utils import summarize_pdf


st.set_page_config(
    page_title="IWRT-Summarizer",
    page_icon="👨‍🦯",
)


# Main Page
# st.sidebar.image("assets/IWTR-LOGO.png", width=240)
st.title("IWTR - Book Summarizer👨‍🦯")
st.write("Upload a PDF book with table of content, and this app will provide a summary of each chapter.")


# File uploader and summarization trigger
uploaded_file = st.file_uploader("Choose a PDF book file", type="pdf")
if uploaded_file is not None:
    # Create a byte stream from the uploaded file
    pdf_stream = io.BytesIO(uploaded_file.getvalue())
    

    with st.spinner("Processing the PDF..."):
        # Summarize the PDF
        try:

            summaries = summarize_pdf(pdf_stream)

            st.header("Chapter Summaries")
            # Display the summaries in Streamlit
            for chapter_title, summary in summaries.items():
                with st.expander(chapter_title):
                    st.write(summary)

            st.write("I'm done Summarizing your Highness👑")
            st.info("\n That's just for three chapters. I stopped there because of rate limit. \nTo summarise every chapter, contact my creator :)")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Something is wrong, Check your network and retry.😫")

