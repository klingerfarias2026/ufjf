import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Carrega o arquivo tratando o cabeçalho do PuTTY
df = pd.read_csv('dados.csv', encoding='latin-1', sep=';', skiprows=1)

sensores = ['DHT22', 'Termopar_K']
for col in sensores:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace('°C', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove nulos para calcular a variação consecutiva estável
df_clean = df[sensores].dropna()

# 2. Configuração do estilo visual
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(7, 5.5))

# Cálculo do ruído consecutivo |X_k - X_{k-1}|
ruido_dht22 = np.abs(df_clean['DHT22'].diff().dropna())
ruido_tk = np.abs(df_clean['Termopar_K'].diff().dropna())

bins = np.arange(0, 1.4, 0.1)

ax.hist([ruido_dht22, ruido_tk], bins=bins, alpha=0.7, 
        color=['#729ece', '#849b7d'], 
        label=['DHT22 (σ=0.122°C)', 'Termopar K (σ=0.241°C)'],
        rwidth=0.8)

ax.set_title('Histograma de Variação\nConsecutiva (ruído)', 
             fontsize=12, fontweight='bold', color='#1d4e77', pad=15)
ax.set_xlabel('|ΔT| entre amostras (°C)', fontsize=10)
ax.set_ylabel('Frequência', fontsize=10)
ax.legend(frameon=True, facecolor='white', edgecolor='none')
ax.grid(linestyle='-', alpha=0.3)
ax.set_facecolor('#f8faff')

plt.tight_layout()
plt.savefig('grafico_2_histograma.png', dpi=300)
plt.show()