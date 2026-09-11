"""
Pytest configuration — sets up the Python path so tests can import
the app package without installation.
"""

import sys
import os

# Add the backend directory to the path so `app` package is importable
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
