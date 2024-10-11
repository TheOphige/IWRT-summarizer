import os
import time
import streamlit as st
import fitz  # PyMuPDF
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from openai import RateLimitError
from dotenv import find_dotenv, load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv(find_dotenv())

# Set up Streamlit page configuration
st.set_page_config(page_title="PDF Chapter Summarizer", page_icon="📄")
st.title('PDF Book Chapter Summarizer')
st.write("Upload a PDF book, and this app will provide a summary of each chapter using LangChain.")

# Function to save uploaded file locally
def save_uploaded_file(uploaded_file):
    folder = 'uploads'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    return file_path

# Function to extract TOC and chapter content
def extract_toc_and_chapter_content(pdf_path):
    # Open the PDF document
    doc = fitz.open(pdf_path)

    # Extract TOC (Table of Contents)
    toc = doc.get_toc(simple=True)  # Format: [level, title, page_number]

    # Remove specified titles from TOC while not being case sensitive
    exclusion_terms = [
        "cover", 
        "other books by this author", 
        "title page", 
        "copyright", 
        "dedication", 
        "acknowledgments", 
        "photo insert", 
        "table of contents",
        "contents",
        "appendix",
        "bibliography",
        "index",
        "endnotes",
        "footnotes",
        "about the author"
    ]
    useful_toc = [item for item in toc if item[1].lower() not in exclusion_terms]
    
    # Create a dictionary to store chapter titles and their corresponding content
    chapters_content = {}

    # Iterate over TOC items
    for i, toc_item in enumerate(useful_toc):
        chapter_title = toc_item[1]  # Chapter title
        start_page_num = toc_item[2] - 1  # Starting page (PyMuPDF is zero-indexed)

        # Get the page number of the next chapter (or end of document)
        if i + 1 < len(toc):
            end_page_num = toc[i + 1][2] - 1  # Next chapter's starting page
        else:
            end_page_num = len(doc)  # Last chapter, so end at the last page

        # Extract text between the current chapter's start page and the next chapter's start page
        chapter_text = ""
        for page_num in range(start_page_num, end_page_num):
            page = doc.load_page(page_num)
            chapter_text += page.get_text()

        # Debugging: Display first 20 words and last 20 words
        words = chapter_text.split()
        first_20_words = " ".join(words[:20])
        last_20_words = " ".join(words[-20:])
        st.write(f"**{chapter_title}**")
        st.write(f"First 20 words: {first_20_words}")
        st.write(f"Last 20 words: {last_20_words}")
        st.write("---")  # Separator for better readability

        # Add to the dictionary
        chapters_content[chapter_title] = chapter_text.strip()  # Remove extra spaces

    # Close the document
    doc.close()

    return chapters_content


# Function to summarize a single chunk with retry mechanism on rate limit error
def summarize_with_retry(llm_chain, text, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            summary = llm_chain.run(text)
            return summary
        except RateLimitError as e:
            retries += 1
            st.warning(f"Rate limit exceeded. Retrying in {2 * retries} seconds... (Attempt {retries}/{max_retries})")
            st.warning(f"Error details: {e}")  # Display the specific error message
            time.sleep(2 * retries)  # Exponential backoff
    st.error("Failed to summarize due to repeated rate limit errors.")
    return None


# Function to summarize the PDF
def summarize_pdf(file_path):
    # Extract TOC and corresponding chapters
    toc_chapters = extract_toc_and_chapter_content(file_path)
    
    # Load language model for summarization
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        model_name="mistralai/pixtral-12b:free",
    )
    prompt = PromptTemplate(template="Summarize the following text: {text}", input_variables=["text"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

    # Store summaries safely
    summaries = {}

    # Summarize chapters sequentially
    for chapter_title, chapter_text in toc_chapters.items():
        with st.spinner(f"Summarizing {chapter_title}..."):
            summary = summarize_with_retry(llm_chain, chapter_text)
            if summary:
                summaries[chapter_title] = summary

    # Summarize chapters concurrently
    # with ThreadPoolExecutor() as executor:
    #     futures = {
    #         executor.submit(summarize_with_retry, llm_chain, chapter_text): chapter_title
    #         for chapter_title, chapter_text in toc_chapters.items()
    #     }

    #     for future in futures:
    #         chapter_title = futures[future]
    #         summary = future.result()
    #         if summary:
    #             summaries[chapter_title] = summary

    # # Display the summaries in Streamlit (after concurrency)
    # for chapter_title, summary in summaries.items():
    #     with st.expander(chapter_title):
    #         st.write(summary)

    return summaries

# File uploader and summarization trigger
uploaded_file = st.file_uploader("Choose a PDF book file", type="pdf")
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    # Summarize the PDF
    with st.spinner("Processing the PDF..."):
        st.header("Chapter Content")
        summaries = summarize_pdf(file_path)

        st.header("Chapter Summaries")
        # Display the summaries in Streamlit
        for chapter_title, summary in summaries.items():
            with st.expander(chapter_title):
                st.write(summary)
