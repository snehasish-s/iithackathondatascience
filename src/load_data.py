import json

def load_transcripts(path="data/Conversational_Transcript_Dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["transcripts"]

if __name__ == "__main__":
    transcripts = load_transcripts()
    print(f"Loaded {len(transcripts)} transcripts")
