from collections import defaultdict
from src.signal_extraction import extract_signals


def analyze_causes(processed_turns):
    cause_stats = defaultdict(int)
    evidence = defaultdict(list)

    for turn in processed_turns:
        if turn["outcome"] != "ESCALATED":
            continue

        signals = extract_signals(turn)
        for signal in signals:
            cause_stats[signal] += 1

            if len(evidence[signal]) < 5:
                evidence[signal].append({
                    "transcript_id": turn["transcript_id"],
                    "turn_number": turn["turn_number"],
                    "text": turn["text"]
                })

    return cause_stats, evidence
