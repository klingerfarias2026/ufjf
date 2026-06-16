import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. ETAPA 1: Ingestão e limpeza padrão
df = pd.read_csv('dados.csv', encoding='latin1', skiprows=1, sep=';',
                 names=['Tempo','DHT22','LM35','Termopar_K','DS18B20',
                        'Setpoint','Erro','Acao_controle'])
df = df[df['Tempo'] != 'Tempo'].copy()

# Conversão explícita das variáveis do bloco de controle
df['Erro'] = pd.to_numeric(df['Erro'].astype(str).str.replace('°C', '', regex=False).str.strip(), errors='coerce')
df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df = df.dropna(subset=['Tempo', 'Erro']).reset_index(drop=True)

# 2. CONFIGURAÇÃO DA PLOTAGEM DO ERRO (Gráfico F)
plt.figure(figsize=(10, 4), dpi=300)

# Preenchimento Bicolor do Erro
# Laranja para Erro Positivo (Abaixo do Setpoint)
plt.fill_between(df['Tempo'], df['Erro'], where=(df['Erro'] >= 0), 
                 color='sandybrown', alpha=0.6, label='Erro+ (Abaixo do Setpoint)')

# Azul para Erro Negativo (Acima do Setpoint / Sobresinal ou Ajuste)
plt.fill_between(df['Tempo'], df['Erro'], where=(df['Erro'] < 0), 
                 color='lightsteelblue', alpha=0.6, label='Erro- (Acima do Setpoint)')

# Linha de referência no Erro zero (Estabilização perfeita)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)

# Estética técnica e rigorosa
plt.title('F — Erro de Controle (Setpoint 50°C − Temperatura DHT22): 913 amostras reais', 
          color='#1f4e79', fontsize=10, fontweight='bold', pad=10)
plt.xlabel('Tempo (s)', fontsize=8, fontweight='bold')
plt.ylabel('Erro (°C)', fontsize=8, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=8, loc='lower left')

plt.tight_layout()

# Salva o arquivo na pasta
plt.savefig('grafico_F_Erro.png', dpi=300)
print("Sucesso! O arquivo 'grafico_F_Erro.png' foi gerado.")
plt.close()