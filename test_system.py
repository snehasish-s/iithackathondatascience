#!/usr/bin/env python3
"""
Test and Demo Script for Causal Chat Analysis
Demonstrates all major features of the system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_config():
    """Test configuration module"""
    print("\n" + "="*70)
    print("TEST 1: Configuration Module")
    print("="*70)
    
    from src.config import (
        validate_config, get_data_path, 
        get_signal_keywords, SIGNAL_CONFIG
    )
    
    errors = validate_config()
    if errors:
        print("❌ Configuration errors found:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("✅ Configuration validated")
    print(f"   Data path: {get_data_path()}")
    print(f"   Signal types: {list(SIGNAL_CONFIG.keys())}")
    print(f"   Frustration keywords: {len(SIGNAL_CONFIG['frustration']['keywords'])}")
    
    return True


def test_data_loading():
    """Test data loading"""
    print("\n" + "="*70)
    print("TEST 2: Data Loading")
    print("="*70)
    
    from src.load_data import load_transcripts
    
    try:
        transcripts = load_transcripts()
        print(f"✅ Loaded {len(transcripts)} transcripts")
        
        # Show sample
        sample = transcripts[0]
        print(f"   Sample transcript fields: {list(sample.keys())}")
        print(f"   Domain: {sample.get('domain')}")
        print(f"   Intent: {sample.get('intent')}")
        print(f"   Conversations: {len(sample.get('conversation', []))}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False


def test_preprocessing():
    """Test preprocessing"""
    print("\n" + "="*70)
    print("TEST 3: Data Preprocessing")
    print("="*70)
    
    from src.load_data import load_transcripts
    from src.preprocess import preprocess_transcripts, label_outcome
    
    try:
        transcripts = load_transcripts()
        processed = preprocess_transcripts(transcripts)
        
        print(f"✅ Processed {len(processed)} conversation turns")
        
        # Show outcome distribution
        escalated = sum(1 for p in processed if p['outcome'] == 'ESCALATED')
        resolved = sum(1 for p in processed if p['outcome'] == 'RESOLVED')
        
        print(f"   Escalated: {escalated} ({escalated/len(processed)*100:.1f}%)")
        print(f"   Resolved: {resolved} ({resolved/len(processed)*100:.1f}%)")
        
        # Show sample processed turn
        sample = processed[0]
        print(f"   Sample turn: {sample['speaker']} - \"{sample['text'][:50]}...\"")
        
        return True
    except Exception as e:
        print(f"❌ Error preprocessing: {e}")
        return False


def test_signal_extraction():
    """Test signal extraction"""
    print("\n" + "="*70)
    print("TEST 4: Signal Extraction")
    print("="*70)
    
    from src.load_data import load_transcripts
    from src.preprocess import preprocess_transcripts
    from src.signal_extraction import extract_signals
    
    try:
        transcripts = load_transcripts()
        processed = preprocess_transcripts(transcripts)
        
        # Extract signals
        signal_count = 0
        signal_types = {}
        
        for turn in processed[:1000]:  # Sample
            signals = extract_signals(turn)
            signal_count += len(signals)
            for signal in signals:
                signal_types[signal] = signal_types.get(signal, 0) + 1
        
        print(f"✅ Extracted signals from sample of 1000 turns")
        print(f"   Total signals: {signal_count}")
        print(f"   Signal types: {signal_types}")
        
        return True
    except Exception as e:
        print(f"❌ Error extracting signals: {e}")
        return False


def test_causal_analysis():
    """Test causal analysis"""
    print("\n" + "="*70)
    print("TEST 5: Causal Analysis")
    print("="*70)
    
    from src.load_data import load_transcripts
    from src.preprocess import preprocess_transcripts
    from src.signal_extraction import extract_signals
    from src.causal_analysis import analyze_causes
    
    try:
        transcripts = load_transcripts()
        processed = preprocess_transcripts(transcripts)
        
        # Add signals
        for turn in processed:
            turn['signals'] = extract_signals(turn)
        
        cause_stats, evidence = analyze_causes(processed)
        
        print(f"✅ Causal analysis completed")
        print(f"   Unique causes: {len(cause_stats)}")
        print(f"   Total signals: {sum(cause_stats.values())}")
        
        for cause, count in sorted(cause_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {cause}: {count}")
        
        return True
    except Exception as e:
        print(f"❌ Error in causal analysis: {e}")
        return False


def test_early_warning():
    """Test early warning detection"""
    print("\n" + "="*70)
    print("TEST 6: Early Warning System")
    print("="*70)
    
    from src.load_data import load_transcripts
    from src.preprocess import preprocess_transcripts
    from src.signal_extraction import extract_signals
    from src.early_warning import (
        detect_early_warning, 
        detect_multi_signal_warning,
        analyze_escalation_risk
    )
    
    try:
        transcripts = load_transcripts()
        processed = preprocess_transcripts(transcripts)
        
        # Add signals
        for turn in processed:
            turn['signals'] = extract_signals(turn)
        
        warnings = detect_early_warning(processed)
        multi_warnings = detect_multi_signal_warning(processed)
        risk_scores = analyze_escalation_risk(processed)
        
        print(f"✅ Early warning detection completed")
        print(f"   Single-signal warnings: {len(warnings)}")
        print(f"   Multi-signal warnings: {len(multi_warnings)}")
        print(f"   Risk-analyzed conversations: {len(risk_scores)}")
        
        if warnings:
            print(f"   Sample warning: {warnings[0]['transcript_id'][:8]}... Turn {warnings[0]['turn_number']}")
        
        return True
    except Exception as e:
        print(f"❌ Error in early warning: {e}")
        return False


def test_utilities():
    """Test utility functions"""
    print("\n" + "="*70)
    print("TEST 7: Utility Functions")
    print("="*70)
    
    try:
        from src.utils import (
            generate_report_text,
            create_transcript_index,
            print_analysis_summary
        )
        from src.load_data import load_transcripts
        
        transcripts = load_transcripts()
        index = create_transcript_index(transcripts)
        
        print(f"✅ Utility functions tested")
        print(f"   Transcript index created: {len(index)} items")
        
        return True
    except Exception as e:
        print(f"❌ Error in utilities: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("CAUSAL CHAT ANALYSIS - SYSTEM TEST SUITE")
    print("="*70)
    
    tests = [
        ("Configuration", test_config),
        ("Data Loading", test_data_loading),
        ("Preprocessing", test_preprocessing),
        ("Signal Extraction", test_signal_extraction),
        ("Causal Analysis", test_causal_analysis),
        ("Early Warning", test_early_warning),
        ("Utilities", test_utilities),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<25} {status}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
