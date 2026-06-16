import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. ETAPA 1: Ingestão e limpeza estrutural do dados.csv
df = pd.read_csv('dados.csv', encoding='latin1', skiprows=1, sep=';',
                 names=['Tempo','DHT22','LM35','Termopar_K','DS18B20',
                        'Setpoint','Erro','Acao_controle'])
df = df[df['Tempo'] != 'Tempo'].copy()

# Remove caracteres residuais e converte para numérico para salvar a curva bruta
df['LM35_bruto'] = pd.to_numeric(df['LM35'].astype(str).str.replace('°C', '', regex=False).str.strip(), errors='coerce')

for col in ['DHT22','LM35','Termopar_K','DS18B20','Setpoint','Erro']:
    df[col] = df[col].astype(str).str.replace('°C', '', regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df = df.dropna(subset=['Tempo']).reset_index(drop=True)

# 2. ETAPA 2: Regra de domínio (Fazer o t=0 virar NaN para a interpolação)
df.loc[df['LM35'] < 10, 'LM35'] = np.nan

# 3. ETAPA 3: Interpolação linear para preencher o t=0 e a lacuna de 66 NaN
df['LM35'] = df['LM35'].interpolate(method='linear')


# 4. PLOTAGEM DO GRÁFICO A
plt.figure(figsize=(10, 4), dpi=300)

# Curva bruta (laranja) - mostrando o zero e a falha
plt.plot(df['Tempo'], df['LM35_bruto'], label='LM35 bruto', color='orange', alpha=0.6, linewidth=1.2)

# Curva corrigida (azul) - após tratamento
plt.plot(df['Tempo'], df['LM35'], label='LM35 interpolado', color='tab:blue', linewidth=1.5)

# Destacar a região da lacuna crônica de NaN
plt.axvspan(70.2, 89.7, color='red', alpha=0.12, label='Lacuna NaN (t=70.2-89.7 s)')

# Anotações em texto apontando as falhas com setas
plt.annotate('LM35=0.00°C\n(mau contato t=0)', xy=(0, 0), xytext=(15, 6),
             arrowprops=dict(arrowstyle='->', color='red', linewidth=1))

plt.annotate('66 NaN\n(19.5 s)', xy=(80, 42), xytext=(95, 33),
             arrowprops=dict(arrowstyle='->', color='red', linewidth=1))

# Formatação estética do gráfico
plt.title('A — LM35: Mau Contato (t=0) e Lacuna de 66 NaN (t=70-90 s) → Interpolação Linear', 
          color='#1f4e79', fontsize=10, fontweight='bold', pad=10)
plt.xlabel('Tempo (s)', fontsize=8, fontweight='bold')
plt.ylabel('Temperatura (°C)', fontsize=8, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=8, loc='lower right')

plt.tight_layout()

# Salva a imagem na mesma pasta do script
plt.savefig('grafico_A_LM35.png', dpi=300)
print("Sucesso! O arquivo 'grafico_A_LM35.png' foi gerado na pasta do projeto.")
plt.close()