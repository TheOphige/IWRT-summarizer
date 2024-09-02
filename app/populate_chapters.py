import os
from app.utils import chapter_content_code_gen

def populate_chapters():

    # Define the chapters dictionary
    summarized_books = {
        'intro': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'fufu': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'eba': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'lulaby': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'gurima': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'gotnick': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'fufus': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'ebas': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'lulabys': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'gurimas': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...',
        'gotnicks': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ...'
    }

    # Ensure the 'pages' directory exists
    os.makedirs('pages', exist_ok=True)

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
