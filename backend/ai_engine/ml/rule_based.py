def decide_next_step(evaluation_result, error_analysis):
    """
    Rule-based adaptive learning decision
    """

    if not evaluation_result.get("valid", True):
        return {
            "next_action": "retry",
            "message": "Input jawaban tidak valid"
        }

    if evaluation_result.get("benar"):
        return {
            "next_action": "increase_difficulty",
            "message": "Naik ke soal SPLTV tingkat lanjut"
        }

    if error_analysis["error_type"] == "conceptual":
        return {
            "next_action": "review_material",
            "message": "Disarankan mengulang materi SPLTV dasar"
        }

    return {
        "next_action": "practice_more",
        "message": "Latihan SPLTV tambahan disarankan"
    }