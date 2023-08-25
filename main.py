import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import re

Graph = nx.Graph()

# retorna umm dicionário associando cada político com seu respectivo partido
def read_file_by_political_party(file_name, p_party):
    selected_parties = set(p_party.split(" "))
    politicians_by_party = {}
    with open(file_name, 'r', encoding = 'utf-8') as file:
        i = 0
        for line in file:
            i += 1
            line_content = line.strip().split(";")
            politician_name = line_content[0]
            party_name = line_content[1]
            if (not selected_parties or party_name in selected_parties) or p_party == "":
                if politician_name not in politicians_by_party:
                    politicians_by_party[politician_name] = []
                politicians_by_party[politician_name].append(party_name)
        file.close()
    return politicians_by_party

# cria o grafo a partir do txt do grafo e os políticos por partido
def read_file(G, file_name, politicians_by_party):
    with open(file_name, 'r', encoding = 'utf-8') as file:
        i = 0
        for line in file:
            i += 1
            line_content = line.strip().split(";")
            u = line_content[0]
            v = line_content[1]
            w = int(line_content[2])
            if u in politicians_by_party and v in politicians_by_party:
                # Concatena os partidos com os nomes dos deputados para criar os nós
                u_with_party = f"({', '.join(politicians_by_party[u])}) {u}"
                v_with_party = f"({', '.join(politicians_by_party[v])}) {v}"
                G.add_edge(u_with_party, v_with_party, weight=w)
        file.close()

# retorna um dicionário com o número de voto de cada político, o que é útil para a normalização do grafo
def read_votes_data(file_path, p_party1):
    selected_parties = set(p_party1.split(" "))
    votes_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split(';')
            if len(fields) == 3:
                politician_name, p_party, votes = fields
                if p_party in selected_parties or p_party1 == "":
                    politician_name = f"({p_party}) {politician_name}"
                    votes_dict[politician_name] = int(votes)
    return votes_dict

# normaliza o grafo 
def normalize_graph(G, votes_dict):
    # campo 'data' é um atributo que é utilizado para acessar especificadamente o campo de peso de cada aresta
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        min_votes = min(votes_dict[u], votes_dict[v])
        normalized_weight = weight / min_votes
        # normalized_weight = round(normalized_weight, 3) # arredondamento para 3 casas decimais
        G.add_edge(u, v, weight=normalized_weight)

# threshold de 0.9 será utilizado
def threshold(G, threshold):
    # criação de uma lista para remoção de arestas, caso removesse diretamente do grafo, o grafo seria modificado durante a iteração
    # erro de runtime -> RuntimeError: dictionary changed size during iteration 
    edges_to_remove = []
    for u, v, data in G.edges(data=True):
        if data['weight'] < threshold:
            edges_to_remove.append((u, v))
    # aqui usamos remove_edges_from para remover as arestas da lista criada anteriormente
    G.remove_edges_from(edges_to_remove)

def inversion_of_weights(G):
    for u, v, data in G.edges(data=True):
        data['weight'] = 1 - data['weight']

# Inverte a cor hexadecimal, para cores não ficar muito semelhante
def invert_hex(content):
    text = content.group(1).lower()
    code = {}
    l1="0123456789abcdef"
    l2="fedcba9876543210"
    for i in range(len(l1)):
        code[l1[i]]=l2[i]
    inverted = ""
    for j in text:
        inverted += code[j]
    return '#{}'.format(inverted)

