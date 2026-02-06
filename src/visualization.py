import streamlit as st
import pandas as pd
from collections import defaultdict
from .load_data import load_transcripts
from .preprocess import preprocess_transcripts, label_outcome
from .causal_analysis import analyze_causes
from .signal_extraction import extract_signals
from .early_warning import detect_early_warning

st.set_page_config(page_title="Causal Chat Analysis", layout="wide")

@st.cache_data
def load_and_process_data():
    transcripts = load_transcripts()
    processed = preprocess_transcripts(transcripts)
    return transcripts, processed

def main():
    st.title("🎯 Causal Chat Analysis Dashboard")
    st.markdown("---")
    
    # Load data
    transcripts, processed = load_and_process_data()
    
    # Sidebar for navigation
    page = st.sidebar.radio("Navigation", 
        ["Overview", "Causal Analysis", "Early Warning", "Detailed View", "Statistics"])
    
    # === PAGE 1: OVERVIEW ===
    if page == "Overview":
        col1, col2, col3, col4 = st.columns(4)
        
        total_transcripts = len(transcripts)
        escalated = sum(1 for t in processed if t["outcome"] == "ESCALATED")
        escalation_rate = (escalated / len(set(t["transcript_id"] for t in processed))) * 100
        avg_turns = len(processed) / len(set(t["transcript_id"] for t in processed))
        
        col1.metric("Total Transcripts", total_transcripts)
        col2.metric("Escalated Cases", escalated)
        col3.metric("Escalation Rate", f"{escalation_rate:.1f}%")
        col4.metric("Avg Turns/Conversation", f"{avg_turns:.1f}")
        
        st.markdown("---")
        
        # Domain breakdown
        st.subheader("📊 Conversations by Domain")
        domain_counts = defaultdict(int)
        for t in transcripts:
            domain_counts[t.get("domain", "Unknown")] += 1
        
        domain_df = pd.DataFrame(list(domain_counts.items()), columns=["Domain", "Count"])
        domain_df = domain_df.sort_values("Count", ascending=False)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(domain_df.set_index("Domain"))
        with col2:
            st.dataframe(domain_df, hide_index=True)
    
    # === PAGE 2: CAUSAL ANALYSIS ===
    elif page == "Causal Analysis":
        st.subheader("🔍 Root Cause Analysis of Escalations")
        
        cause_stats, evidence = analyze_causes(processed)
        
        if cause_stats:
            # Sort by frequency
            sorted_causes = sorted(cause_stats.items(), key=lambda x: x[1], reverse=True)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Signals", sum(cause_stats.values()))
            col2.metric("Unique Causes", len(cause_stats))
            col3.metric("Top Cause", sorted_causes[0][0] if sorted_causes else "N/A")
            
            st.markdown("---")
            
            # Chart
            st.subheader("Signal Frequency")
            causes_df = pd.DataFrame(sorted_causes, columns=["Cause", "Frequency"])
            st.bar_chart(causes_df.set_index("Cause"))
            
            st.markdown("---")
            
            # Detailed causes
            st.subheader("📋 Cause Details")
            for cause, count in sorted_causes:
                with st.expander(f"{cause.replace('_', ' ').title()} ({count} occurrences)"):
                    st.write(f"**Frequency**: {count}")
                    st.write(f"**Evidence Sample**: {len(evidence[cause])} examples")
                    
                    for i, ev in enumerate(evidence[cause][:3], 1):
                        st.write(f"\n**Example {i}** (Transcript ID: {ev['transcript_id']}, Turn {ev['turn_number']})")
                        st.text(ev['text'])
        else:
            st.info("No escalation signals detected in the dataset.")
    
    # === PAGE 3: EARLY WARNING ===
    elif page == "Early Warning":
        st.subheader("⚠️ Early Warning System")
        
        threshold = st.slider("Frustration Threshold", min_value=1, max_value=5, value=2,
                             help="Number of frustration signals before warning")
        
        # Add signal extraction to processed data
        for turn in processed:
            turn["signals"] = extract_signals(turn)
        
        warnings = detect_early_warning(processed, threshold=threshold)
        
        col1, col2 = st.columns(2)
        col1.metric("Early Warnings Generated", len(warnings))
        col2.metric("Threshold Setting", f"{threshold} signals")
        
        st.markdown("---")
        
        if warnings:
            st.subheader("Predicted Escalation Warnings")
            
            warning_data = []
            for w in warnings:
                # Find the corresponding transcript
                transcript = next((t for t in transcripts if t["transcript_id"] == w["transcript_id"]), None)
                if transcript:
                    warning_data.append({
                        "Transcript ID": w["transcript_id"][:8] + "...",
                        "Domain": transcript.get("domain", "Unknown"),
                        "Intent": transcript.get("intent", "Unknown"),
                        "Turn": w["turn_number"],
                        "Preview": w["text"][:60] + "..."
                    })
            
            warning_df = pd.DataFrame(warning_data)
            st.dataframe(warning_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Warning Details")
            for warning in warnings[:5]:
                with st.expander(f"Warning - Transcript {warning['transcript_id'][:8]}... (Turn {warning['turn_number']})"):
                    st.text(warning['text'])
        else:
            st.info(f"No warnings detected with threshold of {threshold}. Try lowering the threshold.")
    
    # === PAGE 4: DETAILED VIEW ===
    elif page == "Detailed View":
        st.subheader("🔎 Detailed Conversation Analysis")
        
        # Select a transcript
        transcript_ids = [t["transcript_id"] for t in transcripts]
        selected_id = st.selectbox("Select a Transcript", transcript_ids)
        
        # Find the transcript
        transcript = next(t for t in transcripts if t["transcript_id"] == selected_id)
        
        # Display transcript info
        col1, col2, col3 = st.columns(3)
        col1.metric("Domain", transcript.get("domain", "N/A"))
        col2.metric("Intent", transcript.get("intent", "N/A"))
        col3.metric("Outcome", label_outcome(transcript))
        
        st.markdown("---")
        st.subheader("Reason for Call")
        st.write(transcript.get("reason_for_call", "N/A"))
        
        st.markdown("---")
        st.subheader("Conversation Flow")
        
        for i, turn in enumerate(transcript["conversation"], 1):
            speaker = turn["speaker"]
            text = turn["text"]
            
            # Extract signals if customer or agent
            temp_turn = {"speaker": speaker, "text": text}
            signals = extract_signals(temp_turn)
            
            col1, col2 = st.columns([1, 10])
            with col1:
                if speaker.lower() == "customer":
                    st.write("👤 Customer")
                else:
                    st.write("🤖 Agent")
            
            with col2:
                st.write(f"**Turn {i}**")
                st.text(text)
                if signals:
                    st.caption(f"🔔 Signals: {', '.join([s.replace('_', ' ').title() for s in signals])}")
    
    # === PAGE 5: STATISTICS ===
    elif page == "Statistics":
        st.subheader("📈 Statistical Analysis")
        
        # Outcome distribution
        outcome_stats = defaultdict(int)
        escalation_by_domain = defaultdict(int)
        escalation_by_intent = defaultdict(int)
        
        for t in processed:
            outcome_stats[t["outcome"]] += 1
            if t["outcome"] == "ESCALATED":
                escalation_by_domain[t["domain"]] += 1
                escalation_by_intent[t["intent"]] += 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Outcome Distribution")
            outcome_df = pd.DataFrame(list(outcome_stats.items()), columns=["Outcome", "Count"])
            st.bar_chart(outcome_df.set_index("Outcome"))
        
        with col2:
            st.subheader("Escalation by Domain")
            domain_esc = pd.DataFrame(list(escalation_by_domain.items()), 
                                     columns=["Domain", "Escalations"])
            domain_esc = domain_esc.sort_values("Escalations", ascending=False).head(10)
            st.bar_chart(domain_esc.set_index("Domain"))
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Escalation by Intent (Top 10)")
            intent_esc = pd.DataFrame(list(escalation_by_intent.items()), 
                                     columns=["Intent", "Escalations"])
            intent_esc = intent_esc.sort_values("Escalations", ascending=False).head(10)
            st.table(intent_esc)
        
        with col2:
            st.subheader("Summary Statistics")
            stats_text = f"""
            **Total Turns Analyzed**: {len(processed)}
            
            **Escalated Turns**: {outcome_stats.get('ESCALATED', 0)}
            
            **Resolved Turns**: {outcome_stats.get('RESOLVED', 0)}
            
            **Escalation Rate**: {(outcome_stats.get('ESCALATED', 0) / len(processed) * 100):.2f}%
            
            **Unique Transcripts**: {len(set(t['transcript_id'] for t in processed))}
            
            **Unique Domains**: {len(set(t['domain'] for t in processed))}
            
            **Unique Intents**: {len(set(t['intent'] for t in processed))}
            """
            st.markdown(stats_text)

if __name__ == "__main__":
    main()
