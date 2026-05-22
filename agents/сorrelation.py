from graph.agent_state import AgentState
from settings import Settings
from tools.profiler import get_leakage_candidates

settings = Settings()

def correlation_node(state: AgentState) -> dict:
    target_column = state["confirmed_target"]
    corr_matrix = state["correlation_matrix"]
    id_columns = state["confirmed_id_columns"] or []
    leakage_candidates = get_leakage_candidates(target_column,
                                                corr_matrix,
                                                id_columns,
                                                settings.correlation_leak_threshold)
    leakage_candidates = [col for col in leakage_candidates if col not in state["confirmed_id_columns"]]
    return {
        "leakage_candidates": leakage_candidates
    }