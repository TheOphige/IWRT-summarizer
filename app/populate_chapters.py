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