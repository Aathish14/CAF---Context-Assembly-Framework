#!/usr/bin/env python
"""
Patch script to fix asyncio.queues issue in Python 3.12.0
"""

# Patch for asyncio.queues missing __all__ in Python 3.12.0

import asyncio

if not hasattr(asyncio.queues, "__all__"):
    asyncio.queues.__all__ = [
        "Queue",
        "PriorityQueue",
        "LifoQueue",
        "QueueEmpty",
        "QueueFull",
    ]

# Now import and run streamlit
import subprocess
import sys

if __name__ == "__main__":
    # Run the Streamlit app in headless mode to avoid opening browser
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "caf/ui/demo_app.py",
        "--server.headless",
        "true",
        "--server.port",
        "0",  # Let the OS pick a free port
    ])