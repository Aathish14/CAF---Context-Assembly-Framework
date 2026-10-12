import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from caf.ui.demo_dashboard import main

if __name__ == "__main__":
    main()
