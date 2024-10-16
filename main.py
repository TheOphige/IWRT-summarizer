import streamlit as st
from utils import save_uploaded_file, summarize_pdf


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
    file_path = save_uploaded_file(uploaded_file)
    
    with st.spinner("Processing the PDF..."):
        # Summarize the PDF
        try:

            summaries = summarize_pdf(file_path)

            st.header("Chapter Summaries")
            # Display the summaries in Streamlit
            for chapter_title, summary in summaries.items():
                with st.expander(chapter_title):
                    st.write(summary)

            st.write("I'm done Summarizing your Highness👑")
            st.info("\n That's just for three chapters, i stopped there because of rate limit. To summarise every chapter, contact my creator :)")

        except:
            st.error("Something is wrong, Check your network and retry.😫")

