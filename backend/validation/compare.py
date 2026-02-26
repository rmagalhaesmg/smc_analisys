"""
Validation script to compare Profit outputs with SMC Web App results.

Usage:
    python compare.py profit.csv app.csv --output report_folder

Generates:
  - HTML/Markdown technical report
  - divergence graph (PNG)
  - CSV list of failures

Metrics compared candle-by-candle:
  HFZScore, FBIScore, DTMScore, SDAScore, MTVScore, FinalScore
  Regime, Trap flag, Recommendation

Criteria:
  - Difference <= 2% is acceptable
  - Regime mismatch is error
  - Trap mismatch is critical error
  - Opposite recommendation is critical error

Exports a summary and detailed discrepancies.
"""

import argparse
import os
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


CRITICAL_COLUMNS = [
    'Regime',
    'TrapFlag',
    'Recommendation',
]

NUMERIC_COLUMNS = [
    'HFZScore', 'FBIScore', 'DTMScore', 'SDAScore', 'MTVScore', 'FinalScore'
]


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df


def compare_rows(row_profit, row_app):
    result = {'timestamp': row_profit['timestamp']}
    # numeric differences in percent
    for col in NUMERIC_COLUMNS:
        p = row_profit.get(col, np.nan)
        a = row_app.get(col, np.nan)
        if pd.isna(p) or pd.isna(a):
            diff = np.nan
        else:
            diff = abs(a - p) / (p if p != 0 else 1) * 100
        result[col] = a
        result[f'{col}_profit'] = p
        result[f'{col}_diff_pct'] = diff
    # categorical checks
    for col in CRITICAL_COLUMNS:
        p = row_profit.get(col, None)
        a = row_app.get(col, None)
        result[col] = a
        result[f'{col}_profit'] = p
        result[f'{col}_match'] = (p == a)
    return result


def generate_report(profit_csv: str, app_csv: str, output: str):
    profit_df = load_data(Path(profit_csv))
    app_df = load_data(Path(app_csv))

    # align on timestamp
    merged = pd.merge(
        profit_df, app_df, on='timestamp', how='inner', suffixes=('_profit', '_app')
    )
    results = []
    for _, row in merged.iterrows():
        r = compare_rows(row[[c + '_profit' for c in NUMERIC_COLUMNS + CRITICAL_COLUMNS]].rename(lambda x: x.replace('_profit','')),
                         row[[c + '_app' for c in NUMERIC_COLUMNS + CRITICAL_COLUMNS]].rename(lambda x: x.replace('_app','')))
        results.append(r)
    report_df = pd.DataFrame(results)

    # compute metrics
    summary = {}
    for col in NUMERIC_COLUMNS:
        summary[f'{col}_avg_diff_pct'] = report_df[f'{col}_diff_pct'].mean()
        summary[f'{col}_max_diff_pct'] = report_df[f'{col}_diff_pct'].max()

    # flags
    summary['regime_mismatch'] = (~report_df['Regime_match']).sum()
    summary['trap_mismatch'] = (~report_df['TrapFlag_match']).sum()
    summary['reco_mismatch'] = (~report_df['Recommendation_match']).sum()

    # save detailed failures
    failures = report_df[
        (report_df['Regime_match'] == False) |
        (report_df['TrapFlag_match'] == False) |
        (report_df['Recommendation_match'] == False) |
        (report_df[[f'{c}_diff_pct' for c in NUMERIC_COLUMNS]] > 2).any(axis=1)
    ]
    os.makedirs(output, exist_ok=True)
    report_df.to_csv(Path(output) / 'comparison_full.csv', index=False)
    failures.to_csv(Path(output) / 'failures.csv', index=False)

    # generate divergence graph
    fig, axs = plt.subplots(len(NUMERIC_COLUMNS), 1, figsize=(10, 4 * len(NUMERIC_COLUMNS)))
    for i, col in enumerate(NUMERIC_COLUMNS):
        axs[i].plot(report_df['timestamp'], report_df[f'{col}_profit'], label='Profit', alpha=0.7)
        axs[i].plot(report_df['timestamp'], report_df[col], label='App', alpha=0.7)
        axs[i].set_title(col)
        axs[i].legend()
        axs[i].tick_params(axis='x', rotation=45)
    fig.tight_layout()
    fig.savefig(Path(output) / 'divergences.png')

    # text summary
    with open(Path(output) / 'report.txt', 'w') as f:
        f.write('SUMMARY REPORT\n')
        f.write('=' * 40 + '\n')
        for k, v in summary.items():
            f.write(f'{k}: {v}\n')
        f.write('\nTotal candles compared: ' + str(len(report_df)) + '\n')
        f.write('Total failures: ' + str(len(failures)) + '\n')

    print(f'Report generated in {output}')
    return summary, report_df, failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare Profit vs App outputs')
    parser.add_argument('profit_csv', help='CSV export from Profit guidance')
    parser.add_argument('app_csv', help='CSV export from backend results')
    parser.add_argument('--output', '-o', default='validation_report', help='Folder to store report')
    args = parser.parse_args()
    generate_report(args.profit_csv, args.app_csv, args.output)
