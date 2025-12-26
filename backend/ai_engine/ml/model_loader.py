from backend.ai_engine.ml.rule_based import decide_next_step


def load_adaptive_model():
    """
    Loader model adaptif
    Saat ini menggunakan rule-based
    """

    return decide_next_step
