from pdf_loader import load_pdfs_from_folder

docs = load_pdfs_from_folder(r"D:\Agentic Knowledge Support\data\sample_doc")

for doc in docs:
    print("=" * 50)
    print(doc["filename"])
    print(doc["text"][:500])  # print first 500 chars