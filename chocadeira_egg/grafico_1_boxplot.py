import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carrega o arquivo tratando o cabeçalho do PuTTY
df = pd.read_csv('dados.csv', encoding='latin-1', sep=';', skiprows=1)

# Mapeia as colunas exatas encontradas no seu cabeçalho real
sensores = ['DHT22', 'LM35', 'Termopar_K', 'DS18B20']

# Garante a limpeza rigorosa de strings e converte estritamente para float
for col in sensores:
    if col in df.columns:
        # Remove "°C", espaços em branco e substitui vírgula por ponto se houver
        df[col] = df[col].astype(str).str.replace('°C', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove linhas onde os sensores principais estejam totalmente nulos (limpeza de segurança)
df_box = df[sensores].dropna(how='all')

# 2. Configuração do estilo visual
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(7, 5.5))

cores = ['#729ece', '#e19d53', '#849b7d', '#cd6263']

# Plotagem do Boxplot forçando a conversão explícita para float do numpy
sns.boxplot(data=df_box.astype(float), palette=cores, width=0.5, 
            medianprops=dict(color="black", linewidth=2.5), ax=ax)

# Customização dos eixos e títulos
ax.set_title('Distribuição por Sensor\n(inclui outliers e mau contato)', 
             fontsize=12, fontweight='bold', color='#1d4e77', pad=15)
ax.set_ylabel('Temperatura (°C)', fontsize=10)
ax.grid(axis='y', linestyle='-', alpha=0.3)
ax.set_facecolor('#f8faff')

# Ajusta os limites do eixo Y automaticamente baseado nos dados reais para não sumir com o gráfico
ax.relim()
ax.autoscale_view()

plt.tight_layout()
plt.savefig('grafico_1_boxplot.png', dpi=300)
plt.show()