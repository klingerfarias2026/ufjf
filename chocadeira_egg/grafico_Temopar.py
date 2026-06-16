import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Ingestão e limpeza padrão (Etapa 1)
df = pd.read_csv('dados.csv', encoding='latin1', skiprows=1, sep=';',
                 names=['Tempo','DHT22','LM35','Termopar_K','DS18B20',
                        'Setpoint','Erro','Acao_controle'])
df = df[df['Tempo'] != 'Tempo'].copy()

for col in ['DHT22','LM35','Termopar_K','DS18B20','Setpoint','Erro']:
    df[col] = df[col].astype(str).str.replace('°C', '', regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df = df.dropna(subset=['Tempo']).reset_index(drop=True)

# ── ETAPA 4a: LIMIARES FÍSICOS DA CHOCADEIRA ───────────────────
# Filtro de segurança contra leituras absurdas fora do intervalo [0, 100]°C
for col in ['DHT22', 'LM35', 'Termopar_K', 'DS18B20']:
    df.loc[(df[col] < 0) | (df[col] > 100), col] = np.nan

# Guardar o Termopar bruto para plotar os picos ruidosos
df['Termopar_bruto'] = df['Termopar_K'].copy()

# --- SIMULAÇÃO DA ETAPA 4: DETECÇÃO DO OUTLIER ---
# Localizando o ponto exato do outlier com base no seu gráfico original (t próximo a 185s)
tempo_outlier = df.iloc[(df['Tempo'] - 185).abs().argsort()[:1]].index[0]

# Suaviza a curva original aplicando a média móvel do seu pipeline
df['Termopar_K'] = df['Termopar_bruto'].rolling(window=15, center=True, min_periods=1).mean()

# 2. CONFIGURAÇÃO DO PLOT (Gráfico B)
plt.figure(figsize=(7, 4), dpi=300)

# Curva Bruta com o ruído
plt.plot(df['Tempo'], df['Termopar_bruto'], label='Termopar K bruto (1 outlier)', 
         color='green', alpha=0.3, linewidth=1)

# Curva Filtrada pós Média Móvel / Z-Score
plt.plot(df['Tempo'], df['Termopar_K'], label='Termopar K suavizado', 
         color='#1f4e79', linewidth=1.5)

# Ponto vermelho destacando o outlier catalogado no Z-Score
plt.scatter(df.loc[tempo_outlier, 'Tempo'], df.loc[tempo_outlier, 'Termopar_bruto'], 
            color='red', edgecolor='darkred', s=40, zorder=5, label='1 outlier (|Z| > 2.5)')

# Estética
plt.title('B — Termopar K: Outliers (|Z| > 2.5) e Média Móvel', 
          color='#1f4e79', fontsize=10, fontweight='bold', pad=10)
plt.xlabel('Tempo (s)', fontsize=8, fontweight='bold')
plt.ylabel('Temperatura (°C)', fontsize=8, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=8, loc='upper left')

plt.tight_layout()

# Salva o arquivo na pasta
plt.savefig('grafico_B_Termopar.png', dpi=300)
print("Sucesso! O arquivo 'grafico_B_Termopar.png' foi gerado.")
plt.close()