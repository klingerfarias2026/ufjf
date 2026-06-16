import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. ETAPA 1: Ingestão e limpeza padrão
df = pd.read_csv('dados.csv', encoding='latin1', skiprows=1, sep=';',
                 names=['Tempo','DHT22','LM35','Termopar_K','DS18B20',
                        'Setpoint','Erro','Acao_controle'])
df = df[df['Tempo'] != 'Tempo'].copy()

# Garantir a conversão correta da coluna de ação de controle
df['Acao_controle'] = pd.to_numeric(df['Acao_controle'], errors='coerce')
df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df = df.dropna(subset=['Tempo', 'Acao_controle']).reset_index(drop=True)

# 2. CONFIGURAÇÃO DA PLOTAGEM DA AÇÃO PWM (Gráfico E)
plt.figure(figsize=(7, 4), dpi=300)

# Preenchimento de área da ação de controle (Laranja/Sienna suave)
plt.fill_between(df['Tempo'], df['Acao_controle'], color='sandybrown', alpha=0.7, 
                 label='PWM (Ação de Controle)')

# Linha tracejada de saturação máxima (PWM = 255)
plt.axhline(255, color='red', linestyle='--', linewidth=1.2, label='PWM máx = 255')

# Anotação descritiva da saturação (318 amostras / 34,8% do tempo total)
plt.annotate('318 amostras\n(34,8%) em PWM=255', xy=(120, 255), xytext=(150, 210),
             arrowprops=dict(arrowstyle='->', color='red', linewidth=1))

# Estética técnica do gráfico
plt.title('E — Ação de Controle PWM (0-255): Fase de Aquecimento', 
          color='#1f4e79', fontsize=10, fontweight='bold', pad=10)
plt.xlabel('Tempo (s)', fontsize=8, fontweight='bold')
plt.ylabel('PWM', fontsize=8, fontweight='bold')
plt.ylim(-10, 285)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=8, loc='center left')

plt.tight_layout()

# Salva o arquivo na pasta
plt.savefig('grafico_E_PWM.png', dpi=300)
print("Sucesso! O arquivo 'grafico_E_PWM.png' foi gerado.")
plt.close()