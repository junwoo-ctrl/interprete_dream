from typing import Dict, List
from dataclasses import dataclass
from collections import Counter


class Sentence:
    def __init__(self, index: int, text: str, bow: Counter) -> None:
        self.index: int = index
        self.text: str = text
        self.bow: Counter = bow

    def __str__(self) -> str:
        return self.text

    def __hash__(self) -> int:
        return self.index


@dataclass
class Vertex:
    score: float
    # predecessors: set  # 밖에서 이 노드로 오는
    # successors: set  # 이 노드에서 밖으로 가는
    data: Sentence  # 노드에 해당하는 문장 혹은 keyword
    index: int

    def update_score(self, updated_score: float):
        self.score = updated_score
        
    def get_score(self) -> float:
        return self.score


@dataclass
class Edge:
    start_node: int
    end_node: int
    weight: float = 0.0


@dataclass
class Graph:
    vertexes: List[Vertex]
    edges: List[Edge]