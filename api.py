#!/usr/bin/env python3
"""
Flask API Backend for Causal Chat Analysis
Provides endpoints for dashboard frontend
"""

from flask import Flask, render_template, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
import sys
import json
from pathlib import Path
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.load_data import load_transcripts
from src.preprocess import preprocess_transcripts, label_outcome
from src.signal_extraction import extract_signals, extract_all_signals, get_signal_confidence
from src.causal_analysis import analyze_causes
from src.early_warning import detect_early_warning, detect_multi_signal_warning, analyze_escalation_risk
from src.config import SIGNAL_CONFIG, EARLY_WARNING_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Global cache for data
_cache = {
    'transcripts': None,
    'processed': None,
    'signals': None,
    'warnings': None
}

def load_data():
    """Load and cache all data"""
    if _cache['transcripts'] is None:
        logger.info("Loading transcripts...")
        _cache['transcripts'] = load_transcripts()
        logger.info(f"Loaded {len(_cache['transcripts'])} transcripts")
        
        logger.info("Preprocessing data...")
        _cache['processed'] = preprocess_transcripts(_cache['transcripts'])
        logger.info(f"Preprocessed {len(_cache['processed'])} conversations")
    
    return _cache['transcripts'], _cache['processed']

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        transcripts, processed = load_data()
        
        escalated = sum(1 for t in processed if t.get('outcome') == 'escalated')
        resolved = sum(1 for t in processed if t.get('outcome') == 'resolved')
        total_turns = sum(len(t.get('turns', [])) for t in processed)
        
        stats = {
            'total_transcripts': len(transcripts),
            'total_turns': total_turns,
            'escalated_conversations': escalated,
            'resolved_conversations': resolved,
            'escalation_rate': round(escalated / len(processed) * 100, 2) if processed else 0,
            'avg_turns_per_conversation': round(total_turns / len(processed), 2) if processed else 0
        }
        
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/causes', methods=['GET'])
def get_causes():
    """Get causal analysis results"""
    try:
        transcripts, processed = load_data()
        
        logger.info("Analyzing causes...")
        causes, evidence = analyze_causes(processed)
        
        # Handle different data structures from analyze_causes
        total_signals = 0
        causes_safe = {}
        if isinstance(causes, dict):
            for key, val in causes.items():
                if isinstance(val, (list, tuple)):
                    causes_safe[key] = len(val)
                    total_signals += len(val)
                elif isinstance(val, int):
                    causes_safe[key] = val
                    total_signals += val
                else:
                    causes_safe[key] = 1
                    total_signals += 1
        
        result = {
            'top_causes': causes_safe,
            'evidence': evidence or {},
            'total_signals': total_signals
        }
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in get_causes: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/signals', methods=['GET'])
def get_signals():
    """Get signal extraction results"""
    try:
        transcripts, processed = load_data()
        
        logger.info("Extracting signals...")
        
        # Count signal types from processed turns (sample for performance)
        signal_counts = {'customer_frustration': 0, 'agent_delay': 0, 'agent_denial': 0}
        total_extracted = 0
        
        # Extract signals from sample of turns
        sample_size = min(1000, len(processed))
        for turn in processed[:sample_size]:
            signals = extract_signals(turn)
            if signals:
                for signal in signals:
                    if isinstance(signal, dict):
                        signal_type = signal.get('type', '')
                    else:
                        signal_type = str(signal)
                    
                    if signal_type in signal_counts:
                        signal_counts[signal_type] += 1
                    total_extracted += 1
        
        # Scale to full dataset
        total_signals = total_extracted
        if sample_size > 0 and sample_size < len(processed):
            scale = len(processed) / sample_size
            for key in signal_counts:
                signal_counts[key] = int(signal_counts[key] * scale)
            total_signals = int(total_extracted * scale)
        
        result = {
            'total_signals': sum(signal_counts.values()),
            'by_type': signal_counts,
            'keywords': SIGNAL_CONFIG
        }
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in get_signals: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/warnings', methods=['GET'])
def get_warnings():
    """Get early warning detection results"""
    try:
        transcripts, processed = load_data()
        
        logger.info("Detecting early warnings...")
        
        single_warnings = 0
        multi_warnings = 0
        high_risk = 0
        
        for conv in processed[:1000]:  # Sample for performance
            turns = conv.get('turns', [])
            if len(turns) > 0:
                signals = extract_signals(conv)
                if signals:
                    warning, confidence = detect_early_warning(signals)
                    if warning:
                        single_warnings += 1
                    
                    multi_warning, multi_conf = detect_multi_signal_warning(signals)
                    if multi_warning:
                        multi_warnings += 1
                
                # Risk analysis
                if len(turns) > 3:
                    risk_score, details = analyze_escalation_risk(turns, signals)
                    if risk_score > 0.7:
                        high_risk += 1
        
        result = {
            'single_signal_warnings': single_warnings,
            'multi_signal_warnings': multi_warnings,
            'high_risk_conversations': high_risk,
            'total_analyzed': min(1000, len(processed)),
            'thresholds': EARLY_WARNING_CONFIG
        }
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in get_warnings: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/domains', methods=['GET'])
def get_domains():
    """Get data by domain"""
    try:
        transcripts, processed = load_data()
        
        domains = {}
        for transcript in transcripts:
            domain = transcript.get('domain', 'Unknown')
            domains[domain] = domains.get(domain, 0) + 1
        
        result = {
            'domains': domains,
            'total_domains': len(domains)
        }
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in get_domains: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get data by intent"""
    try:
        transcripts, processed = load_data()
        
        intents = {}
        for transcript in transcripts:
            intent = transcript.get('intent', 'Unknown')
            intents[intent] = intents.get(intent, 0) + 1
        
        sorted_intents = dict(sorted(intents.items(), key=lambda x: x[1], reverse=True)[:10])
        
        result = {
            'intents': sorted_intents,
            'total_intents': len(intents)
        }
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in get_intents: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/transcript/<transcript_id>', methods=['GET'])
def get_transcript(transcript_id):
    """Get specific transcript details"""
    try:
        transcripts, processed = load_data()
        
        transcript = next((t for t in transcripts if t.get('transcript_id') == transcript_id), None)
        
        if not transcript:
            return jsonify({'success': False, 'error': 'Transcript not found'}), 404
        
        # Find processed version
        proc_transcript = next((t for t in processed if t.get('transcript_id') == transcript_id), None)
        
        signals = extract_signals(proc_transcript) if proc_transcript else []
        
        result = {
            'transcript': transcript,
            'processed': proc_transcript,
            'signals': signals
        }
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"Error in get_transcript: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'success': True, 'message': 'API is running'})

if __name__ == '__main__':
    logger.info("Starting Causal Chat Analysis API...")
    app.run(debug=True, host='0.0.0.0', port=5000)
