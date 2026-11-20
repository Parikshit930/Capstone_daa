"""
models.py
Data structures and models for the Mini-Courier Planner Capstone Project.
Course: Design & Analysis of Algorithms (ETCCDA302)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
import json


@dataclass
class Parcel:
    """Represents a parcel to be delivered."""
    id: str
    customer_name: str
    destination: str
    weight: int           # integer weight (in kg) for Knapsack DP
    priority: int         # priority / value score (higher means more critical)
    deadline_hours: float # delivery deadline in hours from dispatch (lower means more urgent)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "destination": self.destination,
            "weight": self.weight,
            "priority": self.priority,
            "deadline_hours": self.deadline_hours,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Parcel":
        return cls(
            id=str(data["id"]),
            customer_name=str(data["customer_name"]),
            destination=str(data["destination"]),
            weight=int(data["weight"]),
            priority=int(data["priority"]),
            deadline_hours=float(data["deadline_hours"]),
        )

    def __repr__(self) -> str:
        return (f"Parcel({self.id}, to={self.destination}, wt={self.weight}kg, "
                f"pri={self.priority}, ddl={self.deadline_hours}h)")


class DeliveryGraph:
    """
    Weighted road network graph representation using an Adjacency List.
    Nodes represent the Depot and Delivery Locations (Customers/Hubs).
    Edges represent road connections with distance (in km).
    """

    def __init__(self, is_directed: bool = False):
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}
        self.is_directed: bool = is_directed
        self.node_metadata: Dict[str, Dict[str, Any]] = {}

    def add_node(self, node: str, label: str = "") -> None:
        if node not in self.adj_list:
            self.adj_list[node] = []
            self.node_metadata[node] = {"label": label or node}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        if weight < 0:
            raise ValueError(f"Edge weight cannot be negative for Dijkstra: {weight}")
        self.add_node(u)
        self.add_node(v)
        self.adj_list[u].append((v, weight))
        if not self.is_directed:
            self.adj_list[v].append((u, weight))

    def get_neighbors(self, node: str) -> List[Tuple[str, float]]:
        return self.adj_list.get(node, [])

    def get_nodes(self) -> List[str]:
        return list(self.adj_list.keys())

    def to_dict(self) -> Dict[str, Any]:
        edges = []
        seen = set()
        for u in self.adj_list:
            for v, w in self.adj_list[u]:
                edge_id = (u, v) if self.is_directed else tuple(sorted([u, v]))
                if edge_id not in seen:
                    seen.add(edge_id)
                    edges.append({"from": u, "to": v, "weight": w})
        return {
            "is_directed": self.is_directed,
            "nodes": [{"id": k, "label": v["label"]} for k, v in self.node_metadata.items()],
            "edges": edges,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeliveryGraph":
        graph = cls(is_directed=data.get("is_directed", False))
        for n in data.get("nodes", []):
            graph.add_node(n["id"], n.get("label", n["id"]))
        for e in data.get("edges", []):
            graph.add_edge(e["from"], e["to"], float(e["weight"]))
        return graph
