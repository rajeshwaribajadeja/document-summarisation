# loader.py
from langchain_community.document_loaders import TextLoader, PyPDFLoader

def load_doc(file_bytes, file_name: str) -> str:
    ext = file_name.split(".")[-1].lower()
    save_file_name = "upload." + ext
    with open(save_file_name, "wb") as f:
        f.write(file_bytes.getvalue())

    if ext == "txt":
        docs = TextLoader(save_file_name).load()
    elif ext == "pdf":
        docs = PyPDFLoader(save_file_name).load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    content = "\n\n".join([d.page_content for d in docs])
    return content
