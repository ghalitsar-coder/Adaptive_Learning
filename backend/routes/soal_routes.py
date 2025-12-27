from flask import Blueprint, request, jsonify
from backend.services.transform_service import evaluate_soal_service, solve_spltv_service, transform_soal_service

soal_bp = Blueprint("soal", __name__)


@soal_bp.route("/transform", methods=["POST"])
def transform_soal():
    data = request.get_json()

    soal_text = data.get("soal_text", "")
    konteks = data.get("konteks", "umum")

    result = transform_soal_service(soal_text, konteks)

    return jsonify(result)

@soal_bp.route("/spltv/evaluate", methods=["POST"])
def evaluate_spltv():
    data = request.get_json()

    soal_text = data.get("soal")
    konteks = data.get("konteks", "umum")
    student_answer = data.get("jawaban")

    return jsonify(
        evaluate_soal_service(soal_text, konteks, student_answer)
    )

@soal_bp.route("/spltv/solve", methods=["POST"])
def solve_spltv():
    data = request.get_json()

    soal_text = data.get("soal")
    konteks = data.get("konteks", "umum")

    return jsonify(
        solve_spltv_service(soal_text, konteks)
    )

@soal_bp.route("/ping", methods=["GET"])
def ping():
    return {"status": "ok"}