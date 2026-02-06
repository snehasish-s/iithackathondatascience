#!/usr/bin/env python3
"""
Main Application for Causal Chat Analysis
Analyzes customer service conversations to identify escalation causes
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from src.load_data import load_transcripts
from src.preprocess import preprocess_transcripts
from src.causal_analysis import analyze_causes
from src.signal_extraction import extract_signals
from src.early_warning import detect_early_warning, detect_multi_signal_warning, analyze_escalation_risk

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_section(text):
    """Print a section divider"""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print(f"{'─' * 70}")

def analyze_transcripts():
    """Main analysis function"""
    try:
        # Load data
        print_header("CAUSAL CHAT ANALYSIS")
        logger.info("Loading transcripts...")
        transcripts = load_transcripts()
        logger.info(f"Loaded {len(transcripts)} transcripts")
        
        # Preprocess
        print_section("Data Preprocessing")
        logger.info("Preprocessing transcripts...")
        processed = preprocess_transcripts(transcripts)
        logger.info(f"Processed {len(processed)} conversation turns")
        
        # Count escalations
        escalated = sum(1 for p in processed if p["outcome"] == "ESCALATED")
        resolved = sum(1 for p in processed if p["outcome"] == "RESOLVED")
        print(f"✓ ESCALATED: {escalated} turns | RESOLVED: {resolved} turns")
        
        # Extract signals
        print_section("Signal Extraction")
        logger.info("Extracting signals from turns...")
        for turn in processed:
            turn["signals"] = extract_signals(turn)
        
        signals_found = sum(len(p.get("signals", [])) for p in processed)
        print(f"✓ Extracted {signals_found} signals from {len(processed)} turns")
        
        # Causal analysis
        print_section("Causal Analysis - Root Causes of Escalation")
        logger.info("Analyzing causal relationships...")
        cause_stats, evidence = analyze_causes(processed)
        
        if not cause_stats:
            print("ℹ No escalation causes detected")
            return
        
        print(f"\nTop causes of escalation ({len(cause_stats)} unique causes):\n")
        for cause, count in sorted(cause_stats.items(), key=lambda x: x[1], reverse=True):
            cause_name = cause.replace("_", " ").upper()
            percentage = (count / sum(cause_stats.values())) * 100
            print(f"  {'●'} {cause_name:<25} {count:>4}  ({percentage:>5.1f}%)")
            
            # Show evidence
            if evidence[cause]:
                print(f"      Evidence samples:")
                for i, ev in enumerate(evidence[cause][:2], 1):
                    print(f"      {i}. Transcript {ev['transcript_id'][:8]}... Turn {ev['turn_number']}")
                    print(f"         \"{ev['text'][:60]}...\"" if len(ev['text']) > 60 else f"         \"{ev['text']}\"")
                if len(evidence[cause]) > 2:
                    print(f"      ... and {len(evidence[cause]) - 2} more examples")
            print()
        
        # Early warning detection
        print_section("Early Warning System")
        logger.info("Detecting early warning signals...")
        
        warnings = detect_early_warning(processed, threshold=2)
        print(f"Single-signal warnings: {len(warnings)} detected")
        
        multi_warnings = detect_multi_signal_warning(processed, confidence_threshold=0.5)
        print(f"Multi-signal warnings: {len(multi_warnings)} detected")
        
        if multi_warnings:
            print("\nTop warning examples:")
            for warning in multi_warnings[:5]:
                confidence = warning['confidence'] * 100
                signals = ", ".join([s.replace("_", " ").title() for s in warning['signals_detected'].keys()])
                print(f"  • Transcript {warning['transcript_id'][:8]}..., Turn {warning['turn_number']}")
                print(f"    Confidence: {confidence:.1f}% | Signals: {signals}")
        
        # Risk analysis
        print_section("Escalation Risk Analysis")
        logger.info("Analyzing escalation risk patterns...")
        risk_scores = analyze_escalation_risk(processed, window_size=3)
        
        # Find highest risk conversations
        high_risk = []
        for tid, risks in risk_scores.items():
            if risks:
                max_risk = max(r['risk_score'] for r in risks)
                high_risk.append((tid, max_risk))
        
        high_risk.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Analyzed {len(risk_scores)} conversations | High-risk categories found: {len([r for r in high_risk if r[1] > 0.5])}")
        
        if high_risk:
            print("\nHighest risk conversations:")
            for tid, risk_score in high_risk[:5]:
                print(f"  • Transcript {tid[:8]}... | Risk Score: {risk_score:.2f}")
        
        # Summary statistics
        print_section("Summary Statistics")
        
        unique_domains = len(set(p["domain"] for p in processed))
        unique_intents = len(set(p["intent"] for p in processed))
        escalation_rate = (escalated / len(processed)) * 100 if len(processed) > 0 else 0
        
        summary = f"""
        Total Turns Analyzed:    {len(processed):>10}
        Total Conversations:     {len(set(p['transcript_id'] for p in processed)):>10}
        
        Escalation Rate:         {escalation_rate:>10.2f}%
        Escalated Turns:         {escalated:>10}
        Resolved Turns:          {resolved:>10}
        
        Unique Domains:          {unique_domains:>10}
        Unique Intents:          {unique_intents:>10}
        Unique Signals:          {len(cause_stats):>10}
        
        Total Signals Detected:  {signals_found:>10}
        Early Warnings:          {len(warnings):>10}
        Multi-Signal Warnings:   {len(multi_warnings):>10}
        """
        print(summary)
        
        # Recommendations
        print_section("Recommendations")
        
        print("🎯 Based on the analysis:\n")
        
        if cause_stats:
            top_cause = max(cause_stats.items(), key=lambda x: x[1])[0]
            print(f"1. PRIMARY FOCUS: Address '{top_cause.replace('_', ' ').title()}'")
            print(f"   This is the most frequent escalation factor.\n")
        
        if warnings:
            print(f"2. PROACTIVE INTERVENTION: {len(warnings)} conversations show early warning signs")
            print(f"   Consider implementing real-time alerts for these patterns.\n")
        
        if high_risk:
            high_risk_count = len([r for r in high_risk if r[1] > 0.7])
            if high_risk_count > 0:
                print(f"3. URGENT REVIEW: {high_risk_count} conversations have critical escalation risk")
                print(f"   These require immediate agent training or policy review.\n")
        
        print("=" * 70)
        logger.info("Analysis completed successfully")
        
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Causal Chat Analysis Tool")
    parser.add_argument("--mode", choices=["cli", "dashboard"], default="cli",
                       help="Run mode: cli for command-line, dashboard for Streamlit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.mode == "dashboard":
        print("\n🚀 Starting Streamlit Dashboard...")
        print("   Run: streamlit run src/visualization.py\n")
        import subprocess
        subprocess.run(["streamlit", "run", "src/visualization.py"])
    else:
        analyze_transcripts()
