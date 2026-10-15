
import os
import matplotlib.pyplot as plt

# Save graphs inside the graphs folder
base = os.path.dirname(os.path.abspath(__file__))
graph_folder = os.path.join(base, "graphs")
os.makedirs(graph_folder, exist_ok=True)

# Six dataset sizes
sizes = [1000, 5000, 10000, 50000, 100000, 500000]
positions = [1, 2, 3, 4, 5, 6]

# Example values only — replace with actual measured timings
dictionary_time = [0.001, 0.004, 0.008, 0.035, 0.070, 0.350]
bst_time = [0.002, 0.010, 0.025, 0.150, 0.350, 2.000]
trie_time = [0.003, 0.012, 0.020, 0.100, 0.200, 1.000]


def make_graph(name, times, filename):
    plt.figure(figsize=(10, 5))

    # Plot all six values with equal spacing
    plt.plot(positions, times, marker="o")

    # Display all six dataset sizes
    plt.xticks(
        positions,
        ["1,000", "5,000", "10,000",
         "50,000", "100,000", "500,000"]
    )

    plt.xlabel("Dataset Size (Words)")
    plt.ylabel("Execution Time (Seconds)")
    plt.title(name + " Performance")

    plt.grid(True)
    plt.tight_layout()

    # Save the graph in the graphs folder
    path = os.path.join(graph_folder, filename)
    plt.savefig(path, dpi=150)
    plt.close()

    print("Saved:", path)


# Create three separate graphs
make_graph(
    "Dictionary",
    dictionary_time,
    "dictionary_graph.png"
)

make_graph(
    "BST",
    bst_time,
    "bst_graph.png"
)

make_graph(
    "Trie",
    trie_time,
    "trie_graph.png"
)

print("\nAll 3 graphs created successfully!")
print("Check the graphs folder inside DSA_Project.")
