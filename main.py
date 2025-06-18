import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Carregar o conjunto de dados
df = pd.read_csv('dados_voos_novembro.csv', delimiter=';')

# Filtrar apenas voos domésticos no Brasil
df['Pais Origem'] = df['Descrição Aeroporto Origem'].apply(lambda x: x.split(' - ')[-1].strip())
df['Pais Destino'] = df['Descrição Aeroporto Destino'].apply(lambda x: x.split(' - ')[-1].strip())
domestic_flights = df[(df['Pais Origem'] == 'BRASIL') & (df['Pais Destino'] == 'BRASIL')].copy()

# Criar o grafo da malha aérea
G = nx.from_pandas_edgelist(
    domestic_flights,
    source='Sigla ICAO Aeroporto Origem',
    target='Sigla ICAO Aeroporto Destino',
    create_using=nx.Graph()
)

# Encontrar a maior componente conectada do grafo
largest_component_nodes = max(nx.connected_components(G), key=len)
G_connected = G.subgraph(largest_component_nodes).copy()

# Calcular o impacto da remoção de cada aeroporto
initial_size = len(G_connected)
airport_impact = {}
for airport in G_connected.nodes():
    G_temp = G_connected.copy()
    G_temp.remove_node(airport)
    if G_temp.nodes:
        new_size = len(max(nx.connected_components(G_temp), key=len))
        impact = initial_size - 1 - new_size
        airport_impact[airport] = impact
    else:
        airport_impact[airport] = initial_size - 1

# Ordenar os aeroportos pelo impacto
critical_airports_ranked = sorted(airport_impact.items(), key=lambda item: item[1], reverse=True)

# --- Visualização do Grafo ---

# Pegar os 5 aeroportos mais críticos
top_5_critical_airports = [airport for airport, impact in critical_airports_ranked[:5]]

# Definir cores e tamanhos para os nós
node_colors = ['#FF5733' if node in top_5_critical_airports else '#A2D9CE' for node in G_connected.nodes()]
node_sizes = [1200 if node in top_5_critical_airports else 300 for node in G_connected.nodes()]

# Configurar o plot
plt.figure(figsize=(20, 20))
plt.title('Grafo da Malha Aérea Brasileira com os 5 Aeroportos Mais Críticos', fontsize=20)

# Desenhar o grafo
pos = nx.spring_layout(G_connected, seed=42) # Usar um layout que distribui bem os nós
nx.draw_networkx_edges(G_connected, pos, alpha=0.5, edge_color='gray')

# Desenhar os nós
nx.draw_networkx_nodes(G_connected, pos, node_color=node_colors, node_size=node_sizes)

# Adicionar labels apenas aos 5 aeroportos mais críticos para não poluir o gráfico
labels = {node: node for node in top_5_critical_airports}
nx.draw_networkx_labels(G_connected, pos, labels=labels, font_size=14, font_weight='bold')

# Criar a legenda
critical_patch = mpatches.Patch(color='#FF5733', label='Top 5 Aeroportos Críticos')
other_patch = mpatches.Patch(color='#A2D9CE', label='Outros Aeroportos')
plt.legend(handles=[critical_patch, other_patch], loc='upper right', fontsize=14)

# Carregar o conjunto de dados de voos
df_flights = pd.read_csv('dados_voos_novembro.csv', delimiter=';')

# Filtrar apenas voos domésticos no Brasil
df_flights['Pais Origem'] = df_flights['Descrição Aeroporto Origem'].apply(lambda x: x.split(' - ')[-1].strip())
df_flights['Pais Destino'] = df_flights['Descrição Aeroporto Destino'].apply(lambda x: x.split(' - ')[-1].strip())
domestic_flights = df_flights[(df_flights['Pais Origem'] == 'BRASIL') & (df_flights['Pais Destino'] == 'BRASIL')].copy()

# Encontrar os 5 aeroportos mais movimentados (pousos + decolagens)
all_traffic = pd.concat([domestic_flights['Sigla ICAO Aeroporto Origem'], domestic_flights['Sigla ICAO Aeroporto Destino']])
busiest_airports_ranked = all_traffic.value_counts().nlargest(5)

# Imprimir o resultado da análise
print("--- Top 5 Aeroportos Mais Movimentados (ICAO e Contagem de Voos) ---")
print(busiest_airports_ranked)

# Carregar o conjunto de dados de voos
print("Carregando e analisando dados...")
df_flights = pd.read_csv('dados_voos_novembro.csv', delimiter=';')

# Filtrar apenas voos domésticos no Brasil
df_flights['Pais Origem'] = df_flights['Descrição Aeroporto Origem'].apply(lambda x: x.split(' - ')[-1].strip())
df_flights['Pais Destino'] = df_flights['Descrição Aeroporto Destino'].apply(lambda x: x.split(' - ')[-1].strip())
domestic_flights = df_flights[(df_flights['Pais Origem'] == 'BRASIL') & (df_flights['Pais Destino'] == 'BRASIL')].copy()

# Encontrar os 5 aeroportos mais movimentados (pousos + decolagens)
all_traffic = pd.concat([domestic_flights['Sigla ICAO Aeroporto Origem'], domestic_flights['Sigla ICAO Aeroporto Destino']])
busiest_airports_ranked = all_traffic.value_counts().nlargest(5)

print("\n--- Análise dos 5 Aeroportos Mais Movimentados ---")

# Iterar sobre os resultados para imprimir uma mensagem detalhada para cada um
for i, (icao_code, flight_count) in enumerate(busiest_airports_ranked.items(), 1):
    # O número representa o total de voos (pousos e decolagens) registrados no arquivo para aquele aeroporto.
    print(f"{i}º Aeroporto: {icao_code} | Total de {flight_count} operações (pousos e decolagens).")