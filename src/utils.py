"""
Utility module for Causal Chat Analysis
Contains helper functions for reporting and data export
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def export_results_json(cause_stats, evidence, warnings, output_path="output/results.json"):
    """
    Export analysis results to JSON format.
    
    Args:
        cause_stats (dict): Statistics on causes
        evidence (dict): Evidence for each cause
        warnings (list): Early warning signals
        output_path (str): Path to save JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "analysis": {
            "cause_statistics": dict(cause_stats),
            "total_signals": sum(cause_stats.values()),
            "unique_causes": len(cause_stats),
            "evidence_summary": {
                cause: len(evs) for cause, evs in evidence.items()
            }
        },
        "warnings": {
            "early_warnings": len(warnings),
            "top_warnings": [
                {
                    "transcript_id": w["transcript_id"],
                    "turn_number": w["turn_number"],
                    "confidence": w.get("confidence", 0)
                }
                for w in warnings[:10]
            ]
        }
    }
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    return str(output_file)


def export_evidence_csv(evidence, output_path="output/evidence.csv"):
    """
    Export evidence to CSV format.
    
    Args:
        evidence (dict): Evidence mapping
        output_path (str): Path to save CSV file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    rows = []
    for cause, examples in evidence.items():
        for ex in examples:
            rows.append({
                "cause": cause,
                "transcript_id": ex["transcript_id"],
                "turn_number": ex["turn_number"],
                "text": ex["text"][:100]  # Truncate for CSV
            })
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    
    return str(output_file)


def export_warnings_csv(warnings, output_path="output/warnings.csv"):
    """
    Export warnings to CSV format.
    
    Args:
        warnings (list): List of warnings
        output_path (str): Path to save CSV file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    rows = []
    for warning in warnings:
        rows.append({
            "transcript_id": warning["transcript_id"],
            "turn_number": warning["turn_number"],
            "confidence": warning.get("confidence", 0),
            "text": warning["text"][:100]
        })
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    
    return str(output_file)


def generate_report_text(cause_stats, evidence, warnings, statistics):
    """
    Generate a text report of the analysis.
    
    Args:
        cause_stats (dict): Cause statistics
        evidence (dict): Evidence data
        warnings (list): Warning list
        statistics (dict): General statistics
    
    Returns:
        str: Formatted report text
    """
    report = []
    report.append("=" * 80)
    report.append("CAUSAL CHAT ANALYSIS - COMPREHENSIVE REPORT")
    report.append("=" * 80)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Executive Summary
    report.append("\n" + "-" * 80)
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 80)
    
    total_signals = sum(cause_stats.values()) if cause_stats else 0
    report.append(f"Total Signals Detected: {total_signals}")
    report.append(f"Unique Causes: {len(cause_stats)}")
    report.append(f"Early Warnings Generated: {len(warnings)}")
    report.append(f"Escalation Rate: {statistics.get('escalation_rate', 0):.2f}%")
    
    # Cause Analysis
    if cause_stats:
        report.append("\n" + "-" * 80)
        report.append("ROOT CAUSE ANALYSIS")
        report.append("-" * 80)
        
        for cause, count in sorted(cause_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_signals * 100) if total_signals > 0 else 0
            report.append(f"\n{cause.replace('_', ' ').upper()}")
            report.append(f"  Frequency: {count} ({percentage:.1f}%)")
            
            if cause in evidence and evidence[cause]:
                report.append(f"  Sample Evidence (showing {min(2, len(evidence[cause]))} of {len(evidence[cause])}):")
                for i, ev in enumerate(evidence[cause][:2], 1):
                    report.append(f"    {i}. \"{ev['text'][:80]}...\"")
    
    # Recommendations
    report.append("\n" + "-" * 80)
    report.append("RECOMMENDATIONS")
    report.append("-" * 80)
    
    if cause_stats:
        top_cause = max(cause_stats.items(), key=lambda x: x[1])[0]
        report.append(f"\n1. PRIMARY FOCUS")
        report.append(f"   Address '{top_cause.replace('_', ' ').title()}' as priority")
        report.append(f"   This accounts for {(cause_stats[top_cause]/total_signals*100):.1f}% of escalations")
    
    if len(warnings) > 0:
        report.append(f"\n2. EARLY INTERVENTION PROGRAM")
        report.append(f"   {len(warnings)} conversations show escalation warning signs")
        report.append(f"   Implement real-time monitoring for early detection")
    
    report.append("\n" + "=" * 80)
    
    return "\n".join(report)


def print_analysis_summary(cause_stats, evidence, warnings, risk_scores=None):
    """
    Print a formatted summary of the analysis.
    
    Args:
        cause_stats (dict): Cause statistics
        evidence (dict): Evidence data
        warnings (list): Warning list
        risk_scores (dict): Risk scores (optional)
    """
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    if cause_stats:
        total = sum(cause_stats.values())
        print(f"\nCause Distribution ({total} total signals):")
        for cause, count in sorted(cause_stats.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int((count / total * 30)) + "░" * (30 - int((count / total * 30)))
            print(f"  {cause:<25} {bar} {count:>5} ({count/total*100:>5.1f}%)")
    
    print(f"\nWarning Signals: {len(warnings)} detected")
    if risk_scores:
        print(f"High-Risk Conversations: {len([r for r in risk_scores.values() if any(x['risk_score'] > 0.7 for x in r)])}")
    
    print("\n" + "=" * 80)


def get_conversation_context(transcript, turn_number, context_window=2):
    """
    Get conversation context around a specific turn.
    
    Args:
        transcript (dict): The full transcript
        turn_number (int): The turn to get context for
        context_window (int): Number of turns before/after to include
    
    Returns:
        list: List of turns with context
    """
    conversation = transcript.get("conversation", [])
    start = max(0, turn_number - context_window - 1)
    end = min(len(conversation), turn_number + context_window)
    
    context = []
    for i in range(start, end):
        turn = conversation[i]
        context.append({
            "turn_number": i + 1,
            "speaker": turn["speaker"],
            "text": turn["text"],
            "is_target": (i + 1 == turn_number)
        })
    
    return context


def create_transcript_index(transcripts):
    """
    Create a quick lookup index for transcripts.
    
    Args:
        transcripts (list): List of transcripts
    
    Returns:
        dict: Mapping of transcript_id to transcript
    """
    return {t["transcript_id"]: t for t in transcripts}
