from collections import deque
from typing import List, Tuple, Optional
import heapq
import random
import time


class PuzzleNode:
    def __init__(self, state: List[int], parent: Optional['PuzzleNode'] = None, 
                 action: str = "", cost: int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
    
    def __lt__(self, other):
        return self.cost < other.cost


class PuzzleSolver:
    GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    MOVES = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}

    @staticmethod
    def get_blank_position(state: List[int]) -> int:
        return state.index(0)

    @staticmethod
    def get_possible_moves(blank_pos: int) -> List[Tuple[str, int]]:
        moves = []
        row, col = divmod(blank_pos, 3)
        
        if row > 0: moves.append(('UP', blank_pos - 3))
        if row < 2: moves.append(('DOWN', blank_pos + 3))
        if col > 0: moves.append(('LEFT', blank_pos - 1))
        if col < 2: moves.append(('RIGHT', blank_pos + 1))
        
        return moves

    @staticmethod
    def get_next_state(state: List[int], blank_pos: int, new_pos: int) -> List[int]:
        new_state = state.copy()
        new_state[blank_pos], new_state[new_pos] = new_state[new_pos], new_state[blank_pos]
        return new_state

    @staticmethod
    def is_goal_state(state: List[int]) -> bool:
        return state == PuzzleSolver.GOAL_STATE

    @staticmethod
    def reconstruct_path(node: PuzzleNode) -> Tuple[List[str], List[List[int]]]:
        path = []
        states = []
        current = node
        
        while current:
            if current.action:
                path.insert(0, current.action)
            states.insert(0, current.state)
            current = current.parent
            
        return path, states

    @staticmethod
    def generate_solvable_state() -> List[int]:
        state = PuzzleSolver.GOAL_STATE[:]
        while True:
            random.shuffle(state)
            if PuzzleSolver.is_solvable(state):
                return state

    @staticmethod
    def is_solvable(state: List[int]) -> bool:
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] > state[j] and state[i] != 0 and state[j] != 0:
                    inversions += 1
        return inversions % 2 == 0

    @staticmethod
    def bfs(initial_state: List[int]) -> Optional[Tuple[List[str], List[List[int]], int]]:
        queue = deque([PuzzleNode(initial_state)])
        visited = {str(initial_state)}
        nodes_explored = 0

        while queue:
            node = queue.popleft()
            nodes_explored += 1
            
            if PuzzleSolver.is_goal_state(node.state):
                return PuzzleSolver.reconstruct_path(node) + (nodes_explored,)

            blank_pos = PuzzleSolver.get_blank_position(node.state)
            for move, new_pos in PuzzleSolver.get_possible_moves(blank_pos):
                new_state = PuzzleSolver.get_next_state(node.state, blank_pos, new_pos)
                state_str = str(new_state)
                if state_str not in visited:
                    visited.add(state_str)
                    queue.append(PuzzleNode(new_state, node, move, node.cost + 1))

        return None

    @staticmethod
    def dfs(initial_state: List[int]) -> Optional[Tuple[List[str], List[List[int]], int]]:
        stack = [PuzzleNode(initial_state)]
        visited = {str(initial_state)}
        nodes_explored = 0

        while stack:
            node = stack.pop()
            nodes_explored += 1
            
            if PuzzleSolver.is_goal_state(node.state):
                return PuzzleSolver.reconstruct_path(node) + (nodes_explored,)

            blank_pos = PuzzleSolver.get_blank_position(node.state)
            for move, new_pos in reversed(PuzzleSolver.get_possible_moves(blank_pos)):
                new_state = PuzzleSolver.get_next_state(node.state, blank_pos, new_pos)
                state_str = str(new_state)
                if state_str not in visited:
                    visited.add(state_str)
                    stack.append(PuzzleNode(new_state, node, move, node.cost + 1))

        return None

    @staticmethod
    def ucs(initial_state: List[int]) -> Optional[Tuple[List[str], List[List[int]], int]]:
        pq = [(0, PuzzleNode(initial_state))]
        visited = {str(initial_state)}
        nodes_explored = 0

        while pq:
            _, node = heapq.heappop(pq)
            nodes_explored += 1
            
            if PuzzleSolver.is_goal_state(node.state):
                return PuzzleSolver.reconstruct_path(node) + (nodes_explored,)

            blank_pos = PuzzleSolver.get_blank_position(node.state)
            for move, new_pos in PuzzleSolver.get_possible_moves(blank_pos):
                new_state = PuzzleSolver.get_next_state(node.state, blank_pos, new_pos)
                state_str = str(new_state)
                if state_str not in visited:
                    visited.add(state_str)
                    new_node = PuzzleNode(new_state, node, move, node.cost + 1)
                    heapq.heappush(pq, (new_node.cost, new_node))

        return None
