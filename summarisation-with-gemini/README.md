# Document Summarisation App

A small Streamlit-based document summarisation app that uses LangChain-compatible LLM connectors (Gemini / OpenAI via community integrations) to produce prose, bullet-point, or extractive summaries from uploaded PDF or TXT files.

This repository contains a lightweight front-end (`app.py`) and summarisation logic (`summariser.py`), plus small loader and configuration helpers.

## Features
- Upload PDF or TXT documents and generate summaries
- Three summary modes: `prose`, `bullet`, and `extractive`
- Three chain behaviours supported: `stuff`, `map_reduce`, `refine`
- Uses prompt templates in `templates/` for easy customization

## Requirements
- Python 3.8+ (3.10 or 3.11 recommended)
- See `requirements.txt` for the Python packages used by the project.

Recommended minimal dependencies (as present in `requirements.txt`):

- langchain
- langchain-core
- langchain-google-genai
- langchain-community
- pypdf
- streamlit
- python-dotenv

## Quick setup (Windows / PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Provide your Google API key (used by the Gemini connector) or other LLM credentials

The app uses `python-dotenv` to load environment variables from a `.env` file. Create a `.env` file in the project root with the following content:

```text
GOOGLE_API_KEY=your_api_key_here
# If using OpenAI-based connectors, set OPENAI_API_KEY=...
```

Alternatively you can set the environment variable in PowerShell for the session:

```powershell
$env:GOOGLE_API_KEY = "your_api_key_here"
```

4. Run the Streamlit app

```powershell
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501) to upload a document and generate summaries.

## Files of interest
- `app.py` — Streamlit user interface (upload, mode selection, and invocation of the summariser)
- `summariser.py` — Core summarisation logic and chain behaviour (`stuff`, `map_reduce`, `refine`)
- `loader.py` — Loads `pdf` and `txt` files into text
- `config.py` — Modes and template paths mapping
- `templates/` — Prompt templates (customise these to tailor the summaries):
  - `prompt_template.txt` (prose)
  - `bullet_summary_template.txt` (bullet points)
  - `extractive_summary_template.txt` (extractive)

## Usage notes
- Supported upload file types: `.pdf`, `.txt`. Uploaded file bytes are saved as `upload.<ext>` in the project root by `loader.py`.
- If no LLM object is passed to `summarise()` the code falls back to `ChatGoogleGenerativeAI` configured with `gemini-1.5-flash`.
- To switch models or provide a custom LLM, pass it into `summarise()` from your code. See `summariser.py` for the expected function signature:

```python
def summarise(documents, llm=None, mode: str = None, chain_type: str = "stuff"):
    # documents: list[str] or list[langchain_core.documents.Document]
    # mode: one of "prose", "bullet", "extractive"
    # chain_type: one of "stuff", "map_reduce", "refine"
```

## Troubleshooting
- If Streamlit does not start, check that the virtual environment is active and packages installed. Re-run `pip install -r requirements.txt`.
- If the LLM connector raises an authentication error, ensure `GOOGLE_API_KEY` or the relevant provider key is set and valid.
- For large PDFs, summarisation may take longer or hit token limits in some chain strategies; try `map_reduce` or `refine` to break work into smaller pieces.

### Regenerating `requirements.txt`

If you want to regenerate `requirements.txt` from the imports in the code you can use `pipreqs`. Example command (run in the project root):

```powershell
python -m pipreqs.pipreqs . --force --encoding=utf-8
```

Notes:
- On Windows `pipreqs` may encounter a UnicodeDecodeError when it reads some files with non-UTF8 encodings. If that happens you can try the `--encoding=utf-8` flag as shown above. If the error persists, regenerate the file manually by inspecting imports and updating `requirements.txt`.
- This project already includes `langchain-core` in `requirements.txt` because `summariser.py` imports `langchain_core.*` types.

## Environment variables (.env)

This project reads runtime configuration from a `.env` file (see `.env.example`). Available variables and defaults:

- `GOOGLE_API_KEY` — API key for Google Generative AI (no default)
- `DEFAULT_MODE` — `prose` | `bullet` | `extractive` (default: `prose`)
- `DEFAULT_CHAIN_TYPE` — `stuff` | `map_reduce` | `refine` (default: `stuff`)
- `DEFAULT_LLM_MODEL` — LLM model name used for fallback (default: `gemini-1.5-flash`)
- `DEFAULT_TEMPERATURE` — model temperature as a number/string (default: `0`)
- `UPLOAD_FILENAME` — prefix used when saving uploaded files (default: `upload`)

Place a `.env` file in the project root or set session environment variables before starting the app. The app will load `.env` automatically via `python-dotenv`.

## Development & Tests
- This repository does not include automated tests yet. For local development, consider adding small unit tests around `loader.py` and `summariser.py` behaviours.

## Contributing
- Feel free to open issues or submit pull requests. For prompt/template changes, edit the files in `templates/` and test different modes / chain types using the Streamlit UI.

## License
- Add a LICENSE file if you intend to publish this repository. If not specified, the code has no license and cannot be reused without permission.

---

If you'd like, I can also:
- add a sample `.env.example` file
- add a simple test for `loader.py` and `summariser.py`
- create a small `Makefile` or PowerShell script for setup commands

Let me know which extras you want and I'll add them.
