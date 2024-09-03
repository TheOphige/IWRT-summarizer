import os
import shutil
from app.utils import chapter_content_code_gen
from app.text_summarize import text_summarize
from app.reimagine import reimagine

def populate_chapters(mode, book):

    if mode == "Text Summarize":
        summarized_books = text_summarize(book=book)
    elif mode == "Reimagine":
        summarized_books = reimagine(book=book)

    # Check if the 'pages' directory exists and delete it if it does
    if os.path.exists('pages'):
        shutil.rmtree('pages')
        print("'pages' directory deleted.")

    # Create a new 'pages' directory
    os.makedirs('pages', exist_ok=True)
    print("'pages' directory created.")

    # Iterate over the dictionary and create Python files
    for chapter_name, chapter_content in summarized_books.items():
        chapter_content_code = chapter_content_code_gen(chapter_content)
        file_path = f'pages/{chapter_name}.py'
        with open(file_path, 'w') as file:
            file.write(chapter_content_code)
        print(f'File created: {file_path}')


# populate_chapters()


# import streamlit as st
# from pages import home, page_1, page_2

# # Sidebar for navigation
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

# # Clickable text links with larger buttons
# if st.sidebar.button("Home"):
#     st.session_state.page = "Home"
# if st.sidebar.button("Page 1"):
#     st.session_state.page = "Page 1"
# if st.sidebar.button("Page 2"):
#     st.session_state.page = "Page 2"

# # Set a default page if none is selected
# if "page" not in st.session_state:
#     st.session_state.page = "Home"

# # Display the selected page
# if st.session_state.page == "Home":
#     home.show()
# elif st.session_state.page == "Page 1":
#     page_1.show()
# elif st.session_state.page == "Page 2":
#     page_2.show()
