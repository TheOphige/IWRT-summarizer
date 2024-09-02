import streamlit as st
from app import text_summarize, reimagine
from app.book_type_extract import novels_extract
from app.populate_chapters import populate_chapters

st.set_page_config(
    page_title="streamlit-folium documentation",
    page_icon="🧨",
    layout="wide",
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Mode", ["Text Summarize", "Reimagine"])


# Main Page
st.image("assets/IWTR-LOGO.png", width=750)
st.title("Welcome to IWTR")

# Introductory Text
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 5)

st.header("Select Your Book Type")

# Define book types and their images
book_types = {
    "Textbook": "assets/textbook.png",
    "Poetry": "assets/poetry.png",
    "Personal Growth": "assets/personal-growth.png",
    "Novel": "assets/novel.png"
}

# Create a selectbox for choosing the book type
selected_book_type = st.selectbox("Choose your book type", list(book_types.keys()))

# Display the selected book type image
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(book_types[selected_book_type], caption=selected_book_type)


# Handle selection
st.write(f"{selected_book_type} selected!")

# PDF Upload
st.header("Upload Your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Summarize Button
if uploaded_file:
    if st.button("Summarize"):
        st.write("⚙Summarizing... While you sleep💤")
        
        populate_chapters()
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