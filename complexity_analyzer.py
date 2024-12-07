class ComplexityAnalyzer:
    def __init__(self):
        self.complexity_map = {
            'BFS': {
                'time': 'O(b^d)',  # b: branching factor, d: depth
                'space': 'O(b^d)'
            },
            'DFS': {
                'time': 'O(b^m)',  # b: branching factor, m: maximum depth
                'space': 'O(bm)'
            },
            'UCS': {
                'time': 'O(b^(1 + C/ε))',  # C: cost of optimal solution, ε: minimum cost increment
                'space': 'O(b^(1 + C/ε))'
            }
        }

    def analyze(self, algorithm: str, nodes_explored: int, path_length: int) -> dict:
        base_complexity = self.complexity_map.get(algorithm, {
            'time': 'Unknown',
            'space': 'Unknown'
        })
        
        complexity = {
            'time': f"{base_complexity['time']} (Visited {nodes_explored} nodes)",
            'space': f"{base_complexity['space']} (Path length: {path_length})"
        }
        
        return complexity
