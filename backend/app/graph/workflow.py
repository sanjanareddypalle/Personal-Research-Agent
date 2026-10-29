import logging
from typing import Literal
from langgraph.graph import StateGraph, END

from app.graph.state import ResearchState
from app.graph.nodes import (
    goal_understanding_node,
    research_planning_node,
    source_collection_node,
    information_extraction_node,
    evidence_comparison_node,
    source_verification_node,
    knowledge_synthesis_node,
    roadmap_generation_node,
    report_generation_node
)

logger = logging.getLogger(__name__)

def check_sources_condition(state: ResearchState) -> Literal["information_extraction", "retry_sources", "report_generation"]:
    """Conditional routing verifying that sufficient sources were obtained."""
    sources = state.get("sources", [])
    retry_count = state.get("retry_count", 0)
    
    if len(sources) >= 1:
        return "information_extraction"
    
    if retry_count < 2:
        logger.warning(f"Insufficient sources ({len(sources)}). Retrying source collection (Attempt {retry_count + 1}/2)...")
        state["retry_count"] = retry_count + 1
        return "retry_sources"
        
    logger.error("Source collection exhausted retries without minimum results.")
    return "information_extraction"

def build_research_graph():
    """Builds and compiles the 9-stage LangGraph execution pipeline."""
    builder = StateGraph(ResearchState)

    # 1. Register Nodes
    builder.add_node("goal_understanding", goal_understanding_node)
    builder.add_node("research_planning", research_planning_node)
    builder.add_node("source_collection", source_collection_node)
    builder.add_node("information_extraction", information_extraction_node)
    builder.add_node("evidence_comparison", evidence_comparison_node)
    builder.add_node("source_verification", source_verification_node)
    builder.add_node("knowledge_synthesis", knowledge_synthesis_node)
    builder.add_node("roadmap_generation", roadmap_generation_node)
    builder.add_node("report_generation", report_generation_node)

    # 2. Sequential & Conditional Edges
    builder.set_entry_point("goal_understanding")
    builder.add_edge("goal_understanding", "research_planning")
    builder.add_edge("research_planning", "source_collection")
    
    # Conditional edge after source collection
    builder.add_conditional_edges(
        "source_collection",
        check_sources_condition,
        {
            "information_extraction": "information_extraction",
            "retry_sources": "source_collection",
            "report_generation": "report_generation"
        }
    )

    builder.add_edge("information_extraction", "evidence_comparison")
    builder.add_edge("evidence_comparison", "source_verification")
    builder.add_edge("source_verification", "knowledge_synthesis")
    builder.add_edge("knowledge_synthesis", "roadmap_generation")
    builder.add_edge("roadmap_generation", "report_generation")
    builder.add_edge("report_generation", END)

    return builder.compile()

research_graph = build_research_graph()
