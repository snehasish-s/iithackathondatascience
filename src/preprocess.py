def label_outcome(transcript):
    intent = transcript.get("intent", "").lower()
    reason = transcript.get("reason_for_call", "").lower()

    if (
        "escalation" in intent
        or "complaint" in intent
        or "supervisor" in reason
        or "complaint" in reason
    ):
        return "ESCALATED"
    return "RESOLVED"


def preprocess_transcripts(transcripts):
    processed_turns = []

    for t in transcripts:
        outcome = label_outcome(t)

        for idx, turn in enumerate(t["conversation"]):
            processed_turns.append({
                "transcript_id": t["transcript_id"],
                "domain": t.get("domain", ""),
                "intent": t.get("intent", ""),
                "outcome": outcome,
                "turn_number": idx + 1,
                "speaker": turn["speaker"],
                "text": turn["text"]
            })

    return processed_turns
