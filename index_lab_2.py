
import os
import re
import time
import random


# DICTIONARY 

class DictionaryIndex:
    def __init__(self):
        self.index = {}

    def build(self, words_by_line):
        for line_no, words in enumerate(words_by_line, 1):
            for word in words:
                self.index.setdefault(word, []).append(line_no)

    def search(self, word):
        return self.index.get(word, [])

    def print_index(self):
        return [
            f"{word}: {self.index[word]}"
            for word in sorted(self.index)
        ]


# BST 

class BSTNode:
    def __init__(self, word, line_no):
        self.word = word
        self.lines = [line_no]
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, word, line_no):
        if self.root is None:
            self.root = BSTNode(word, line_no)
            return

        node = self.root

        while True:
            if word == node.word:
                node.lines.append(line_no)
                return
            elif word < node.word:
                if node.left is None:
                    node.left = BSTNode(word, line_no)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(word, line_no)
                    return
                node = node.right

    def build(self, words_by_line):
        for line_no, words in enumerate(words_by_line, 1):
            for word in words:
                self.insert(word, line_no)

    def search(self, word):
        node = self.root

        while node:
            if word == node.word:
                return node.lines
            elif word < node.word:
                node = node.left
            else:
                node = node.right

        return []

    def print_index(self):
        result = []
        stack = []
        node = self.root

        while stack or node:
            while node:
                stack.append(node)
                node = node.left

            node = stack.pop()
            result.append(f"{node.word}: {node.lines}")
            node = node.right

        return result


# TRIE 

class TrieNode:
    def __init__(self):
        self.children = {}
        self.lines = []


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, line_no):
        node = self.root

        for char in word:
            node = node.children.setdefault(char, TrieNode())

        node.lines.append(line_no)

    def build(self, words_by_line):
        for line_no, words in enumerate(words_by_line, 1):
            for word in words:
                self.insert(word, line_no)

    def search(self, word):
        node = self.root

        for char in word:
            node = node.children.get(char)
            if node is None:
                return []

        return node.lines

    def print_index(self):
        result = []
        stack = [(self.root, "")]

        while stack:
            node, prefix = stack.pop()

            if node.lines:
                result.append(f"{prefix}: {node.lines}")

            for char in sorted(node.children, reverse=True):
                stack.append(
                    (node.children[char], prefix + char)
                )

        return result


# PERFORMANCE TEST 

def main():
    sizes = {
        "1": 1000,
        "2": 5000,
        "3": 10000,
        "4": 50000,
        "5": 100000,
        "6": 500000
    }

    print("========== WORD INDEXING PERFORMANCE ==========")

    for key, size in sizes.items():
        print(f"{key}. {size} words")

    choice = input("\nChoose dataset (1-6): ").strip()

    if choice not in sizes:
        print("Invalid dataset choice!")
        return

    size = sizes[choice]

    base = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(
        base, "large_test_files", f"input_{size}.txt"
    )
    input_file = os.path.join(base, "input.txt")

    if not os.path.isfile(input_file):
        print("Input file not found:", input_file)
        return

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    words_by_line = [
        re.findall(r"\b\w+\b", line.lower())
        for line in lines
    ]

    all_words = [
        word for words in words_by_line for word in words
    ]

    if not all_words:
        print("Input file is empty!")
        return

    rng = random.Random(42)
    searches = [
        rng.choice(all_words)
        for _ in range(min(1000, len(all_words)))
    ]

    methods = [
        ("Dictionary", DictionaryIndex),
        ("BST", BST),
        ("Trie", Trie)
    ]

    print(f"\nDataset size: {size}")
    print(f"Words loaded: {len(all_words)}")

    # Save all three indexes in separate output files.
    for name, IndexClass in methods:
        print(f"\n========== {name} ==========")

        index = IndexClass()

        start = time.perf_counter()
        index.build(words_by_line)
        build_time = time.perf_counter() - start

        start = time.perf_counter()
        for word in searches:
            index.search(word)
        search_time = time.perf_counter() - start

        start = time.perf_counter()
        output = index.print_index()
        print_time = time.perf_counter() - start

        output_path = os.path.join(
            base, f"{name.lower()}_{size}_output.txt"
        )
        output_path = os.path.join(base, "output.txt")

        # Write the COMPLETE index to the output file.
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("\n".join(output))
            if output:
                file.write("\n")

        total_time = build_time + search_time + print_time

        # Show summary only in the terminal.
        print(f"Dataset size  : {size}")
        print(f"Unique words  : {len(output)}")
        print(f"Build time    : {build_time:.6f} seconds")
        print(f"Search time   : {search_time:.6f} seconds")
        print(f"Index time    : {print_time:.6f} seconds")
        print(f"Total time    : {total_time:.6f} seconds")
        print(f"Output file   : {output_path}")
        print("Status        : Full index saved successfully")

    print("\n========== COMPARISON COMPLETED ==========")
    print("Check the output .txt files in your project folder.")


if __name__ == "__main__":
    main()