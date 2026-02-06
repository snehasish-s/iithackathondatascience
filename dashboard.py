#!/usr/bin/env python3
"""
Streamlit Dashboard Launcher
Properly initializes and runs the Causal Chat Analysis dashboard
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now run streamlit
import streamlit.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", str(project_root / "src" / "visualization.py")]
    stcli.main()
