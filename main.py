import streamlit as st
from app import home, about
from app.book_type_extract import novels_extract

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# Routing
if page == "Home":
    home.show()
elif page == "About":
    about.show()

# Example usage of book_type functions
book_list = [
    {"title": "Book A", "genre": "Fiction"},
    {"title": "Book B", "genre": "Non-Fiction"},
]
categories = novels_extract
st.write("Categorized Books:", categories)
