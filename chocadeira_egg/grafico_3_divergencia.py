import pandas as pd
import matplotlib.pyplot as plt

# 1. Carrega o arquivo tratando o cabeçalho do PuTTY
df = pd.read_csv('dados.csv', encoding='latin-1', sep=';', skiprows=1)

# Limpeza rigorosa de strings e conversão para numérico
all_sensors = ['DHT22', 'LM35', 'Termopar_K', 'DS18B20']
for col in all_sensors:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace('°C', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove linhas onde a referência essencial (DHT22) tenha falhado
df = df.dropna(subset=['DHT22'])

# Correção da Etapa 3 (Domínio LM35 t=0): Remove o zero inicial espúrio para o gráfico não quebrar a escala
df.loc[df['LM35'] == 0, 'LM35'] = df['DHT22']

# Geração da série suavizada para manter a fidelidade visual do gráfico original (Etapa 5)
df['TK_suav'] = df['Termopar_K'].rolling(window=15, min_periods=1).mean()

# 2. Configuração do estilo visual
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(8, 5.5))

# Define o eixo dinâmico de tempo (usando o índice de amostras para casar com o seu original)
tempo = df.index 

# Cálculo das divergências em relação ao referencial (DHT22)
div_lm35 = df['LM35'] - df['DHT22']
div_tk = df['TK_suav'] - df['DHT22']
div_ds = df['DS18B20'] - df['DHT22']

# Plotagem das linhas com as cores idênticas às originais
ax.plot(tempo, div_lm35, color='#e19d53', label='LM35 – DHT22', linewidth=1.2)
ax.plot(tempo, div_tk, color='#849b7d', label='TK_suav – DHT22', linewidth=1.2)
ax.plot(tempo, div_ds, color='#cd6263', label='DS18B20 – DHT22', linewidth=1.2)

# Linha de referência no zero e Região de Tolerância de +-0.5°C
ax.axhline(0, color='black', linestyle='--', linewidth=1.5)
ax.axhspan(-0.5, 0.5, color='#e2ede4', alpha=0.4, label='Tolerância ±0,5°C')

# Customização fina dos eixos e títulos
ax.set_title('Divergência de cada sensor\nem relação ao DHT22', 
             fontsize=12, fontweight='bold', color='#1d4e77', pad=15)
ax.set_xlabel('Tempo (s)', fontsize=10)
ax.set_ylabel('Diferença (°C)', fontsize=10)
ax.legend(loc='lower left', frameon=True, facecolor='white')
ax.grid(linestyle='-', alpha=0.3)
ax.set_facecolor('#f8faff')

plt.tight_layout()
plt.savefig('grafico_3_divergencia.png', dpi=300)
plt.show()