"""
Configuration module for Causal Chat Analysis
Centralized settings for data paths, thresholds, and parameters
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIR / "Conversational_Transcript_Dataset.json"
PDF_DIR = PROJECT_ROOT / "pdf"

# Signal detection thresholds
SIGNAL_CONFIG = {
    "frustration": {
        "keywords": [
            "frustrated", "angry", "wasted", "again",
            "multiple", "complaint", "supervisor",
            "not getting help", "fed up", "tired",
            "disappointed", "upset", "unacceptable",
            "ridiculous", "absurd", "annoyed"
        ],
        "min_word_count": 1,
        "case_sensitive": False
    },
    "agent_delay": {
        "keywords": [
            "let me check", "please hold", "one moment",
            "checking", "looking into", "bear with me",
            "give me a second", "wait", "processing",
            "just a moment"
        ],
        "min_word_count": 1,
        "case_sensitive": False
    },
    "agent_denial": {
        "keywords": [
            "cannot", "not possible", "unable",
            "policy", "not allowed", "sorry",
            "can't", "won't", "don't allow"
        ],
        "min_word_count": 5,
        "case_sensitive": False,
        "must_contain": ["sorry"]
    }
}

# Escalation detection config
ESCALATION_CONFIG = {
    "keywords": [
        "escalation", "complaint", "supervisor",
        "manager", "escalate", "escalated"
    ],
    "fields_to_check": ["intent", "reason_for_call"]
}

# Early warning system config
EARLY_WARNING_CONFIG = {
    "default_threshold": 2,
    "min_threshold": 1,
    "max_threshold": 10,
    "signal_type": "customer_frustration"
}

# Analysis config
ANALYSIS_CONFIG = {
    "min_evidence_items": 5,
    "log_level": "INFO",
    "verbose": False
}

# Output config
OUTPUT_CONFIG = {
    "output_dir": PROJECT_ROOT / "output",
    "create_dirs": True,
    "formats": ["json", "csv", "txt"]
}

# Streamlit config
STREAMLIT_CONFIG = {
    "page_title": "Causal Chat Analysis Dashboard",
    "page_icon": "🎯",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Create output directory if needed
if OUTPUT_CONFIG["create_dirs"]:
    OUTPUT_CONFIG["output_dir"].mkdir(parents=True, exist_ok=True)

def get_signal_keywords(signal_type):
    """Get keywords for a specific signal type"""
    if signal_type in SIGNAL_CONFIG:
        return SIGNAL_CONFIG[signal_type]["keywords"]
    return []

def get_data_path():
    """Get the data file path"""
    return str(DATA_FILE)

def get_output_dir():
    """Get the output directory path"""
    return str(OUTPUT_CONFIG["output_dir"])

def validate_config():
    """Validate configuration"""
    errors = []
    
    if not DATA_FILE.exists():
        errors.append(f"Data file not found: {DATA_FILE}")
    
    if not PDF_DIR.exists():
        errors.append(f"PDF directory not found: {PDF_DIR}")
    
    return errors

# Configuration presets for different analysis modes
ANALYSIS_PRESETS = {
    "strict": {
        "early_warning_threshold": 1,
        "min_evidence": 3,
        "focus": "High precision, catch all escalations"
    },
    "balanced": {
        "early_warning_threshold": 2,
        "min_evidence": 5,
        "focus": "Balanced precision and recall"
    },
    "relaxed": {
        "early_warning_threshold": 3,
        "min_evidence": 10,
        "focus": "Only critical escalations"
    }
}

if __name__ == "__main__":
    print("Configuration Loaded")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data File: {DATA_FILE}")
    print(f"Data File Exists: {DATA_FILE.exists()}")
    
    errors = validate_config()
    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✓ Configuration validated successfully")
