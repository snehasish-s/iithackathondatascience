# Quick Start Guide - Causal Chat Analysis

## 📦 Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip or conda
- Git (optional, for version control)

### 2. Setup Steps

#### Option A: Using Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd causal-chat-analysis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using Conda

```bash
# Create conda environment
conda create -n causal-analysis python=3.10

# Activate environment
conda activate causal-analysis

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
# Test the main application
python app.py

# You should see the analysis output
```

## 🚀 Running the Application

### Command Line Interface (CLI)

Run the full analysis pipeline:
```bash
python app.py
```

With verbose output:
```bash
python app.py --verbose
```

### Interactive Dashboard

Launch the Streamlit dashboard using the wrapper script:
```bash
python dashboard.py
```

This properly initializes the Python path and launches the interactive dashboard.

The dashboard will open at http://localhost:8501

**Alternative methods:**
```bash
# Using streamlit directly from project root
streamlit run src/visualization.py

# Using verbose CLI mode
python app.py --verbose
```

## 📊 What You Get

### CLI Output Includes:
- ✅ Data loading and preprocessing statistics
- ✅ Signal extraction summary
- ✅ Root cause analysis with evidence
- ✅ Early warning detection
- ✅ Escalation risk analysis
- ✅ Statistical summary
- ✅ Actionable recommendations

### Dashboard Features:
- 📊 Overview with key metrics
- 🔍 Detailed causal analysis
- ⚠️ Early warning system
- 🔎 Individual conversation review
- 📈 Statistical breakdowns

## 📁 Project Structure Review

```
causal-chat-analysis/
├── app.py                    # Main entry point
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
├── .gitignore               # Git configuration
│
├── src/
│   ├── config.py            # Configuration management
│   ├── load_data.py         # Data loading
│   ├── preprocess.py        # Data preprocessing
│   ├── signal_extraction.py # Signal detection
│   ├── causal_analysis.py   # Cause analysis
│   ├── early_warning.py     # Warning detection
│   ├── visualization.py     # Streamlit dashboard
│   └── utils.py             # Utility functions
│
├── data/
│   └── Conversational_Transcript_Dataset.json
│
├── pdf/
│   └── ML_HACKATHON_PRAVAAH.pdf
│
└── output/                  # Generated reports (created on run)
    ├── results.json
    ├── evidence.csv
    └── warnings.csv
```

## 🔧 Common Tasks

### Task 1: Run Basic Analysis
```bash
python app.py
```
✓ Loads data, extracts signals, and analyzes causes

### Task 2: Generate Reports
```python
from src.load_data import load_transcripts
from src.preprocess import preprocess_transcripts
from src.causal_analysis import analyze_causes
from src.utils import export_results_json, export_evidence_csv

transcripts = load_transcripts()
processed = preprocess_transcripts(transcripts)
causes, evidence = analyze_causes(processed)

# Export results
export_results_json(causes, evidence, [], "output/my_report.json")
export_evidence_csv(evidence, "output/my_evidence.csv")
```

### Task 3: Customize Signal Detection
Edit `src/config.py`:
```python
SIGNAL_CONFIG = {
    "frustration": {
        "keywords": [
            # Add your custom keywords
            "unhappy", "dissatisfied", "problems"
        ]
    }
}
```

### Task 4: Analyze Specific Domain
```python
processed = preprocess_transcripts(transcripts)

# Filter to e-commerce only
ecommerce = [t for t in processed if t["domain"] == "E-commerce & Retail"]

# Analyze filtered data
causes, evidence = analyze_causes(ecommerce)
```

## 🎓 Understanding the Output

### Key Metrics:
- **Escalation Rate**: % of conversations that escalated
- **Customer Frustration**: Conversations containing frustration keywords
- **Agent Delay**: Conversations where agent asked customer to wait
- **Agent Denial**: Conversations where agent denied a request

### Example Output:
```
Top causes of escalation:

  ● CUSTOMER FRUSTRATION     2826  ( 63.3%)
      Evidence samples:
      1. Transcript 7034-543... Turn 4
         "I've already explained this to multiple different people..."
```

This means:
- 2826 escalations involved customer frustration
- This represents 63.3% of all escalation signals
- Multiple examples show how customers express frustration

## 🐛 Troubleshooting

### Issue: "Data file not found"
**Solution**: Ensure `data/Conversational_Transcript_Dataset.json` exists

### Issue: "Module not found" errors
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Streamlit not working
**Solution**: 
1. Install streamlit specifically:
```bash
pip install streamlit>=1.20.0
```

2. Use the dashboard wrapper script:
```bash
python dashboard.py
```

If you get import errors like "ModuleNotFoundError: No module named 'src'", make sure to run `python dashboard.py` from the project root directory, not from within the src folder.

### Issue: "Config not found"
**Solution**: Ensure you have `src/config.py` in your src directory

## 💡 Tips & Tricks

1. **Batch Processing**: Process multiple datasets by modifying `load_data.py`
2. **Custom Thresholds**: Adjust early warning threshold in `app.py`
3. **Export Data**: Use utilities in `src/utils.py` to export results
4. **Performance**: For large datasets, consider caching with `@st.cache_data`

## 📞 Getting Help

1. Check the full [README.md](README.md) for detailed documentation
2. Review module docstrings:
   ```bash
   python -c "from src.causal_analysis import analyze_causes; help(analyze_causes)"
   ```
3. Check configuration in `src/config.py`
4. Review example usage in `app.py`

## ✅ Next Steps

1. **Run the CLI**: `python app.py`
2. **Explore the Dashboard**: `streamlit run src/visualization.py`
3. **Customize Keywords**: Edit `src/config.py` for your domain
4. **Generate Reports**: Use `src/utils.py` for data export
5. **Extend Analysis**: Add new signal types in `src/signal_extraction.py`

## 📝 Version Information

- **Python**: 3.8+ required
- **Pandas**: ≥1.3.0
- **Streamlit**: ≥1.20.0
- **Scikit-learn**: ≥1.0.0

---

**Last Updated**: February 6, 2026  
💪 Happy analyzing!
