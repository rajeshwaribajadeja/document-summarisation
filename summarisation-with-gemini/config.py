# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

MODES = {
    "prose": {
        "template_file": os.path.join(CURRENT_DIR, "templates/prompt_template.txt"),
        "description": "General abstractive summary in paragraph form",
    },
    "bullet": {
        "template_file": os.path.join(CURRENT_DIR, "templates/bullet_summary_template.txt"),
        "description": "Bullet-point summary",
    },
    "extractive": {
        "template_file": os.path.join(CURRENT_DIR, "templates/extractive_summary_template.txt"),
        "description": "Extractive summary (key sentences)",
    },
}

# Defaults can be overridden via environment variables (loaded from a .env file)
DEFAULT_MODE = os.getenv("DEFAULT_MODE", "prose")
# Default chain behaviour: stuff / map_reduce / refine
DEFAULT_CHAIN_TYPE = os.getenv("DEFAULT_CHAIN_TYPE", "stuff")

# LLM defaults
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gemini-1.5-flash")
# stored as string in env; convert to float when used
DEFAULT_TEMPERATURE = os.getenv("DEFAULT_TEMPERATURE", "0")

# Upload filename prefix
UPLOAD_FILENAME = os.getenv("UPLOAD_FILENAME", "upload")
