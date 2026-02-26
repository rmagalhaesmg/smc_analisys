"""
Profit Format Exporter
Converts SMC Web App analysis results to Profit platform format
"""

import json
import csv
from pathlib import Path
from typing import Dict, List
from datetime import datetime

RESULTS_DIR = Path(__file__).parent / "analysis_results"
BATCH_DIR = RESULTS_DIR / "batch_analyses"

class ProfitFormatter:
    """Formats SMC results for Profit platform import"""
    
    @staticmethod
    def convert_to_profit_format(results: List[Dict]) -> List[Dict]:
        """
        Convert SMC results to Profit format
        
        Profit expected format:
        {
            'timestamp': ISO timestamp,
            'open': float,
            'high': float,
            'low': float,
            'close': float,
            'volume': int,
            'hfz': score (0-100),
            'fbi': score (0-100),
            'dtm': score (0-100),
            'sda': score (0-100),
            'mtv': score (0-100),
            'regime': string,
            'signal': string,  # composite signal
            'confidence': float (0-100)
        }
        """
        profit_results = []
        
        for result in results:
            input_data = result.get('input', {})
            
            profit_entry = {
                'timestamp': result.get('timestamp'),
                'candle_timestamp': input_data.get('timestamp'),
                'open': input_data.get('open'),
                'high': input_data.get('high'),
                'low': input_data.get('low'),
                'close': input_data.get('close'),
                'volume': input_data.get('volume'),
                'trades': input_data.get('trades'),
                # Indicator scores (normalized to 0-100 if needed)
                'hfz': round(result.get('hfz_score', 0) or 0, 2),
                'fbi': round(result.get('fbi_score', 0) or 0, 2),
                'dtm': round(result.get('dtm_score', 0) or 0, 2),
                'sda': round(result.get('sda_score', 0) or 0, 2),
                'mtv': round(result.get('mtv_score', 0) or 0, 2),
                # Analysis results
                'regime': result.get('regime', 'Unknown'),
                'signal': result.get('type', 'neutral'),  # 'type' is the signal
                'composite_score': round(result.get('score', 0) or 0, 2),
                'confidence': round(result.get('confluence_score', 0) or 0, 2),
                'session': result.get('session', 'Unknown'),
                'alert': result.get('alert', False),
            }
            
            profit_results.append(profit_entry)
        
        return profit_results
    
    @staticmethod
    def export_to_csv(results: List[Dict], output_file: Path):
        """Export Profit format to CSV"""
        try:
            profit_results = ProfitFormatter.convert_to_profit_format(results)
            
            if not profit_results:
                print(f"✗ No results to export")
                return False
            
            fieldnames = profit_results[0].keys()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(profit_results)
            
            print(f"✓ Profit CSV exported: {output_file.name}")
            return True
        
        except Exception as e:
            print(f"✗ CSV export error: {e}")
            return False
    
    @staticmethod
    def export_to_json(results: List[Dict], output_file: Path):
        """Export Profit format to JSON"""
        try:
            profit_results = ProfitFormatter.convert_to_profit_format(results)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profit_results, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Profit JSON exported: {output_file.name}")
            return True
        
        except Exception as e:
            print(f"✗ JSON export error: {e}")
            return False
    
    @staticmethod
    def export_to_tsv(results: List[Dict], output_file: Path):
        """Export Profit format to TSV (Tab-Separated Values)"""
        try:
            profit_results = ProfitFormatter.convert_to_profit_format(results)
            
            if not profit_results:
                print(f"✗ No results to export")
                return False
            
            fieldnames = profit_results[0].keys()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
                writer.writeheader()
                writer.writerows(profit_results)
            
            print(f"✓ Profit TSV exported: {output_file.name}")
            return True
        
        except Exception as e:
            print(f"✗ TSV export error: {e}")
            return False
    
    @staticmethod
    def export_comparison_template(output_file: Path):
        """
        Generate a template for Profit manual entry
        For comparing SMC vs Profit outputs side-by-side
        """
        try:
            template_content = """PROFIT vs SMC COMPARISON TEMPLATE
================================================================================

Instructions:
1. Export the same candles from Profit platform
2. Fill in the Profit columns with exact scores from Profit
3. Compare SMC scores against Profit scores
4. Document any divergences

Format:
timestamp | Profit HFZ | SMC HFZ | Diff | Profit FBI | SMC FBI | Diff | ...

================================================================================

COMPARISON MATRIX:

Timestamp,Profit_HFZ,SMC_HFZ,HFZ_Diff,Profit_FBI,SMC_FBI,FBI_Diff,Profit_DTM,SMC_DTM,DTM_Diff,Profit_SDA,SMC_SDA,SDA_Diff,Profit_MTV,SMC_MTV,MTV_Diff,Profit_Signal,SMC_Signal,Signal_Match

"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            print(f"✓ Comparison template created: {output_file.name}")
            return True
        
        except Exception as e:
            print(f"✗ Template creation error: {e}")
            return False

def process_analysis_results(json_file: Path, output_dir: Path = None):
    """Process JSON results and export to Profit formats"""
    
    if not json_file.exists():
        print(f"✗ Results file not found: {json_file}")
        return False
    
    # Determine output directory
    if output_dir is None:
        output_dir = json_file.parent
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Processing: {json_file.name}")
    print(f"💾 Output: {output_dir}")
    
    # Load results
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except Exception as e:
        print(f"✗ Error loading JSON: {e}")
        return False
    
    print(f"✓ Loaded {len(results)} records\n")
    
    # Export to multiple formats
    print("Exporting to Profit formats...")
    
    # CSV format (most compatible)
    csv_output = output_dir / "profit_format.csv"
    ProfitFormatter.export_to_csv(results, csv_output)
    
    # JSON format (for data integration)
    json_output = output_dir / "profit_format.json"
    ProfitFormatter.export_to_json(results, json_output)
    
    # TSV format (alternative)
    tsv_output = output_dir / "profit_format.tsv"
    ProfitFormatter.export_to_tsv(results, tsv_output)
    
    # Comparison template
    template_output = output_dir / "comparison_template.csv"
    ProfitFormatter.export_comparison_template(template_output)
    
    return True

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("PROFIT FORMAT EXPORTER")
    print("="*80)
    
    # Find analysis directories
    if not BATCH_DIR.exists():
        print(f"⚠️  No batch analyses found. Run bulk_analysis.py first.")
        return
    
    analysis_dirs = [d for d in BATCH_DIR.iterdir() if d.is_dir()]
    
    if not analysis_dirs:
        print(f"⚠️  No analysis directories found in {BATCH_DIR}")
        return
    
    print(f"\nFound {len(analysis_dirs)} analysis directories:\n")
    
    # Process each directory
    for analysis_dir in sorted(analysis_dirs):
        json_file = analysis_dir / "results.json"
        
        if json_file.exists():
            print(f"{'='*80}")
            process_analysis_results(json_file, analysis_dir)
    
    # Single file processing (from analysis_results)
    single_file = RESULTS_DIR / "smc_analysis_results.json"
    
    if single_file.exists():
        print(f"\n{'='*80}")
        print("Processing single analysis results...")
        process_analysis_results(single_file, RESULTS_DIR)
    
    print(f"\n{'='*80}")
    print("✅ EXPORT COMPLETE")
    print("="*80)
    print(f"\n📊 Profit format files created:")
    print(f"  • profit_format.csv - Ready for Profit import")
    print(f"  • profit_format.json - For data integration")
    print(f"  • profit_format.tsv - Alternative format")
    print(f"  • comparison_template.csv - For manual validation")
    print(f"\n🔍 Next steps:")
    print(f"  1. Export same data from Profit platform")
    print(f"  2. Use comparison_template.csv to fill in Profit scores")
    print(f"  3. Compare results for accuracy validation")
    print(f"  4. Document any divergences\n")

if __name__ == "__main__":
    main()
