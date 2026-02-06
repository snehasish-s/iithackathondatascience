"""
Causal Chat Analysis Source Package
"""

__version__ = "1.0.0"
__author__ = "Causal Analysis Team"

from .load_data import load_transcripts
from .preprocess import preprocess_transcripts, label_outcome
from .causal_analysis import analyze_causes
from .signal_extraction import extract_signals, extract_signals_advanced
from .early_warning import detect_early_warning, detect_multi_signal_warning, analyze_escalation_risk
from .config import SIGNAL_CONFIG, ESCALATION_CONFIG, EARLY_WARNING_CONFIG

__all__ = [
    'load_transcripts',
    'preprocess_transcripts',
    'label_outcome',
    'analyze_causes',
    'extract_signals',
    'extract_signals_advanced',
    'detect_early_warning',
    'detect_multi_signal_warning',
    'analyze_escalation_risk',
    'SIGNAL_CONFIG',
    'ESCALATION_CONFIG',
    'EARLY_WARNING_CONFIG',
]
