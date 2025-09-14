# sqlite_patch.py
"""
Forces Python to use pysqlite3 instead of the system sqlite3.
This ensures SQLite >= 3.35, required by ChromaDB,
on both Docker and Streamlit Cloud.
"""

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
