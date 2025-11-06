# summariser.py
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOpenAI
from config import MODES, DEFAULT_MODE, DEFAULT_LLM_MODEL, DEFAULT_TEMPERATURE


def load_template(template_file_path):
    with open(template_file_path, "r", encoding="utf-8") as f:
        return f.read()


def summarise(documents, llm=None, mode: str = None, chain_type: str = "stuff"):
    """
    Summarise a list of LangChain Documents or plain text chunks.
    Supports 'stuff', 'map_reduce', and 'refine' behaviours using LCEL.
    """
    mode = mode or DEFAULT_MODE
    if mode not in MODES:
        raise ValueError(f"Unsupported mode {mode}. Choose from {list(MODES.keys())}")

    template_path = MODES[mode]["template_file"]
    template_str = load_template(template_path)

    # ✅ Fallback: use Gemini (or configured provider/model) if no LLM passed
    if llm is None:
        # DEFAULT_TEMPERATURE is read from env as a string; convert to float safely
        try:
            temp = float(DEFAULT_TEMPERATURE)
        except Exception:
            temp = 0.0

        # If a GOOGLE_API_KEY is available, pass it to the connector
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            llm = ChatGoogleGenerativeAI(model=DEFAULT_LLM_MODEL, temperature=temp, google_api_key=google_key)
        else:
            # Fallback without explicit key (some environments may use ADC or other auth)
            llm = ChatGoogleGenerativeAI(model=DEFAULT_LLM_MODEL, temperature=temp)

    prompt = PromptTemplate.from_template(template_str)
    parser = StrOutputParser()

    # Helper: normalize docs
    def get_text(doc):
        if isinstance(doc, Document):
            return doc.page_content
        elif isinstance(doc, str):
            return doc
        else:
            raise TypeError(f"Unsupported document type: {type(doc)}")

    # --- “stuff” summarization ---
    if chain_type == "stuff":
        chain = prompt | llm | parser
        joined_text = "\n\n".join(get_text(doc) for doc in documents)
        return chain.invoke({"content": joined_text})

    # --- “map_reduce” style ---
    elif chain_type == "map_reduce":
        map_chain = prompt | llm | parser
        partial_summaries = [
            map_chain.invoke({"content": get_text(doc)}) for doc in documents
        ]
        combined_prompt = PromptTemplate.from_template(
            "Combine these summaries into one concise summary:\n\n{content}"
        )
        combine_chain = combined_prompt | llm | parser
        return combine_chain.invoke({"content": "\n".join(partial_summaries)})

    # --- “refine” style ---
    elif chain_type == "refine":
        base_summary = ""
        for doc in documents:
            refine_prompt = PromptTemplate.from_template(
                f"Existing summary:\n{base_summary}\n\nRefine it using this text:\n{{content}}"
            )
            refine_chain = refine_prompt | llm | parser
            base_summary = refine_chain.invoke({"content": get_text(doc)})
        return base_summary

    else:
        raise ValueError(f"Unsupported chain_type {chain_type}")
