import os
import shutil
import streamlit as st

# from dotenv import find_dotenv, load_dotenv
# load_dotenv(find_dotenv())

# Retrieve API keys from .env
# IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
# CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
# CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Retrieve API keys from secrets
# IMGUR_CLIENT_ID = st.secrets["IMGUR_CLIENT_ID"]
# OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
# HUGGINGFACEHUB_API_TOKEN = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
# CLOUDINARY_NAME = st.secrets["CLOUDINARY_NAME"]
# CLOUDINARY_API_KEY = st.secrets["CLOUDINARY_API_KEY"]
# CLOUDINARY_API_SECRET = st.secrets["CLOUDINARY_API_SECRET"]


# Function to clear cache and session state
def clear_cache_and_state():
    # Clear Streamlit cache
    st.cache_data.clear()

    # Clear Streamlit session state
    for key in st.session_state.keys():
        del st.session_state[key]

# Delete the 'pages' directory and clear cache/session state before Streamlit runs
if os.path.exists('pages'):
    shutil.rmtree('pages')
    clear_cache_and_state()
    print("'pages' directory deleted and cache/session state cleared.")

st.set_page_config(
    page_title="IWRT-Summarizer",
    page_icon="🧨",
    layout="wide",
)


# from app.book_type_extract.novels_extract import novels_extract
# from app.book_type_extract.poetry_extract import poetry_extract
# from app.book_type_extract.personal_growth_extract import personal_growth_extract
# from app.book_type_extract.textbook_extract import textbook_extract
from app.book_extract import book_extract
from app.populate_chapters import populate_chapters



# Main Page
st.image("assets/IWTR-LOGO.png", width=300)
st.title("Welcome to IWTR")

# Introductory Text
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 5)


# select summarize mode
st.sidebar.title("Royal commands")
summarize_mode = st.sidebar.radio("Select Mode", ["Text Summarize", "Reimagine"])

# # Handle selection
# if summarize_mode == "Text Summarize":
#     st.header(f"{summarize_mode} selected! Words are better few.")
# elif summarize_mode == "Reimagine":
#     st.header(f"{summarize_mode} selected! One image is more than a thousand words.")

# Define book types
# book_types = ["Textbook", "Poetry", "Personal Growth", "Novel"]

# # Create a selectbox for choosing the book type
# selected_book_type = st.sidebar.selectbox("Select book type", book_types)

# # Handle selection
# if selected_book_type == "Textbook":
#     st.write(f"{selected_book_type} selected! Knowledge is power.")
# elif selected_book_type == "Poetry":
#     st.write(f"{selected_book_type} selected! Shakespeare.")
# elif selected_book_type == "Personal Growth":
#     st.write(f"{selected_book_type} selected! Readers are leaders.")
# elif selected_book_type == "Novel":
#     st.write(f"{selected_book_type} selected! Novels are like sausages.")

# PDF Upload
st.header("Upload Your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Summarize Button
if uploaded_file:
    if st.button("Summarize"):
        st.write("⚙Summarizing... While you sleep💤")

        # extract book based on book type
        # if selected_book_type == 'Textbook':
        #     book = textbook_extract(uploaded_file)
        #     st.write("Textbook extracted")
        # elif selected_book_type == 'Poetry':
        #     book = poetry_extract(uploaded_file)
        #     st.write("Poetry extracted")
        # elif selected_book_type == 'Personal Growth':
        #     book = personal_growth_extract(uploaded_file)
        #     st.write("Personal Growth book extracted")
        # elif selected_book_type == 'Novel':
        #     book = novels_extract(uploaded_file)
        #     st.write("Novels extracted")

        book = book_extract(uploaded_file)
        st.write("Book extracted")
        
        # check summarized mode selection
        if summarize_mode == "Text Summarize":
            mode = "Text Summarize"
            st.write("Summarizing text...")
        elif summarize_mode == "Reimagine":
            mode = "Reimagine"
            st.write("Reimagining...")

        # get summarized book 
        populate_chapters(mode = mode, book= book)

        st.write("I'm done Summarizing your Highness👑")

# Reset button
if st.sidebar.button("Upload new book"):
     # Delete the 'pages' directory before rerunning the app
    if os.path.exists('pages'):
        shutil.rmtree('pages')
        print("'pages' directory deleted.")
        clear_cache_and_state()
        st.rerun()
        # import streamlit as st
        # from pages import novels_extract, poetry_extract

        # Sidebar for navigation
        # st.sidebar.markdown("<h2 style='text-align: center;'>Navigation</h2>", unsafe_allow_html=True)

        # # Custom CSS for larger buttons
        # button_style = """
        #     <style>
        #     .stButton button {
        #         width: 100%;
        #         height: 50px;
        #         font-size: 20px;
        #     }
        #     </style>
        # """

        # st.sidebar.markdown(button_style, unsafe_allow_html=True)

        # chapter_names = ['intro', 'fufu', 'eba', 'lulaby', 'gurima', 'gotnick', 'fufus', 'ebas', 'lulabys', 'gurimas', 'gotnicks',]
        # for name in chapter_names:
        #     if st.sidebar.button(name):
        #         st.session_state.page = name
        

        # # Set a default page if none is selected
        # if "page" not in st.session_state:
        #     st.session_state.page = "Home"

        # Display the selected page
        # if st.session_state.page == "Home":
        #     home.show()
        # elif st.session_state.page == "Page 1":
        #     page_1.show()
        # elif st.session_state.page == "Page 2":
        #     page_2.show()

        



        # # Routing
        # if page == "Text Summarize":
        #     st.write("Text Summarize selected")
        #     # text_summarize.show()  
        # elif page == "Reimagine":
        #     st.write("Reimagine selected")
        #     # reimagine.show()