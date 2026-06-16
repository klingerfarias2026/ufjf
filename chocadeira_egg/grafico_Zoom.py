import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. ETAPA 1: Ingestão e limpeza padrão
df = pd.read_csv('dados.csv', encoding='latin1', skiprows=1, sep=';',
                 names=['Tempo','DHT22','LM35','Termopar_K','DS18B20',
                        'Setpoint','Erro','Acao_controle'])
df = df[df['Tempo'] != 'Tempo'].copy()

for col in ['DHT22','LM35','Termopar_K','DS18B20','Setpoint','Erro']:
    df[col] = df[col].astype(str).str.replace('°C', '', regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df = df.dropna(subset=['Tempo']).reset_index(drop=True)

# 2. Aplicação rápida das Etapas 2 e 3 no LM35 para o gráfico ficar correto
df.loc[df['LM35'] < 10, 'LM35'] = np.nan
df['LM35'] = df['LM35'].interpolate(method='linear')

# Suavização leve no Termopar K para bater com o seu pipeline (Etapa 4)
df['Termopar_K'] = df['Termopar_K'].rolling(window=11, center=True, min_periods=1).mean()

# 3. CONFIGURAÇÃO DA PLOTAGEM COM ZOOM (Gráfico D)
plt.figure(figsize=(7, 4.5), dpi=300)

# Plotagem das curvas de todos os sensores pós-pipeline
plt.plot(df['Tempo'], df['DHT22'], label='DHT22', color='tab:blue', linewidth=1.8)
plt.plot(df['Tempo'], df['LM35'], label='LM35', color='darkgoldenrod', linewidth=1.5)
plt.plot(df['Tempo'], df['Termopar_K'], label='Termopar K [suav.]', color='darkgreen', linewidth=1.2)
plt.plot(df['Tempo'], df['DS18B20'], label='DS18B20', color='brown', linewidth=1.5)

# Destacar a região da perturbação (Abertura da tampa)
plt.axvspan(220, 260, color='red', alpha=0.08)

# Aplicar o Zoom na janela temporal do evento (conforme o seu painel original)
plt.xlim(200, 280)
plt.ylim(41, 50.5)

# Anotação descritiva com seta apontando a dinâmica do sistema
plt.annotate('Queda térmica\n~4-5°C em 40s', xy=(231, 44.5), xytext=(208, 41.8),
             arrowprops=dict(arrowstyle='->', color='red', linewidth=1))

# Estética técnica
plt.title('D — Zoom: Queda Térmica em t ≈ 220-260 s (todos os sensores)', 
          color='#1f4e79', fontsize=10, fontweight='bold', pad=10)
plt.xlabel('Tempo (s)', fontsize=8, fontweight='bold')
plt.ylabel('Temperatura (°C)', fontsize=8, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=8, loc='lower right')

plt.tight_layout()

# Salva o arquivo na pasta
plt.savefig('grafico_D_Zoom.png', dpi=300)
print("Sucesso! O arquivo 'grafico_D_Zoom.png' foi gerado.")
plt.close()