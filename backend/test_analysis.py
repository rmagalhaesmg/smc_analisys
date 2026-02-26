"""
SMC Web App - CSV Upload & Analysis Test Script
Tests the API with example_data.csv and exports results for Profit validation
"""

import os
import json
import time
import csv
from pathlib import Path
from typing import Dict, List
import sys

# For API requests
try:
    import requests
except ImportError:
    print("Installing requests library...")
    os.system("pip install requests")
    import requests

# API Configuration
API_BASE_URL = "http://localhost:8000"
EXAMPLE_CSV = Path(__file__).parent / "example_data.csv"
RESULTS_DIR = Path(__file__).parent / "analysis_results"

def ensure_results_dir():
    """Create results directory if it doesn't exist"""
    RESULTS_DIR.mkdir(exist_ok=True)
    print(f"✓ Results directory: {RESULTS_DIR}")

def check_api_health():
    """Verify API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ API is healthy: {API_BASE_URL}")
            return True
    except Exception as e:
        print(f"✗ API health check failed: {e}")
        return False

def upload_csv():
    """Upload CSV file to API"""
    if not EXAMPLE_CSV.exists():
        print(f"✗ CSV file not found: {EXAMPLE_CSV}")
        return None
    
    print(f"\n📤 Uploading CSV: {EXAMPLE_CSV.name}")
    
    try:
        with open(EXAMPLE_CSV, 'rb') as f:
            files = {'file': (EXAMPLE_CSV.name, f, 'text/csv')}
            response = requests.post(
                f"{API_BASE_URL}/data/upload-csv",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Upload successful!")
            print(f"  Candles loaded: {data.get('candles_loaded', 'N/A')}")
            print(f"  Status: {data.get('status')}")
            return data
        else:
            print(f"✗ Upload failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Upload error: {e}")
        return None

def analyze_single_candle(candle_data: Dict):
    """Analyze a single candle"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze/candle",
            json=candle_data,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"✗ Analysis failed with status {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Analysis error: {e}")
        return None

def analyze_csv_file():
    """Analyze all candles from CSV and collect results"""
    print(f"\n📊 Analyzing candles from CSV...")
    
    if not EXAMPLE_CSV.exists():
        print(f"✗ CSV file not found: {EXAMPLE_CSV}")
        return []
    
    results = []
    
    try:
        with open(EXAMPLE_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                # Convert string values to appropriate types
                candle = {
                    'timestamp': row['timestamp'],
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': int(row['volume']),
                    'trades': int(row['trades']),
                }
                
                print(f"  Processing candle {idx}...", end='\r')
                
                result = analyze_single_candle(candle)
                if result:
                    result['input'] = candle
                    results.append(result)
                
                # Small delay to avoid overwhelming the API
                time.sleep(0.1)
        
        print(f"✓ Analyzed {len(results)} candles          ")
        return results
    
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return []

def export_results_to_json(results: List[Dict]):
    """Export results to JSON format"""
    if not results:
        print("✗ No results to export")
        return None
    
    output_file = RESULTS_DIR / "smc_analysis_results.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✓ Results exported to: {output_file}")
        return output_file
    except Exception as e:
        print(f"✗ Export error: {e}")
        return None

