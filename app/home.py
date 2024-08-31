import streamlit as st
from app.book_type_extract import novels_extract, personal_growth_extract, poetry_extract, textbook_extract

def show():
    st.title("Home")
    st.write("Welcome to the home page of this Streamlit app.")
    
    novel = novels_extract
    st.write("Here is some novel:")
    st.write(novel)
    
    st.write("Here is a plot of the data:")
    
