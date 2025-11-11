import networkx as nx
import matplotlib.pyplot as plt

def draw_candidates_graph(candidates,context,number_of_suggestions):
    if  context:
        G = nx.DiGraph()
        context_str = "".join(context).lower()
        G.add_node(context_str, color="orange")

        first = True
        count = 0
        for word, weight in candidates:
            count += 1
            if count < number_of_suggestions+1:
                if first:
                    G.add_node(f"{word}({weight})", color="red")
                    first = False
                else:
                    G.add_node(f"{word}({weight})", color="skyblue")
                G.add_edge(context_str, f"{word}({weight})", weight=1)
            else:
                break

        pos = nx.spring_layout(G, seed=42)

        colors = [data["color"] for _, data in G.nodes(data=True)]
        nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2000, alpha=0.9)
        nx.draw_networkx_labels(G,pos,font_size=10,font_weight="bold")
        weights = [G[u][v]["weight"] for u, v in G.edges()]
        nx.draw_networkx_edges(
            G,
            pos,
            edge_color="gray",
            arrows=True,
            arrowsize=20,
            width=[w * 1.5 for w in weights],
            connectionstyle="arc3,rad=0.1"
        )

        plt.title(f"Candidatos para: '{context_str}'")
        plt.axis("off")
        plt.savefig("static/images/candidates_graph.png", transparent=True)
        plt.close()

import networkx as nx
import matplotlib.pyplot as plt
import math

def draw_pdf(wg, context, number_of_suggestions):
    if not context:
        return

    # 🔹 Limpiar el contexto
    words = [w.strip().lower() for w in context.split(" ") if w.strip()]
    if not words:
        return

    G = nx.DiGraph()
    for i, word in enumerate(words):
        G.add_node(word, color="orange",)
        if i > 0:
            G.add_edge(words[i - 1], word, weight=1)
    for word in words:
        try:
            predictions = wg.predict_next(word)
        except Exception as e:
            print(f"Error al predecir '{word}': {e}")
            continue

        first = True
        for count, (pred, weight) in enumerate(predictions, start=1):
            if count > number_of_suggestions:
                break
            pred = str(pred).strip()
            if not pred:
                continue
            node_label = f"{pred}({weight})"
            G.add_node(node_label, color="red" if first else "skyblue")
            G.add_edge(word, node_label, weight=1)
            first = False
    pos = {}
    base_x = 0
    x_spacing = 10
    radius = 3

    for i, word in enumerate(words):
        center_x = i * x_spacing
        center_y = 0
        pos[word] = (center_x, center_y)
        preds = [n for n in G.successors(word) if "(" in n]
        n_preds = len(preds)
        if n_preds == 0:
            continue
        for j, pred in enumerate(preds):
            angle = 2 * math.pi * j / n_preds
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            pos[pred] = (x, y)
    plt.figure(figsize=(max(15, len(words) * 6), 12))

    colors = [data["color"] for _, data in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=2200, alpha=0.95,linewidths=2, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    weights = [G[u][v]["weight"] for u, v in G.edges()]
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="gray",
        arrows=True,
        arrowsize=20,
        width=[w * 1.3 for w in weights],
        connectionstyle="arc3,rad=0.2"
    )

    plt.title("Grafo completo de predicciones", fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("static/images/candidates_graph_pdf.png", transparent=True, dpi=500)
    plt.close()
