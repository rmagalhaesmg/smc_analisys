import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)

# Add both backend/ and parent directory to sys.path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import uvicorn

port = int(os.environ.get("PORT", 8000))

# Check if we're running from root directory (Railway) or from backend/ (local)
if os.path.exists(os.path.join(ROOT_DIR, "main.py")):
    # Running from backend/ directory
    app_module = "main:app"
else:
    # Running from root/ directory (Railway)
    app_module = "backend.main:app"

uvicorn.run(app_module, host="0.0.0.0", port=port)
