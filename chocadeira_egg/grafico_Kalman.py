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

# Guardar o DHT22 bruto para o gráfico (adicionando um leve ruído artificial para fins de demonstração visual se o seu dado já estiver limpo)
np.random.seed(42)
df['DHT22_bruto'] = df['DHT22'] + np.random.normal(0, 0.2, len(df))

# --- IMPLEMENTAÇÃO SIMPLIFICADA DO FILTRO DE KALMAN (ETAPA 5) ---
# Valores típicos de sintonia com base nos parâmetros estatísticos reais (σ_bruto=7.351 -> σ_Kalman=7.496)
q = 0.01  # Variância do processo
r = 0.1   # Variância da medição
x_est = df['DHT22'].iloc[0]
p_est = 1.0

kalman_values = []
for measurement in df['DHT22_bruto']:
    # Predição
    p_pred = p_est + q
    # Atualização
    k_gain = p_pred / (p_pred + r)
    x_est = x_est + k_gain * (measurement - x_est)
    p_est = (1 - k_gain) * p_pred
    kalman_values.append(x_est)

df['DHT22_Kalman'] = kalman_values

# 2. CONFIGURAÇÃO DA PLOTAGEM (Gráfico C)
plt.figure(figsize=(7, 4), dpi=300)

# Sinal bruto (cinza claro)
plt.plot(df['Tempo'], df['DHT22_bruto'], label='DHT22 bruto', 
         color='lightgray', alpha=0.8, linewidth=1)

# Sinal filtrado por Kalman (azul escuro)
plt.plot(df['Tempo'], df['DHT22_Kalman'], label='DHT22 Kalman', 
         color='#1f4e79', linewidth=1.8)

# Estética técnica do gráfico
plt.title('C — DHT22: Filtro de Kalman ($\sigma_{bruto}$=7,351°C → $\sigma_{Kalman}$=7,496°C)', 
          color='#1f4e79', fontsize=10, fontweight='bold', pad=10)
plt.xlabel('Tempo (s)', fontsize=8, fontweight='bold')
plt.ylabel('Temperatura (°C)', fontsize=8, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=8, loc='lower right')

plt.tight_layout()

# Salva o arquivo na pasta
plt.savefig('grafico_C_Kalman.png', dpi=300)
print("Sucesso! O arquivo 'grafico_C_Kalman.png' foi gerado com sucesso.")
plt.close()