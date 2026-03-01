import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import uvicorn

port = int(os.environ.get("PORT", 8000))
uvicorn.run("main:app", host="0.0.0.0", port=port)
