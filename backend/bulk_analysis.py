"""
Bulk CSV Analysis Tool
Processes multiple CSV files and generates analysis for all of them
"""

import os
import json
import time
import csv
from pathlib import Path
from typing import Dict, List
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests

# Configuration
API_BASE_URL = "http://localhost:8000"
UPLOADS_DIR = Path(__file__).parent / "uploads"
RESULTS_DIR = Path(__file__).parent / "analysis_results"
BATCH_DIR = RESULTS_DIR / "batch_analyses"

def setup_directories():
    """Create necessary directories"""
    UPLOADS_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)
    BATCH_DIR.mkdir(exist_ok=True)
    print(f"✓ Directories ready:")
    print(f"  Upload: {UPLOADS_DIR}")
    print(f"  Results: {RESULTS_DIR}")
    print(f"  Batch: {BATCH_DIR}")

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

def find_csv_files():
    """Find all CSV files in uploads directory"""
    if not UPLOADS_DIR.exists():
        print(f"⚠️  No uploads directory found at: {UPLOADS_DIR}")
        print(f"   Create the 'uploads' folder and place your CSVs there")
        return []
    
    csv_files = list(UPLOADS_DIR.glob("*.csv"))
    
    if not csv_files:
        print(f"⚠️  No CSV files found in: {UPLOADS_DIR}")
        print(f"   Place your CSV files in the uploads folder")
        return []
    
    print(f"\n📂 Found {len(csv_files)} CSV files:")
    for csv_file in csv_files:
        size_kb = csv_file.stat().st_size / 1024
        print(f"   • {csv_file.name} ({size_kb:.1f} KB)")
    
    return csv_files

