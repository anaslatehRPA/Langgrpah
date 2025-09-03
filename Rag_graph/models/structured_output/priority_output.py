"""Structured output for project priority responses."""

from typing import List
from typing_extensions import TypedDict, Annotated, NotRequired


class ProjectPriorityItem(TypedDict):
    project: Annotated[str, "project folder/name"]
    priority_score: Annotated[float, "computed priority score (higher => do first)"]
    progress_percent: Annotated[int, "estimated percent complete (0-100)"]
    urgency_count: Annotated[int, "count of deadline/urgency keywords found"]
    risk_count: Annotated[int, "count of risk/issue keywords found"]
    reason: Annotated[str, "short human-readable reason / recommendation"]


class PriorityOutput(TypedDict):
    items: List[ProjectPriorityItem]
    generated_at: Annotated[str, "ISO timestamp"]
    summary: Annotated[str, "short textual summary"]
    notes: NotRequired[List[str]]


__all__ = ["ProjectPriorityItem", "PriorityOutput"]
