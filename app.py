import sys
from pathlib import Path

# Add the repository root to the Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import and run the actual CAF application
from caf.ui.demo_dashboard import main

if __name__ == "__main__":
    main()