def export_results_to_csv(results: List[Dict]):
    """Export results to CSV for comparison with Profit"""
    if not results:
        print("✗ No results to export")
        return None
    
    output_file = RESULTS_DIR / "smc_analysis_results.csv"
    
    try:
        # Extract data for comparison
        rows = []
        for result in results:
            input_data = result.get('input', {})
            
            row = {
                'timestamp': input_data.get('timestamp'),
                'open': input_data.get('open'),
                'high': input_data.get('high'),
                'low': input_data.get('low'),
                'close': input_data.get('close'),
                'volume': input_data.get('volume'),
                'trades': input_data.get('trades'),
                # SMC Indicator Scores
                'hfz_score': result.get('hfz_score'),
                'fbi_score': result.get('fbi_score'),
                'dtm_score': result.get('dtm_score'),
                'sda_score': result.get('sda_score'),
                'mtv_score': result.get('mtv_score'),
                # Analysis results
                'type': result.get('type'),
                'price': result.get('price'),
                'score': result.get('score'),
                'composite_signal': result.get('type'),  # 'type' field is the signal
                'confidence': result.get('confluence_score'),
                'regime': result.get('regime'),
                'confluence_level': result.get('confluence_level'),
                'session': result.get('session'),
                'alert': result.get('alert'),
            }
            rows.append(row)
        
        # Write CSV
        if rows:
            fieldnames = rows[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            print(f"✓ Results exported to CSV: {output_file}")
            return output_file
        
    except Exception as e:
        print(f"✗ CSV export error: {e}")
    
    return None

def generate_validation_report(results: List[Dict]):
    """Generate a validation report for comparison with Profit"""
    if not results:
        print("✗ No results for report")
        return None
    
    report_file = RESULTS_DIR / "validation_report.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("SMC WEB APP - ANALYSIS VALIDATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Candles Analyzed: {len(results)}\n")
            f.write(f"API Base URL: {API_BASE_URL}\n\n")
            
            # Summary statistics
            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 80 + "\n")
            
            signals = [r.get('composite_signal') for r in results if r.get('composite_signal')]
            regimes = [r.get('regime') for r in results if r.get('regime')]
            traps = [r.get('trap_detected') for r in results if r.get('trap_detected') is not None]
            
            if signals:
                f.write(f"Composite Signals Generated: {len(signals)}\n")
                f.write(f"  BUY Signals: {sum(1 for s in signals if s == 'BUY')}\n")
                f.write(f"  SELL Signals: {sum(1 for s in signals if s == 'SELL')}\n")
                f.write(f"  HOLD Signals: {sum(1 for s in signals if s == 'HOLD')}\n")
            
            if regimes:
                f.write(f"\nRegime Detection:\n")
                regime_counts = {}
                for regime in regimes:
                    regime_counts[regime] = regime_counts.get(regime, 0) + 1
                for regime, count in regime_counts.items():
                    f.write(f"  {regime}: {count}\n")
            
            if traps:
                trap_count = sum(1 for t in traps if t)
                f.write(f"\nTrap Detection:\n")
                f.write(f"  Traps Detected: {trap_count}\n")
                f.write(f"  Clean Candles: {len(traps) - trap_count}\n")
            
            # Detailed results
            f.write(f"\n\nDETAILED RESULTS\n")
            f.write("=" * 80 + "\n")
            
            for idx, result in enumerate(results, 1):
                f.write(f"\nCandle #{idx}\n")
                f.write("-" * 80 + "\n")
                
                input_data = result.get('input', {})
                f.write(f"Timestamp: {input_data.get('timestamp')}\n")
                f.write(f"OHLCV: {input_data.get('open')} | {input_data.get('high')} | {input_data.get('low')} | {input_data.get('close')} | {input_data.get('volume')}\n\n")
                
                # Individual indicator scores
                f.write("Indicator Scores:\n")
                for indicator in ['hfz', 'fbi', 'dtm', 'sda', 'mtv']:
                    ind_data = result.get(indicator, {})
                    score = ind_data.get('score', 'N/A')
                    signal = ind_data.get('signal', 'N/A')
                    f.write(f"  {indicator.upper()}: Score={score}, Signal={signal}\n")
                
                # Composite result
                f.write(f"\nComposite Signal: {result.get('composite_signal', 'N/A')}\n")
                f.write(f"Confidence: {result.get('confidence', 'N/A')}\n")
                f.write(f"Regime: {result.get('regime', 'N/A')}\n")
                f.write(f"Trap Detected: {result.get('trap_detected', 'N/A')}\n")
            
            # Comparison instructions
            f.write(f"\n\n{'=' * 80}\n")
            f.write("VALIDATION INSTRUCTIONS\n")
            f.write(f"{'=' * 80}\n\n")
            f.write("To compare these results with Profit:\n\n")
            f.write("1. Export identical data from Profit platform\n")
            f.write("2. Compare CSV files:\n")
            f.write(f"   - SMC Web App: smc_analysis_results.csv\n")
            f.write(f"   - Profit Output: profit_analysis_results.csv\n")
            f.write("3. Check for score/signal differences\n")
            f.write("4. Validate regime detection accuracy\n")
            f.write("5. Verify trap detection accuracy\n")
            f.write("6. Document any divergences\n")
        
        print(f"✓ Validation report generated: {report_file}")
        return report_file
    
    except Exception as e:
        print(f"✗ Report generation error: {e}")
        return None

def main():
    """Main execution flow"""
    print("\n" + "=" * 80)
    print("SMC WEB APP - ANALYSIS & VALIDATION TEST")
    print("=" * 80)
    
    # Step 1: Verify API
    if not check_api_health():
        print("\n⚠️  API is not running. Start it with:")
        print("   docker-compose up -d")
        sys.exit(1)
    
    # Step 2: Create results directory
    ensure_results_dir()
    
    # Step 3: Upload CSV
    upload_result = upload_csv()
    if not upload_result:
        print("Failed to upload CSV. Exiting.")
        sys.exit(1)
    
    # Allow time for processing
    time.sleep(2)
    
    # Step 4: Analyze candles
    print("\n" + "-" * 80)
    results = analyze_csv_file()
    
    if not results:
        print("No results generated. Exiting.")
        sys.exit(1)
    
    # Step 5: Export results
    print("\n" + "-" * 80)
    print(f"\n💾 Exporting results...")
    
    json_file = export_results_to_json(results)
    csv_file = export_results_to_csv(results)
    report_file = generate_validation_report(results)
    
    # Step 6: Summary
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n📁 Output Files Created:\n")
    if json_file:
        print(f"  1. JSON Results: {json_file}")
    if csv_file:
        print(f"  2. CSV Results:  {csv_file}")
    if report_file:
        print(f"  3. Report:       {report_file}")
    
    print(f"\n📝 Next Steps:")
    print(f"  1. Export same data from Profit platform")
    print(f"  2. Compare CSV files for score/signal accuracy")
    print(f"  3. Review validation_report.txt for details")
    print(f"  4. Document any divergences between platforms")
    
    print(f"\n🔗 For manual testing, visit:")
    print(f"  API Docs: {API_BASE_URL}/docs")
    print(f"  Swagger:  {API_BASE_URL}/docs\n")

if __name__ == "__main__":
    main()
