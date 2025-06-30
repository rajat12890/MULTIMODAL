from langchain.document_loaders import PyPDFLoader
import tempfile

def extract_text_from_pdf(pdf_file)->str:
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")as tmp:
        tmp.write(pdf_file.read())
        tmp_path=tmp.name
    loader=PyPDFLoader(tmp_path)
    documents=loader.load()
    all_text = "\n".join([doc.page_content for doc in documents])
    return all_text.strip()