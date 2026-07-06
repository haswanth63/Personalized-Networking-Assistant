"""
Pages Package - Streamlit Application Pages
Each page follows the same pattern: render() function
"""

from frontend.pages import home_page
from frontend.pages import generate_page
from frontend.pages import fact_check_page
from frontend.pages import history_page
from frontend.pages import feedback_page

__all__ = [
    'home_page',
    'generate_page',
    'fact_check_page',
    'history_page',
    'feedback_page'
]