def chapter_content_code_gen(chapter_content):
    chapter_content_code = f"""import streamlit as st
st.write("{chapter_content}")
        """
    return chapter_content_code