def analyze_csv_file(csv_path: Path):
    """Analyze a single CSV file"""
    print(f"\n{'='*80}")
    print(f"📊 Analyzing: {csv_path.name}")
    print(f"{'='*80}")
    
    if not csv_path.exists():
        print(f"✗ File not found: {csv_path}")
        return None
    
    results = []
    error_count = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            print(f"  Total rows: {len(rows)}")
            
            for idx, row in enumerate(rows, 1):
                try:
                    # Build candle from CSV row
                    candle = {
                        'timestamp': row.get('timestamp', ''),
                        'open': float(row.get('open', 0)),
                        'high': float(row.get('high', 0)),
                        'low': float(row.get('low', 0)),
                        'close': float(row.get('close', 0)),
                        'volume': int(float(row.get('volume', 0))),
                        'trades': int(float(row.get('trades', 0))),
                    }
                    
                    # Optional: Add aggression data if available
                    if 'aggression_buy' in row and row['aggression_buy']:
                        candle['aggression_buy'] = float(row['aggression_buy'])
                    if 'aggression_sell' in row and row['aggression_sell']:
                        candle['aggression_sell'] = float(row['aggression_sell'])
                    
                    print(f"  Processing row {idx}/{len(rows)}...", end='\r')
                    
                    # Send to API
                    response = requests.post(
                        f"{API_BASE_URL}/analyze/candle",
                        json=candle,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        result['input'] = candle
                        results.append(result)
                    else:
                        error_count += 1
                        print(f"\n  ✗ Row {idx} analysis failed: {response.status_code}")
                    
                    time.sleep(0.05)  # Small delay
                
                except Exception as e:
                    error_count += 1
                    print(f"\n  ✗ Row {idx} error: {str(e)}")
        
        print(f"  ✓ Processed {len(results)} rows ({error_count} errors)          ")
        return results
    
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return None

def export_results(filename: str, results: List[Dict]):
    """Export results to multiple formats"""
    if not results:
        print("✗ No results to export")
        return None
    
    # Create subdirectory for this analysis
    analysis_dir = BATCH_DIR / filename.replace('.csv', f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    analysis_dir.mkdir(exist_ok=True)
    
    # JSON export
    json_file = analysis_dir / "results.json"
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"  ✓ JSON: {json_file.name}")
    except Exception as e:
        print(f"  ✗ JSON export failed: {e}")
    
    # CSV export
    csv_file = analysis_dir / "results.csv"
    try:
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
                'hfz_score': result.get('hfz_score'),
                'fbi_score': result.get('fbi_score'),
                'dtm_score': result.get('dtm_score'),
                'sda_score': result.get('sda_score'),
                'mtv_score': result.get('mtv_score'),
                'type': result.get('type'),
                'score': result.get('score'),
                'regime': result.get('regime'),
                'confidence': result.get('confluence_score'),
                'session': result.get('session'),
                'alert': result.get('alert'),
            }
            rows.append(row)
        
        if rows:
            fieldnames = rows[0].keys()
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"  ✓ CSV: {csv_file.name}")
    except Exception as e:
        print(f"  ✗ CSV export failed: {e}")
    
    # Summary report
    report_file = analysis_dir / "summary.txt"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Analysis Summary\n")
            f.write(f"{'='*80}\n")
            f.write(f"File: {filename}\n")
            f.write(f"Analyzed: {len(results)} candles\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Statistics
            f.write(f"Score Statistics:\n")
            scores = [r.get('score', 0) for r in results]
            if scores:
                f.write(f"  Min: {min(scores):.2f}\n")
                f.write(f"  Max: {max(scores):.2f}\n")
                f.write(f"  Avg: {sum(scores)/len(scores):.2f}\n\n")
            
            # Indicator averages
            f.write(f"Indicator Averages:\n")
            hfz_scores = [r.get('hfz_score', 0) for r in results if r.get('hfz_score')]
            fbi_scores = [r.get('fbi_score', 0) for r in results if r.get('fbi_score')]
            dtm_scores = [r.get('dtm_score', 0) for r in results if r.get('dtm_score')]
            sda_scores = [r.get('sda_score', 0) for r in results if r.get('sda_score')]
            mtv_scores = [r.get('mtv_score', 0) for r in results if r.get('mtv_score')]
            
            if hfz_scores:
                f.write(f"  HFZ: {sum(hfz_scores)/len(hfz_scores):.2f}\n")
            if fbi_scores:
                f.write(f"  FBI: {sum(fbi_scores)/len(fbi_scores):.2f}\n")
            if dtm_scores:
                f.write(f"  DTM: {sum(dtm_scores)/len(dtm_scores):.2f}\n")
            if sda_scores:
                f.write(f"  SDA: {sum(sda_scores)/len(sda_scores):.2f}\n")
            if mtv_scores:
                f.write(f"  MTV: {sum(mtv_scores)/len(mtv_scores):.2f}\n")
        
        print(f"  ✓ Report: {report_file.name}")
    except Exception as e:
        print(f"  ✗ Report generation failed: {e}")
    
    return analysis_dir

def main():
    print("\n" + "="*80)
    print("BULK CSV ANALYSIS TOOL")
    print("="*80)
    
    # Setup
    setup_directories()
    
    # Check API
    if not check_api_health():
        print("\n⚠️  API is not running. Start it with:")
        print("   docker-compose up -d")
        sys.exit(1)
    
    # Find files
    csv_files = find_csv_files()
    if not csv_files:
        sys.exit(1)
    
    # Analyze each file
    all_results = {}
    for csv_file in csv_files:
        results = analyze_csv_file(csv_file)
        
        if results:
            output_dir = export_results(csv_file.name, results)
            all_results[csv_file.name] = {
                'count': len(results),
                'output_dir': str(output_dir)
            }
    
    # Summary
    print("\n" + "="*80)
    print("✅ BULK ANALYSIS COMPLETE")
    print("="*80)
    
    if all_results:
        print(f"\nAnalyzed {len(all_results)} files:")
        for filename, info in all_results.items():
            print(f"  • {filename}: {info['count']} candles")
            print(f"    Output: {info['output_dir']}")
    
    print(f"\n📁 All results in: {BATCH_DIR}")
    print(f"\n✅ Ready for Profit comparison!")

if __name__ == "__main__":
    main()
