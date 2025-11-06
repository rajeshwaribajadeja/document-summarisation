import streamlit as st
from summariser import summarise
from loader import load_doc
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
from config import DEFAULT_MODE, DEFAULT_CHAIN_TYPE, DEFAULT_LLM_MODEL, DEFAULT_TEMPERATURE

load_dotenv()  # loads .env file


def main():
    st.title("Document Summarisation App")

    mode_options = ["prose", "bullet", "extractive"]
    default_mode = os.getenv("DEFAULT_MODE", DEFAULT_MODE)
    mode_index = mode_options.index(default_mode) if default_mode in mode_options else 0
    mode = st.selectbox("Choose summary mode", mode_options, index=mode_index)

    chain_options = ["stuff", "map_reduce", "refine"]
    default_chain = os.getenv("DEFAULT_CHAIN_TYPE", DEFAULT_CHAIN_TYPE)
    chain_index = chain_options.index(default_chain) if default_chain in chain_options else 0
    chain_type = st.selectbox("Choose summarisation strategy", chain_options, index=chain_index)

    uploaded_file = st.file_uploader("Upload document", type=['pdf', 'txt'])

    if uploaded_file:
        st.markdown(f"**Selected file:** {uploaded_file.name}")

        # Show a submit button so the user can confirm before running the LLM
        if st.button("Generate summary"):
            with st.spinner("Generating summary — this may take a moment..."):
                try:
                    doc_content = load_doc(uploaded_file, uploaded_file.name)

                    model = os.getenv("DEFAULT_LLM_MODEL", DEFAULT_LLM_MODEL)
                    # temperature may be stored as string in env
                    try:
                        temp = float(os.getenv("DEFAULT_TEMPERATURE", DEFAULT_TEMPERATURE))
                    except Exception:
                        temp = 0.0

                    llm = GoogleGenerativeAI(model=model, google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=temp)

                    summary = summarise([doc_content], llm, mode=mode, chain_type=chain_type)

                    st.write("## Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"An error occurred while generating the summary: {e}")


if __name__ == "__main__":
    main()
