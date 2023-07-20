import os
import re
import networkx as nx
import matplotlib.pyplot as plt

class DependencyGraph:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, source, dependency):
        if source in self.dependencies:
            self.dependencies[source].append(dependency)
        else:
            self.dependencies[source] = [dependency]

    def get_dependencies(self, source):
        if source in self.dependencies:
            return self.dependencies[source]
        else:
            return []

def create_dependency_graph(root_dir):
    graph = DependencyGraph()
    file_regex = re.compile(r'\.py$')

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if file_regex.search(filename):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path, graph)
                
    return graph

def process_file(file_path, graph):
    with open(file_path, 'r') as file:
        content = file.read()
        dependencies = find_imports(content)

        for dependency in dependencies:
            graph.add_dependency(file_path, dependency)

def find_imports(content):
    import_regex = re.compile(r'from\s+(\S+)\s+import|\nimport\s+(\S+)')
    imports = []

    matches = import_regex.findall(content)
    for match in matches:
        for imp in match:
            if imp:
                imports.append(imp)

    return imports

def visualize_dependency_graph(graph):
    G = nx.DiGraph()

    for source, dependencies in graph.dependencies.items():
        G.add_node(source)
        for dependency in dependencies:
            G.add_edge(source, dependency)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=800, edge_color='gray', arrows=True)
    plt.title("Dependency Graph")
    plt.show()

# Usage example
root_directory = 'src'
dependency_graph = create_dependency_graph(root_directory)

visualize_dependency_graph(dependency_graph)
