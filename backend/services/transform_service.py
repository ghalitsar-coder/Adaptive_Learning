from backend.ai_engine.ml.model_loader import load_adaptive_model
from backend.ai_engine.text_transformer import transform_spltv_text
from backend.services.analysis_service import evaluate_spltv_answer
from backend.services.analysis_service import solve_spltv_numpy

def solve_spltv_service(soal_text: str, konteks: str):
    """
    Service untuk menyelesaikan SPLTV
    """

    transform_result = transform_spltv_text(soal_text, konteks)

    if not transform_result.get("success"):
        return transform_result

    coefficients = transform_result.get("coefficients")

    solution = solve_spltv_numpy(coefficients)

    if not solution:
        return {
            "success": False,
            "message": "SPLTV tidak dapat diselesaikan"
        }

    return {
        "success": True,
        "materi": "SPLTV",
        "solution": solution
    }

def transform_soal_service(soal_text: str, konteks: str):
    """
    Service layer untuk transformasi soal SPLTV
    Menghubungkan route dengan AI engine
    """
    return transform_spltv_text(
        soal_text=soal_text,
        konteks=konteks
    )

def evaluate_soal_service(soal_text, konteks, student_answer):
    """
    Service evaluasi jawaban SPLTV
    """

    transform_result = transform_spltv_text(soal_text, konteks)

    if not transform_result.get("success"):
        return transform_result

    coefficients = transform_result.get("coefficients")

    correct_solution = solve_spltv_numpy(coefficients)

    if not correct_solution:
        return {
            "success": False,
            "message": "Gagal menyelesaikan SPLTV untuk evaluasi"
        }

    evaluation = evaluate_spltv_answer(coefficients, student_answer)

    return {
        "success": True,
        "materi": "SPLTV",
        "evaluation": evaluation
    }

# def adaptive_learning_service(evaluation_result):
#     error_analysis = analyze_spltv_error(evaluation_result["detail"])
#     adaptive_model = load_adaptive_model()

#     decision = adaptive_model(
#         evaluation_result=evaluation_result,
#         error_analysis=error_analysis
#     )

#     return {
#         "evaluation": evaluation_result,
#         "error_analysis": error_analysis,
#         "adaptive_decision": decision
#     }