#!/usr/bin/env python3
"""Entry point for Rock Paper Scissors game."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()
