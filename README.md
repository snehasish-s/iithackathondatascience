# Causal Chat Analysis - Conversation Escalation Detection & Analysis

A machine learning pipeline for analyzing customer service conversations to identify causal factors leading to escalation, provide early warning signals, and extract actionable insights.

## 📋 Project Overview

This project analyzes conversational transcripts to:
- **Detect escalation patterns** in customer service conversations
- **Identify root causes** of escalation (customer frustration, agent delays, policy denials)
- **Generate early warning signals** to predict escalation before it happens
- **Extract conversation signals** for deeper analysis
- **Provide statistical insights** on conversation outcomes

## 🎯 Key Features

### 1. **Causal Analysis**
- Identifies primary causes of escalation in conversations
- Tracks frustration keywords and patterns
- Detects agent-related issues (delays, denials)
- Provides evidence for each identified cause

### 2. **Signal Extraction**
- Customer frustration detection
- Agent delay identification
- Agent denial of service tracking
- Expandable signal library for custom analysis

### 3. **Early Warning System**
- Detects potential escalation before it occurs
- Configurable thresholds for sensitivity
- Real-time warning generation
- Transcript-level tracking

### 4. **Data Processing**
- Robust JSON data loading
- Automatic outcome classification (ESCALATED vs RESOLVED)
- Turn-by-turn transcript processing
- Multi-domain support (E-commerce, Finance, Support, etc.)

## 📁 Project Structure

```
causal-chat-analysis/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   └── Conversational_Transcript_Dataset.json  # Input dataset
├── pdf/
│   └── ML_HACKATHON_PRAVAAH.pdf   # Project specification
└── src/
    ├── __pycache__/               # Python cache
    ├── load_data.py               # Data loading utilities
    ├── preprocess.py              # Transcript preprocessing
    ├── causal_analysis.py          # Causal analysis engine
    ├── signal_extraction.py        # Signal extraction logic
    ├── early_warning.py            # Early warning detection
    ├── visualization.py            # (Optional) Data visualization
    └── config.py                   # (Optional) Configuration management
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone/Navigate to the project:**
   ```bash
   cd causal-chat-analysis
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

Run the main analysis:
```bash
python app.py
```

This will:
1. Load conversational transcripts from the JSON dataset
2. Preprocess all conversations
3. Perform causal analysis to identify escalation patterns
4. Display top causes with supporting evidence

### Example Output
```
Top causes of escalation:

customer_frustration: 45
  - This is the third time I'm calling about this issue
  - I'm frustrated with the lack of progress
  - Can I please speak to a supervisor?
  
agent_delay: 23
  - Let me check that for you, please hold
  - I'm looking into your account
  
agent_denial: 12
  - Unfortunately, that's not possible per our policy
```

### 🌐 Interactive Web Dashboard

The project includes a modern, responsive web dashboard built with **HTML5, CSS3, and JavaScript** with a **Flask backend API**.

#### Quick Launch (Recommended)

```bash
python run.py
```

This automated script will:
- ✅ Check all dependencies
- ✅ Install missing packages if needed
- ✅ Start the Flask API server
- ✅ Auto-open dashboard in your browser

#### Manual Launch

```bash
# Start the API server
python api.py

# Open browser and visit:
# http://localhost:5000
```

#### Windows Users

**Option 1**: Double-click `start.bat`  
**Option 2**: Run PowerShell script:
```powershell
.\start.ps1
```

#### Dashboard Features (5 Interactive Tabs)

1. **Overview** - Key metrics, escalation breakdown, domain & intent analysis
2. **Causes** - Root cause analysis with evidence and distribution charts  
3. **Signals** - Signal extraction metrics and keyword detection
4. **Early Warnings** - Escalation prediction and warning distribution
5. **Insights** - Priority-ranked recommendations with actionable insights

**Open in browser**: http://localhost:5000

**For detailed frontend documentation**, see [DASHBOARD.md](DASHBOARD.md) and [FRONTEND_SETUP.md](FRONTEND_SETUP.md)

## 📊 Data Format

### Input Dataset Structure
```json
{
  "transcripts": [
    {
      "transcript_id": "unique-id",
      "time_of_interaction": "YYYY-MM-DD HH:MM:SS",
      "domain": "E-commerce & Retail",
      "intent": "Delivery Investigation",
      "reason_for_call": "Description of the issue",
      "conversation": [
        {
          "speaker": "Agent|Customer",
          "text": "Conversation turn text"
        }
      ]
    }
  ]
}
```

### Outcome Classification
- **ESCALATED**: Conversations involving escalations, complaints, or supervisor requests
- **RESOLVED**: Standard conversations that are successfully resolved

## 🔧 Module Details

### `load_data.py`
Loads and validates conversational transcripts from JSON.

**Functions:**
- `load_transcripts(path)` - Load transcripts from JSON file

### `preprocess.py`
Prepares transcripts for analysis with outcome labeling.

**Functions:**
- `label_outcome(transcript)` - Classify conversation outcome
- `preprocess_transcripts(transcripts)` - Process all transcripts

### `signal_extraction.py`
Extracts signals from individual conversation turns.

