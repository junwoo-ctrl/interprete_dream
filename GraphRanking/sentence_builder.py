from typing import List, Callable, Union, Tuple
from re import split
from collections import Counter
from itertools import combinations
import random

from GraphRanking.graph import Vertex, Graph, Edge, Sentence


class SentenceTokenizer:
    
    @staticmethod
    def preprocess_text(text: str, tokenizer: Callable) -> List[str]:
        candidates: List[str] = split(r'(?:(?<=[^0-9])\.|\n|!|\?)', text)
        index: int = 1
        duplication_checker: set = set()
        sentences: List[Sentence] = []
        
        # inspecting
        for candidate in candidates:
            stripped_candidate: str = SentenceTokenizer._validate_cleansing(candidate, duplication_checker)
            if stripped_candidate is None:
                continue
            
            tokens: List[str] = SentenceTokenizer._validate_tokenize(stripped_candidate, tokenizer, duplication_checker)
            if tokens is None:
                continue
                
            bow: Counter = Counter(tokens)
            
            sentence: Sentence =  Sentence(index, stripped_candidate, bow)
            sentences.append(sentence)
            index += 1
        return sentences
            
    @staticmethod
    def _validate_cleansing(candidate: str, duplication_checker: set) -> Union[str, None]:
        stripped_candidate = candidate.strip('. ')
        if not len(stripped_candidate):
            return None
        if stripped_candidate in duplication_checker:
            return None
        return stripped_candidate
    
    @staticmethod
    def _validate_tokenize(stripped_candidate: str, tokenizer: Callable, duplication_checker: set) -> List[str]:
        tokens: List[str] = tokenizer(stripped_candidate)
        if len(tokens) < 2:
            return None
        duplication_checker.add(stripped_candidate)
        return tokens
    
    
class SentenceGraphBuilder:
    
    @staticmethod
    def build(sentence_list: List[Sentence]) -> Graph:
        vertex_list: List[Vertex] = SentenceGraphBuilder._gen_vertex_list_from_sentences(sentence_list)
        edge_list: List[Edges] = SentenceGraphBuilder._gen_edge_list_from_vertex_list(vertex_list)
        graph = Graph(vertexes=vertex_list, edges=edge_list)
        return graph
        
    @staticmethod
    def _gen_edge_list_from_vertex_list(vertex_list: List[Vertex]) -> List[Edge]:
        edge_list: List[Edge] = list(map(SentenceGraphBuilder._get_edge, combinations(vertex_list, 2)))  # element is Tuple.
        return edge_list
    
    @staticmethod
    def _get_edge(vertex_tuple: Tuple[Vertex]) -> Edge:

        weight: float = SentenceGraphBuilder._calc_sentence_similarity(vertex_tuple[0].data.bow, vertex_tuple[1].data.bow)
        return Edge(start_node=vertex_tuple[0].index, end_node=vertex_tuple[1].index, weight=weight)
        
    @staticmethod
    def _calc_sentence_similarity(bow1: Counter, bow2: Counter) -> float:
        intersection_count: int = sum((bow1 & bow2).values())
        union_count: int = sum((bow1 | bow2).values())
        try:
            return intersection_count / union_count
        except ZeroDivisionError:
            return 0.0
    
    @staticmethod
    def _gen_vertex_list_from_sentences(sentence_list: List[Sentence]) -> List[Vertex]:
        return list(map(SentenceGraphBuilder._get_vertex, sentence_list))
            
    @staticmethod
    def _get_vertex(sentence: Sentence) -> Vertex:
        return Vertex(
            score=round(random.uniform(0, 1), 4),
            data=sentence,
            index=sentence.index
        )