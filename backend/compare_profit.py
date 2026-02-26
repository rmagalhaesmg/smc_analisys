"""
SMC vs Profit Comparison & Validation Tool
Compares analysis results from SMC Web App with Profit platform outputs
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

RESULTS_DIR = Path(__file__).parent / "analysis_results"

class ComparisonValidator:
    """Compares SMC and Profit analysis results"""
    
    def __init__(self):
        self.indicators = ['hfz', 'fbi', 'dtm', 'sda', 'mtv']
        self.tolerance = 2.0  # Allow 2% difference
        self.divergences = []
    
    def load_csv(self, filepath: Path) -> List[Dict]:
        """Load CSV file"""
        if not filepath.exists():
            print(f"✗ File not found: {filepath}")
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            return []
    
    def compare_scores(self, smc_value, profit_value, tolerance=2.0) -> Tuple[bool, float]:
        """
        Compare two scores
        Returns: (is_match, difference)
        """
        try:
            smc_float = float(smc_value or 0)
            profit_float = float(profit_value or 0)
            
            # Calculate percentage difference
            if profit_float == 0:
                diff = abs(smc_float - profit_float)
            else:
                diff = abs((smc_float - profit_float) / profit_float * 100)
            
            is_match = diff <= tolerance
            return is_match, diff
        except:
            return False, 0
    
    def validate_pair(self, smc_file: Path, profit_file: Path) -> Dict:
        """
        Compare SMC and Profit results
        
        Expected format:
        - Timestamps must match
        - Indicator columns: hfz, fbi, dtm, sda, mtv (or prefixed like profit_hfz, smc_hfz)
        """
        print(f"\n{'='*80}")
        print(f"VALIDATION REPORT")
        print(f"{'='*80}\n")
        
        # Load files
        smc_data = self.load_csv(smc_file)
        profit_data = self.load_csv(profit_file)
        
        if not smc_data:
            print(f"✗ Could not load SMC data from {smc_file}")
            return {'status': 'error', 'message': 'No SMC data'}
        
        if not profit_data:
            print(f"⚠️  Profit file not found. Using template mode.")
            return self._generate_template(smc_data)
        
        print(f"📊 Comparing:")
        print(f"  SMC:    {smc_file.name} ({len(smc_data)} rows)")
        print(f"  Profit: {profit_file.name} ({len(profit_data)} rows)\n")
        
        # Index profit data by timestamp
        profit_by_timestamp = {}
        for row in profit_data:
            ts = row.get('timestamp') or row.get('candle_timestamp')
            if ts:
                profit_by_timestamp[ts] = row
        
        # Compare
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_rows': len(smc_data),
            'matched_rows': 0,
            'divergent_rows': 0,
            'missing_in_profit': 0,
            'indicator_stats': {ind: {'matches': 0, 'divergences': 0, 'avg_diff': 0} for ind in self.indicators},
            'divergences': [],
            'summary': {}
        }
        
        indicator_diffs = {ind: [] for ind in self.indicators}
        
        # Compare each row
        for idx, smc_row in enumerate(smc_data, 1):
            smc_ts = smc_row.get('timestamp') or smc_row.get('candle_timestamp')
            profit_row = profit_by_timestamp.get(smc_ts)
            
            if not profit_row:
                results['missing_in_profit'] += 1
                results['divergences'].append({
                    'type': 'missing',
                    'timestamp': smc_ts,
                    'message': 'Timestamp not found in Profit data'
                })
                continue
            
            row_divergences = []
            row_matched = True
            
            # Compare each indicator
            for indicator in self.indicators:
                smc_key = indicator
                # Try different naming conventions
                profit_keys = [indicator, f'profit_{indicator}', f'{indicator}_profit']
                
                smc_value = smc_row.get(smc_key)
                profit_value = None
                
                for pkey in profit_keys:
                    if pkey in profit_row:
                        profit_value = profit_row[pkey]
                        break
                
                if smc_value and profit_value:
                    is_match, diff = self.compare_scores(smc_value, profit_value, self.tolerance)
                    
                    indicator_diffs[indicator].append(diff)
                    
                    if is_match:
                        results['indicator_stats'][indicator]['matches'] += 1
                    else:
                        results['indicator_stats'][indicator]['divergences'] += 1
                        row_matched = False
                        row_divergences.append({
                            'indicator': indicator,
                            'smc': float(smc_value),
                            'profit': float(profit_value),
                            'diff_percent': round(diff, 2)
                        })
            
            if row_matched:
                results['matched_rows'] += 1
            else:
                results['divergent_rows'] += 1
                results['divergences'].append({
                    'type': 'divergence',
                    'timestamp': smc_ts,
                    'indicators': row_divergences
                })
        
        # Calculate averages
        for ind in self.indicators:
            if indicator_diffs[ind]:
                results['indicator_stats'][ind]['avg_diff'] = round(
                    sum(indicator_diffs[ind]) / len(indicator_diffs[ind]), 2
                )
        
        # Generate summary
        accuracy = (results['matched_rows'] / results['total_rows'] * 100) if results['total_rows'] > 0 else 0
        results['summary'] = {
            'total_accuracy': round(accuracy, 2),
            'status': 'PASSED' if accuracy >= 95 else 'REVIEW REQUIRED' if accuracy >= 80 else 'FAILED',
        }
        
        return results
    
    def _generate_template(self, smc_data: List[Dict]) -> Dict:
        """Generate a template for manual Profit entry"""
        print(f"📋 Generating comparison template for manual entry...")
        
        return {
            'status': 'template_mode',
            'message': 'Profit data not found. Use template to manually enter Profit scores.',
            'rows': len(smc_data),
            'template_rows': [
                {
                    'timestamp': row.get('timestamp') or row.get('candle_timestamp'),
                    'smc_hfz': row.get('hfz_score', 'N/A'),
                    'profit_hfz': 'ENTER_HERE',
                    'smc_fbi': row.get('fbi_score', 'N/A'),
                    'profit_fbi': 'ENTER_HERE',
                    'smc_dtm': row.get('dtm_score', 'N/A'),
                    'profit_dtm': 'ENTER_HERE',
                    'smc_sda': row.get('sda_score', 'N/A'),
                    'profit_sda': 'ENTER_HERE',
                    'smc_mtv': row.get('mtv_score', 'N/A'),
                    'profit_mtv': 'ENTER_HERE',
                }
                for row in smc_data
            ]
        }
    
    def print_report(self, results: Dict):
        """Print validation report"""
        print(f"\n{'='*80}")
        print(f"VALIDATION RESULTS")
        print(f"{'='*80}\n")
        
        if results.get('status') == 'error':
            print(f"✗ {results.get('message')}")
            return
        
        if results.get('status') == 'template_mode':
            print(f"⚠️  Template mode - Profit data not found")
            print(f"   Use the template to manually enter Profit scores\n")
            return
        
        # Summary
        summary = results.get('summary', {})
        print(f"Overall Accuracy: {summary.get('total_accuracy', 'N/A')}%")
        print(f"Status: {summary.get('status', 'N/A')}\n")
        
        # Statistics
        print(f"Statistics:")
        print(f"  Total Candles: {results.get('total_rows')}")
        print(f"  Matched: {results.get('matched_rows')}")
        print(f"  Divergent: {results.get('divergent_rows')}")
        print(f"  Missing in Profit: {results.get('missing_in_profit')}\n")
        
        # Indicator breakdown
        print(f"Indicator Comparison:")
        for ind, stats in results.get('indicator_stats', {}).items():
            print(f"  {ind.upper()}:")
            print(f"    Matches: {stats['matches']}, Divergences: {stats['divergences']}")
            print(f"    Average Difference: {stats['avg_diff']}%\n")
        
        # Top divergences
        divergences = results.get('divergences', [])
        if divergences:
            print(f"Top Divergences (first 10):\n")
            for div in divergences[:10]:
                if div['type'] == 'divergence':
                    print(f"  Timestamp: {div['timestamp']}")
                    for ind_div in div['indicators']:
                        print(f"    {ind_div['indicator'].upper()}: SMC={ind_div['smc']:.2f}, Profit={ind_div['profit']:.2f}, Diff={ind_div['diff_percent']:.2f}%")
                    print()
    
    def export_report(self, results: Dict, output_file: Path):
        """Export validation report to file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("SMC vs PROFIT VALIDATION REPORT\n")
                f.write("="*80 + "\n\n")
                f.write(f"Generated: {results.get('timestamp')}\n\n")
                
                # Summary
                summary = results.get('summary', {})
                f.write(f"Overall Accuracy: {summary.get('total_accuracy', 'N/A')}%\n")
                f.write(f"Status: {summary.get('status', 'N/A')}\n\n")
                
                # Statistics
                f.write("STATISTICS\n")
                f.write("-"*80 + "\n")
                f.write(f"Total Candles: {results.get('total_rows')}\n")
                f.write(f"Matched: {results.get('matched_rows')}\n")
                f.write(f"Divergent: {results.get('divergent_rows')}\n")
                f.write(f"Missing in Profit: {results.get('missing_in_profit')}\n\n")
                
                # Indicator breakdown
                f.write("INDICATOR BREAKDOWN\n")
                f.write("-"*80 + "\n")
                for ind, stats in results.get('indicator_stats', {}).items():
                    f.write(f"{ind.upper()}:\n")
                    f.write(f"  Matches: {stats['matches']}\n")
                    f.write(f"  Divergences: {stats['divergences']}\n")
                    f.write(f"  Average Difference: {stats['avg_diff']}%\n\n")
                
                # Divergences
                f.write("DIVERGENCES\n")
                f.write("-"*80 + "\n")
                divergences = results.get('divergences', [])
                for div in divergences:
                    if div['type'] == 'divergence':
                        f.write(f"Timestamp: {div['timestamp']}\n")
                        for ind_div in div['indicators']:
                            f.write(f"  {ind_div['indicator'].upper()}: SMC={ind_div['smc']:.2f}, Profit={ind_div['profit']:.2f}, Diff={ind_div['diff_percent']:.2f}%\n")
                        f.write("\n")
            
            print(f"✓ Report exported: {output_file.name}")
            return True
        except Exception as e:
            print(f"✗ Export error: {e}")
            return False

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("SMC vs PROFIT COMPARISON TOOL")
    print("="*80)
    
    validator = ComparisonValidator()
    
    # Paths
    smc_file = RESULTS_DIR / "smc_analysis_results.csv"
    profit_file = RESULTS_DIR / "profit_analysis_results.csv"  # Expected name
    
    # Check if SMC file exists
    if not smc_file.exists():
        print(f"✗ SMC results not found: {smc_file}")
        print(f"   Run test_analysis.py or bulk_analysis.py first")
        return
    
    # Validate
    results = validator.validate_pair(smc_file, profit_file)
    
    # Print report
    validator.print_report(results)
    
    # Export report
    report_file = RESULTS_DIR / "validation_report.txt"
    validator.export_report(results, report_file)
    
    print(f"\n✅ Validation complete!")
    print(f"   Report: {report_file}")

if __name__ == "__main__":
    main()
