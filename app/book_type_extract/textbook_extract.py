import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Limit Data Return",
    page_icon="🤏",
    layout="wide",
)

def extract_chapter():
    chapter_name = ['intro', 'fufu', 'eba', 'lulaby', 'gurima', 'gotnick', 'fufu', 'eba', 'lulaby', 'gurima', 'gotnick',]
    extracted_chapter_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n " * 5
    
    return chapter_name, extracted_chapter_text