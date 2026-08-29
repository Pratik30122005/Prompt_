"""
api/index.py — Vercel serverless entry point for the FastAPI backend.

This file imports the full FastAPI `app` from server.py and exposes it
as a Vercel Python serverless handler. Vercel detects the `app` object
(ASGI) and serves it automatically.
"""

import sys
import os

# Make sure the project root is on the path so server.py can import router.py, eval.py, etc.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app  # noqa: F401  — Vercel picks up `app` automatically
