"""
Application constants.
"""

# Database
TABLE_QUESTIONS = "questions"
TABLE_CONTEXTS = "contexts"
TABLE_INSTRUCTIONS = "instructions"
TABLE_VERSIONS = "versions"
TABLE_VARIANTS = "variants"
TABLE_FEEDBACK = "feedback"
TABLE_ITERATIONS = "iterations"

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

# File upload
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".json", ".txt", ".csv"}

# Text limits
MAX_QUESTION_LENGTH = 500
MAX_OPTION_LENGTH = 200
MAX_TEMPLATE_LENGTH = 10000

# Versioning
MAX_VERSION_HISTORY = 50

# Feedback
MIN_RATING = 1
MAX_RATING = 5
