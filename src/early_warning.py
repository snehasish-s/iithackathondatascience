from collections import defaultdict
from src.signal_extraction import extract_signals


def detect_early_warning(processed_turns, threshold=2, signal_type="customer_frustration"):
    """
    Detect early warning signals for potential escalation.
    
    Args:
        processed_turns (list): List of processed conversation turns
        threshold (int): Number of signal occurrences before warning (default: 2)
        signal_type (str): Type of signal to track (default: "customer_frustration")
    
    Returns:
        list: List of warning dictionaries with escalation predictions
    """
    warnings = []
    tracker = defaultdict(lambda: {"count": 0, "first_occurrence": None})
    
    for turn in processed_turns:
        tid = turn["transcript_id"]
        
        # Extract signals if not already present
        if "signals" not in turn:
            turn["signals"] = extract_signals(turn)
        
        # Check if the target signal is present
        if signal_type in turn.get("signals", []):
            if tracker[tid]["count"] == 0:
                tracker[tid]["first_occurrence"] = turn["turn_number"]
            
            tracker[tid]["count"] += 1
            
            # Generate warning when threshold is reached
            if tracker[tid]["count"] == threshold:
                warnings.append({
                    "transcript_id": tid,
                    "turn_number": turn["turn_number"],
                    "text": turn["text"],
                    "signal_count": tracker[tid]["count"],
                    "confidence": min(tracker[tid]["count"] / threshold, 1.0),
                    "first_signal_turn": tracker[tid]["first_occurrence"]
                })
    
    return warnings


def detect_multi_signal_warning(processed_turns, signal_weights=None, confidence_threshold=0.7):
    """
    Detect warnings based on multiple signal types with weighted scoring.
    
    Args:
        processed_turns (list): List of processed conversation turns
        signal_weights (dict): Weights for different signal types
        confidence_threshold (float): Minimum confidence score to trigger warning
    
    Returns:
        list: List of warnings with confidence scores
    """
    if signal_weights is None:
        signal_weights = {
            "customer_frustration": 0.5,
            "agent_delay": 0.3,
            "agent_denial": 0.2
        }
    
    warnings = []
    tracker = defaultdict(lambda: {"score": 0.0, "signals": defaultdict(int)})
    
    for turn in processed_turns:
        tid = turn["transcript_id"]
        
        # Extract signals
        if "signals" not in turn:
            turn["signals"] = extract_signals(turn)
        
        # Update signal counts and scores
        for signal in turn.get("signals", []):
            weight = signal_weights.get(signal, 0.1)
            tracker[tid]["score"] += weight
            tracker[tid]["signals"][signal] += 1
            
            # Generate warning if confidence threshold is reached
            if tracker[tid]["score"] >= confidence_threshold:
                # Check if this warning hasn't been already added
                if not any(w["transcript_id"] == tid and w["turn_number"] == turn["turn_number"] 
                          for w in warnings):
                    warnings.append({
                        "transcript_id": tid,
                        "turn_number": turn["turn_number"],
                        "text": turn["text"],
                        "confidence": min(tracker[tid]["score"], 1.0),
                        "signals_detected": dict(tracker[tid]["signals"])
                    })
    
    return warnings


def analyze_escalation_risk(processed_turns, window_size=3):
    """
    Analyze escalation risk using a sliding window approach.
    
    Args:
        processed_turns (list): List of processed conversation turns
        window_size (int): Number of turns to consider for risk assessment
    
    Returns:
        dict: Risk scores for each transcript
    """
    from src.signal_extraction import extract_signals
    
    risk_scores = defaultdict(list)
    transcript_windows = defaultdict(list)
    
    # Build windows for each transcript
    for turn in processed_turns:
        tid = turn["transcript_id"]
        
        # Extract signals if not already present
        if "signals" not in turn:
            turn["signals"] = extract_signals(turn)
        
        transcript_windows[tid].append(turn)
    
    # Analyze each window
    for tid, turns in transcript_windows.items():
        for i in range(len(turns) - window_size + 1):
            window = turns[i:i + window_size]
            
            # Count signals in window
            signal_count = sum(len(turn.get("signals", [])) for turn in window)
            
            risk_score = min(signal_count / (window_size * 2), 1.0)  # Normalize to 0-1
            
            if risk_score > 0:
                risk_scores[tid].append({
                    "turn_range": f"{window[0]['turn_number']}-{window[-1]['turn_number']}",
                    "risk_score": risk_score,
                    "signal_count": signal_count
                })
    
    return risk_scores
