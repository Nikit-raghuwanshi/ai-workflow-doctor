"""A small data model for one workflow execution trace step."""

from dataclasses import dataclass


@dataclass
class TraceStep:
    """Describe one operation performed during a workflow execution."""

    node_name: str
    target_system: str
    operation: str
    status: str