**Key Signals:**
- `customer_frustration` - Detects customer frustration keywords
- `agent_delay` - Identifies agent response delays
- `agent_denial` - Tracks policy-related denials

**Customizable Keywords:**
- `FRUSTRATION_KEYWORDS` - Customer frustration indicators
- `AGENT_DELAY_KEYWORDS` - Agent delay phrases
- `AGENT_DENIAL_KEYWORDS` - Denial indicators

### `causal_analysis.py`
Analyzes causal relationships between signals and escalation.

**Functions:**
- `analyze_causes(processed_turns)` - Main analysis function
- Returns cause statistics and supporting evidence

### `early_warning.py`
Detects early warning signals for potential escalation.

**Functions:**
- `detect_early_warning(processed_turns, threshold=2)` - Identify warnings

**Parameters:**
- `threshold` - Number of frustration signals before warning (default: 2)

## 🎓 Analysis Workflow

```
1. Load Data
   └─> JSON transcripts loaded
   
2. Preprocess
   └─> Outcome labeling (ESCALATED/RESOLVED)
   └─> Turn-by-turn processing
   
3. Signal Extraction
   └─> Identify signals in each turn
   └─> Customer frustration, agent delays, denials
   
4. Causal Analysis
   └─> Aggregate signals by cause
   └─> Collect evidence
   └─> Generate statistics
   
5. Output
   └─> Print cause statistics
   └─> Display evidence examples
```

## 📈 Analysis Examples

### Example 1: Identifying Frustration Patterns
```python
from src.load_data import load_transcripts
from src.preprocess import preprocess_transcripts
from src.causal_analysis import analyze_causes

transcripts = load_transcripts()
processed = preprocess_transcripts(transcripts)
causes, evidence = analyze_causes(processed)

# Get top frustration cases
for cause, count in sorted(causes.items(), key=lambda x: x[1], reverse=True):
    print(f"{cause}: {count} occurrences")
```

### Example 2: Early Warning Detection
```python
from src.early_warning import detect_early_warning

warnings = detect_early_warning(processed, threshold=2)
for warning in warnings[:5]:
    print(f"Warning in transcript {warning['transcript_id']}")
    print(f"Turn {warning['turn_number']}: {warning['text']}")
```

## 🔍 Extending the Analysis

### Adding Custom Signals
1. Add keywords to `signal_extraction.py`:
   ```python
   NEW_SIGNAL_KEYWORDS = ["keyword1", "keyword2", "keyword3"]
   ```

2. Add detection logic:
   ```python
   if any(word in text for word in NEW_SIGNAL_KEYWORDS):
       signals.append("new_signal_name")
   ```

### Customizing Outcome Labels
Modify `preprocess.py`'s `label_outcome()` function to adjust escalation detection logic.

### Adjusting Early Warning Sensitivity
Increase or decrease the `threshold` parameter in `detect_early_warning()`:
- Lower threshold = More sensitive warnings
- Higher threshold = Only critical escalations

## 📊 Key Metrics

The system tracks:
- **Total Escalations**: Number of escalated conversations
- **Cause Distribution**: Breakdown of escalation causes
- **Signal Frequency**: How often each signal type appears
- **Evidence Count**: Supporting examples per cause
- **Early Warnings**: Predicted escalations for proactive intervention

## 🛠️ Dependencies

See `requirements.txt` for the full list:
- `pandas` - Data manipulation and analysis
- `nltk` - Natural Language Processing
- `textblob` - Text analysis
- `scikit-learn` - Machine learning utilities
- `streamlit` - (Optional) Interactive dashboard

## 💡 Use Cases

1. **Quality Assurance**: Identify training needs for agents
2. **Predictive Support**: Catch issues before escalation
3. **Root Cause Analysis**: Understand why customers escalate
4. **Performance Monitoring**: Track agent and system performance
5. **Policy Optimization**: Identify problematic policies
6. **Trend Analysis**: Spot emerging issues in real-time

## 📝 Notes

- All transcript IDs are anonymized
- Data is processed locally (no external API calls)
- Output includes supporting evidence for transparency
- Keyword-based approach is extensible with ML models

## 🤝 Contributing

To contribute improvements:
1. Add new signals to `signal_extraction.py`
2. Enhance causal analysis logic
3. Improve preprocessing rules
4. Add visualization capabilities

## 📄 License

This project is part of the ML Hackathon PRAVAAH initiative.

## 🗂️ Future Enhancements

- [ ] Machine learning-based signal detection (NLP/BERT)
- [ ] Interactive Streamlit dashboard
- [ ] Real-time conversation monitoring
- [ ] Statistical significance testing
- [ ] Predictive modeling for escalation probability
- [ ] Multi-language support
- [ ] Performance analytics and KPI tracking
- [ ] Export reports (PDF, CSV)

## 📞 Support

For issues or questions about the analysis, review:
- `signal_extraction.py` for signal definitions
- `preprocess.py` for outcome classification logic
- `causal_analysis.py` for cause analysis algorithm

---

**Last Updated**: February 6, 2026  
**Data Source**: Conversational_Transcript_Dataset.json  
**Status**: Active Development
