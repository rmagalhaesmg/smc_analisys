"""Convert Profit CSV to SMC analysis format"""
import pandas as pd
from pathlib import Path

# Read the Profit CSV
csv_file = r'C:\Users\Usuário\Desktop\SMC_MTV.csv'
df = pd.read_csv(csv_file, encoding='utf-8')

print('📊 Converting Profit data to SMC format...\n')
print(f'Original: {len(df)} rows, {len(df.columns)} columns')

# Create processed DataFrame with SMC column names
processed = pd.DataFrame()

# Create timestamp from Data and Hora
processed['timestamp'] = pd.to_datetime(
    df['Data'] + ' ' + df['Hora'],
    format='%d/%m/%Y %H:%M:%S'
).dt.strftime('%Y-%m-%d %H:%M:%S')

# Map price columns (Portuguese → English)
processed['open'] = df['Abertura'].astype(float)
processed['high'] = df['Máximo'].astype(float)
processed['low'] = df['Mínimo'].astype(float)
processed['close'] = df['Último'].astype(float)
processed['volume'] = df['Volume'].astype('int64')
processed['trades'] = df['Negócios'].astype('int64')

print(f'\n✓ Converted: {len(processed)} rows')
print(f'✓ Columns: {list(processed.columns)}')
print(f'\n📅 Data Range:')
print(f'  From: {processed["timestamp"].min()}')
print(f'  To:   {processed["timestamp"].max()}')

print(f'\n📊 Sample Row:')
for col in processed.columns:
    print(f'  {col}: {processed[col].iloc[0]}')

# Save to uploads folder
output_file = Path('uploads/SMC_MTV_processed.csv')
output_file.parent.mkdir(parents=True, exist_ok=True)
processed.to_csv(output_file, index=False)

print(f'\n✅ Saved: {output_file}')
print(f'✅ Ready for bulk analysis!')