# Associa uma cor aleatoria a cada partido, útil para coloração dos nós
def create_dict_colors():
    politicians_by_party = read_file_by_political_party(politicians_path, p_party)
    values = list(politicians_by_party.values())
    result = []
    re_hex = re.compile("#([0-9a-f]{3,6})(\W)?", re.IGNORECASE)
    for i in values: 
        if i not in result:
            result.append(i)
    colors = []
    for i in range(len(result)):
        if (i % 2 == 0):
            colors.append("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
        else:
            colors.append(re_hex.sub(invert_hex, "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])))
    dict_colors = {}
    for i in range(len(result)):
        for j in result[i]:
            dict_colors[j] = colors[i]
    return dict_colors

def create_betwenness(Graph, year, p_party):
    
    betweenness_centrality = nx.betweenness_centrality(Graph)
    
    nodes, centralities = zip(*sorted(betweenness_centrality.items(), key=lambda item: item[1]))
    
    # Plotar o grafico de barras
    plt.figure(figsize=(25, 17))
    plt.bar(nodes, centralities)
    plt.xlabel("Deputados")
    plt.ylabel("Betweenness")
    plt.title("Medida de Centralidade")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if len(p_party) == 0:
        plt.savefig(f"betwenness_/betwenness_{year}_ALL.png")
    else:
        p_party = p_party.replace(' ','_')
        plt.savefig(f"betwenness_/betwenness_{year}_{p_party}.png")

# Criando heatmap em ordem alfabética, tanto de partido quanto deputado
def create_heatmap(Graph, year, p_party):
    # Chamando novamente (5 linhas abaixo) para que o threshold e inversão não afete o heatmap
    graph_path = "datasets/graph" + year + ".txt"
    politicians_path = "datasets/politicians" + year + ".txt"
    read_file(Graph, graph_path, read_file_by_political_party(politicians_path, p_party))
    print(Graph)
    normalize_graph(Graph, read_votes_data(politicians_path, p_party))
    
    my_edges = list(Graph.edges(data=True))
    my_edges.sort()
    
    sorted_nodes = sorted(Graph.nodes())

    num_nodes = len(sorted_nodes)
    adj_matrix = np.zeros((num_nodes, num_nodes))
    # Preencher a matriz com os pesos das arestas do grafo
    for u, v, data in my_edges:
        u_idx = sorted_nodes.index(u)
        v_idx = sorted_nodes.index(v)
        adj_matrix[u_idx][v_idx] = data['weight']
        adj_matrix[v_idx][u_idx] = data['weight']  # A matriz é simétrica para grafos não direcionados

    # Criar o heatmap usando o Matplotlib
    plt.figure(figsize=(25, 21))
    plt.imshow(adj_matrix, cmap='hot', origin='upper')
    plt.colorbar(label='Peso das Arestas')
    plt.xticks(ticks=np.arange(num_nodes), labels=sorted_nodes, rotation=45, ha = 'right')
    plt.yticks(ticks=np.arange(num_nodes), labels=sorted_nodes)
    plt.tight_layout()
    
    if len(p_party) == 0:
        plt.savefig(f"heatmap_/heatmap_{year}_ALL.png")
    else:
        p_party = p_party.replace(' ','_')
        plt.savefig(f"heatmap_/heatmap_{year}_{p_party}.png")

def create_graph(Graph, year, p_party):
    random.seed(42)
    nodes_to_remove = [node for node in Graph.nodes() if Graph.degree(node) == 0]

    # Remover os nós com grau zero
    for node in nodes_to_remove:
        Graph.remove_node(node)

    # Conf. layout do grafo
    pos = nx.spring_layout(Graph)

    plt.subplots(figsize=(25, 21))  # (largura, altura)
    
    dict_colors = create_dict_colors()
    colors = []
    for node in Graph.nodes():
        partido = ""
        for i in node:
            if (i == '('):
                continue
            elif (i == ')'):
                break
            else:
                 partido += i
        colors.append(dict_colors[partido])
    
    layout = nx.spring_layout(Graph, k=0.15)
    
    # Desenha o grafo
    nx.draw(Graph, pos = layout, with_labels=True, node_size=400, node_color=colors, font_size=10, font_color='black', font_weight='bold')
    
    if len(p_party) == 0:
        plt.savefig(f"graph_/graph_{year}_ALL.png")
    else:
        p_party = p_party.replace(' ','_')
        plt.savefig(f"graph_/graph_{year}_{p_party}.png")

if __name__ == '__main__':
    year = input("Informe o ano a considerar ( de 2001 a 2023) : ")
    p_party = input("Informe os partidos a analisar , separados por espaço ( ex . PT MDB PL ) : ")
    threshold_idx = float(input("Informe o percentual mínimo de concordância ( threshold ) ( ex . 0.9) : "))
    
    graph_path = "datasets/graph" + year + ".txt"
    politicians_path = "datasets/politicians" + year + ".txt"
    
    read_file(Graph, graph_path, read_file_by_political_party(politicians_path, p_party))
    print(Graph)
    normalize_graph(Graph, read_votes_data(politicians_path, p_party))
    threshold(Graph, threshold_idx)
    
    create_graph(Graph, year, p_party)
    
    inversion_of_weights(Graph)
    
    create_betwenness(Graph, year, p_party)
    create_heatmap(Graph, year, p_party)
