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