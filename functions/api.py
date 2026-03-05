import os
import sys

# Ensure the root directory is in the path so we can import main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import handler

# Use Mangum handler defined in main.py
# Netlify searches for 'handler' in this file.
