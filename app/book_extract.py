import os
import re
import time
import streamlit as st
import fitz  # PyMuPDF
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from openai import RateLimitError
from dotenv import find_dotenv, load_dotenv
from concurrent.futures import ThreadPoolExecutor
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

# Function to extract TOC using PyMuPDF
def extract_toc_from_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc(simple=True)
    st.write("TOC extracted from metadata: ", toc)  # Debug: Print TOC
    return [toc_item[1] for toc_item in toc] if toc else None

# Fallback: Extract TOC using regex patterns
def extract_toc_with_regex(text):
    toc_pattern = re.compile(r'Table of Contents|Contents|Chapter|Chapters|Outline', re.IGNORECASE)
    toc_match = toc_pattern.search(text)
    if toc_match:
        toc_start = toc_match.end()
        toc_section = text[toc_start:text.find('\n\n', toc_start)].strip()  # Assuming TOC ends before double newlines
        st.write("Extracted TOC section: ", toc_section)  # Debug: Print TOC section
        chapter_pattern = re.compile(r'(\d+\.?\s+.*?)(?=\n|$)', re.MULTILINE)
        return chapter_pattern.findall(toc_section)
    return []

# Function to extract chapters based on TOC
def extract_chapters(text, toc_titles):
    chapters = {}
    lines = text.split('\n')
    current_chapter = None
    lines = [line.strip() for line in lines if line.strip()]  # Clean up the text

    st.write("Extracted Text Lines: ", lines[:100])  # Debug: Print the first 100 lines

    for line in lines:
        if line in toc_titles or is_chapter_title(line):
            current_chapter = line
            st.write(f"Detected chapter title: {line}")  # Debug: Print detected chapter titles
            chapters[current_chapter] = ""
        elif current_chapter:
            chapters[current_chapter] += line + "\n"

    return {k: v.strip() for k, v in chapters.items() if v.strip()}

# Function to classify if a line is a chapter title using regex
def is_chapter_title(line):
    line = line.strip()
    chapter_keywords = r'(Chapter|Ch|Chap\.|Part|Bk|Book|Vol|Volume)'
    roman_numeral_pattern = r'(I{1,3}|IV|V|VI{0,3}|IX|X|L|C{1,3}|D|M)'
    numeric_pattern = r'(\d+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Twenty|Thirty|Hundred)'
    special_titles = r'(Introduction|Prologue|Epilogue|Preface|Acknowledgments|Bibliography|Foreword|Contents|Glossary|Appendix|Index)'
    chapter_title_pattern = rf'^\s*({chapter_keywords})\s*({numeric_pattern}|{roman_numeral_pattern})[.:;\-\–\s]*.*$'
    standalone_chapter_pattern = rf'^\s*({numeric_pattern}|{roman_numeral_pattern}|{special_titles})\s*[.:;\-\–\s]*.*$'
    return bool(re.match(chapter_title_pattern, line, re.IGNORECASE)) or bool(re.match(standalone_chapter_pattern, line, re.IGNORECASE))

# Text size-based heuristic for chapter detection
def extract_chapters_by_text_size(pdf_path):
    doc = fitz.open(pdf_path)
    text_sizes = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = page.get_text("dict")["blocks"]
        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_sizes.append(span["size"])
    most_common_size = max(set(text_sizes), key=text_sizes.count)
    chapters = {}
    current_chapter = None

    st.write("Most common text size:", most_common_size)  # Debug: Print text size information

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = page.get_text("dict")["blocks"]
        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]
                        if size > most_common_size:
                            if current_chapter:
                                chapters[current_chapter] += text + "\n"
                            else:
                                current_chapter = text
                                chapters[current_chapter] = ""
                        elif current_chapter:
                            chapters[current_chapter] += text + "\n"
    st.write("Extracted chapters by text size:", chapters.keys())  # Debug: Print extracted chapter titles
    return {k: v.strip() for k, v in chapters.items() if v.strip()}

# Cross-check TOC with actual content headings
def cross_check_toc_and_chapters(toc_titles, extracted_chapters):
    """Compare TOC titles with extracted chapter titles and align them."""
    matched_chapters = {}
    for toc_title in toc_titles:
        for chapter_title in extracted_chapters.keys():
            if re.search(re.escape(toc_title), chapter_title, re.IGNORECASE):
                matched_chapters[toc_title] = extracted_chapters[chapter_title]
                break
    st.write("Matched chapters after cross-check:", matched_chapters.keys())  # Debug: Print matched chapters
    return matched_chapters

# Function to summarize a single chunk with retry mechanism on rate limit error
def summarize_with_retry(llm_chain, text, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            summary = llm_chain.run(text)
            return summary
        except RateLimitError:
            retries += 1
            st.warning(f"Rate limit exceeded. Retrying in {2 * retries} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(2 * retries)  # Exponential backoff
    st.error("Failed to summarize due to repeated rate limit errors.")
    return None

# Function to summarize the PDF
def summarize_pdf(uploaded_file):
    loader = PyPDFLoader(uploaded_file)
    documents = loader.load()
    full_text = "\n".join([doc.page_content for doc in documents])

    # Extract TOC using metadata
    toc_titles = extract_toc_from_metadata(uploaded_file)
    if toc_titles:
        st.success("TOC successfully extracted from metadata.")
    else:
        st.warning("No TOC metadata found. Falling back to regex extraction.")
        toc_titles = extract_toc_with_regex(full_text)

    if not toc_titles:
        st.warning("No TOC or chapters detected using regex. Trying text size-based chapter extraction.")
        chapters = extract_chapters_by_text_size(uploaded_file)
    else:
        chapters = extract_chapters(full_text, toc_titles)

    if not chapters:
        st.error("No chapters detected. Please ensure the PDF has a clear structure.")
        return

    # Cross-check TOC and chapter content
    cross_checked_chapters = cross_check_toc_and_chapters(toc_titles, chapters)
    
    # Load language model for summarization
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        model_name="mistralai/pixtral-12b:free",
    )
    prompt = PromptTemplate(template="Summarize the following text: {text}", input_variables=["text"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

    # Summarize chapters concurrently
    summaries = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(summarize_with_retry, llm_chain, chapter_text): chapter_title for chapter_title, chapter_text in cross_checked_chapters.items()}
        for future in futures:
            chapter_title = futures[future]
            summary = future.result()
            summaries[chapter_title] = summary

    st.write("Summarized chapters:", summaries.keys())  # Debug: Print summarized chapter titles
    return summaries

# File uploader and summarization trigger
uploaded_file = st.file_uploader("Choose a PDF book file", type="pdf")
if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    summaries = summarize_pdf(file_path)
    if summaries:
        st.write("Summary of the book:")
        for chapter, summary in summaries.items():
            st.subheader(chapter)
            st.write(summary)
