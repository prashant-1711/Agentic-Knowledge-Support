import fitz  # PyMuPDF
import os


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def load_pdfs_from_folder(folder_path: str):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)

            print(f"📄 Processing: {filename}")

            try:
                text = extract_text_from_pdf(full_path)

                documents.append({
                    "filename": filename,
                    "text": text
                })

            except Exception as e:
                print(f"❌ Failed: {filename} | Error: {e}")

    return documents