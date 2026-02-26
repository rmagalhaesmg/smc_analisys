"""
SMC Analysis Diagnostic Tool
Checks what the API is actually returning and identifies any issues
"""

import json
from pathlib import Path
import requests

API_BASE_URL = "http://localhost:8000"
RESULTS_DIR = Path(__file__).parent / "analysis_results"

def load_latest_results():
    """Load the latest analysis results"""
    json_file = RESULTS_DIR / "smc_analysis_results.json"
    
    if not json_file.exists():
        print(f"✗ Results file not found: {json_file}")
        return None
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_results():
    """Analyze the results for completeness"""
    results = load_latest_results()
    
    if not results:
        return
    
    print("\n" + "=" * 80)
    print("SMC ANALYSIS DIAGNOSTIC REPORT")
    print("=" * 80)
    
    first_result = results[0]
    
    print("\nFIRST CANDLE ANALYSIS SAMPLE:")
    print("-" * 80)
    print(json.dumps(first_result, indent=2, ensure_ascii=False))
    
    # Check for missing data
    print("\n\nDATA COMPLETENESS CHECK:")
    print("-" * 80)
    
    indicators = ['hfz', 'fbi', 'dtm', 'sda', 'mtv']
    
    for indicator in indicators:
        ind_data = first_result.get(indicator)
        if ind_data is None:
            print(f"✗ {indicator.upper()}: Missing completely")
        elif isinstance(ind_data, dict):
            if ind_data.get('score') is None:
                print(f"⚠️  {indicator.upper()}: Has no 'score' field")
            else:
                print(f"✓ {indicator.upper()}: Score={ind_data.get('score')}, Signal={ind_data.get('signal')}")
        else:
            print(f"✗ {indicator.upper()}: Invalid format (not dict)")
    
    # Check composite signal
    print(f"\nComposite Signal: {first_result.get('composite_signal', 'MISSING')}")
    print(f"Confidence: {first_result.get('confidence', 'MISSING')}")
    print(f"Regime: {first_result.get('regime', 'MISSING')}")
    print(f"Trap Detected: {first_result.get('trap_detected', 'MISSING')}")
    
    # Summary statistics
    print("\n\nRESULTS SUMMARY:")
    print("-" * 80)
    print(f"Total candles analyzed: {len(results)}")
    
    # Count populated fields
    filled_hfz = sum(1 for r in results if r.get('hfz', {}).get('score') is not None)
    filled_fbi = sum(1 for r in results if r.get('fbi', {}).get('score') is not None)
    filled_dtm = sum(1 for r in results if r.get('dtm', {}).get('score') is not None)
    filled_sda = sum(1 for r in results if r.get('sda', {}).get('score') is not None)
    filled_mtv = sum(1 for r in results if r.get('mtv', {}).get('score') is not None)
    
    print(f"\nIndicators with scores:")
    print(f"  HFZ: {filled_hfz}/{len(results)}")
    print(f"  FBI: {filled_fbi}/{len(results)}")
    print(f"  DTM: {filled_dtm}/{len(results)}")
    print(f"  SDA: {filled_sda}/{len(results)}")
    print(f"  MTV: {filled_mtv}/{len(results)}")
    
    # Signals
    signals = [r.get('composite_signal') for r in results if r.get('composite_signal')]
    print(f"\nComposite signals generated: {len(signals)}/{len(results)}")
    
    regimes = [r.get('regime') for r in results]
    regime_counts = {}
    for r in regimes:
        if r:
            regime_counts[r] = regime_counts.get(r, 0) + 1
    print(f"\nRegime detection:")
    for regime, count in regime_counts.items():
        print(f"  {regime}: {count}")
    
    # Recommendations
    print("\n\nRECOMMENDATIONS:")
    print("-" * 80)
    
    if filled_hfz == 0:
        print("⚠️  HFZ indicator returning no scores")
        print("   Check: aggression_buy/aggression_sell fields in CSV")
        print("   Or: HFZ module implementation\n")
    
    if filled_fbi == 0:
        print("⚠️  FBI indicator returning no scores")
        print("   Check: FBI module implementation\n")
    
    if filled_dtm == 0:
        print("⚠️  DTM indicator returning no scores")
        print("   Check: DTM module implementation\n")
    
    if filled_sda == 0:
        print("⚠️  SDA indicator returning no scores")
        print("   Check: SDA module implementation\n")
    
    if filled_mtv == 0:
        print("⚠️  MTV indicator returning no scores")
        print("   Check: MTV module implementation, time parsing\n")
    
    if len(signals) == 0:
        print("⚠️  No composite signals being generated")
        print("   Check: Signal generation logic in main.py _generate_signal()\n")
    
    # Check API logs
    print("\nTO DEBUG FURTHER:")
    print("-" * 80)
    print("1. Check Docker container logs:")
    print("   docker-compose logs -f smc-api\n")
    print("2. Look for error messages during analysis\n")
    print("3. Verify all SMC modules are correctly imported\n")
    print("4. Check if indicators.csv contains the required columns:\n")
    print("   aggression_buy, aggression_sell")

def main():
    print("Loading latest analysis results...")
    analyze_results()

if __name__ == "__main__":
    main()
