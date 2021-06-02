from typing import List, Set
from dataclasses import dataclass

from GraphRanking.graph import Graph, Vertex

        
class GraphRanker:
    damping_factor: float = 0.85
        
    # TODO: garbage collecting by reference count
    
    @staticmethod
    def compute_iterates(iteration: int, graph: Graph) -> Graph:
        graph_ret = list()
        for it in iteration:
            next_graph: Graph = GraphRanker._update_graph(graph)
            graph_ret.add(iter_graph)
        return graph_ret

    @staticmethod
    def _update_graph(graph: Graph) -> Graph:
        ret = {}
        for idx, vertex in graph.vertexes.items():
            updated_vertex = GraphRanker._calc_vertex_score(vertex, graph)
            ret[idx] = deepcopy(updated_vertex)

        netx_graph: Graph = Graph(ret)
        return next_graph

    @staticmethod
    def _calc_vertex_score(vertex, graph) -> Vertex:
        # 1. predecessors는 vertex가 아닌 그래프 내의 엣지리스트에서 가져와야한다.
        # 그런 의미에서 predecessors는 vertex의 클래스변수가 아닌 별도의 extractor 클래스가 구현되어야 한다.
        term_one: float = 1 - GraphRanker.damping_factor
        term_two: float = GraphRanker._calc_integrate_weight(vertex.predecessors, graph)

        vertex_score = term_one + term_two
        vertex.update_score(vertex_score)
        return vertex

    @staticmethod
    def _calc_integrate_weight(predecessors: set, graph: Graph) -> float:
        # 2. score를 계산할때, 가장 밑부분까지 graph obj가 같이 내려가서 필요한 정보를 제공해줄 수 있어야한다.
        # 그러므로 `_calc_partial_score` 를 계산할 때도, graph 객체가 같이 내려가야 할 것이다.
        score_set = []
        for predecessor in predecessors:
            vertex_j = graph[predecessor]
            partial_score = GraphRanker._calc_partial_score(vertex_j)
            score_set.append(partial_score)

        score = sum(score_set)
        weight = GraphRanker.damping_factor * score
        return weight

    @staticmethod
    def _calc_partial_score(vertex_j: Vertex) -> float:
        # 3. 위에서 서술한 마찬가지의 이유로 `vertex.successors` 의 계산 역시 별도의 extractor 객체에서 제공하는 메서드를 이용해야한다.
        # 이러한 그래프에서 필요한 정보를 뽑아내는 객체를 `graph_feature_extractor` 라고 명명하고 해당 객체의 도움을 받을 필요가 있다.
        score_vertex_j = vertex_j.score
        num_successors = int(vertex_j.successors)
        return score_vertex_j / num_successors