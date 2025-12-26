from backend.utils.text_cleaner import clean_text
from backend.ai_engine.nlp.preprocessing import tokenize_text
from backend.services.analysis_service import (
    is_spltv_question,
    extract_spltv_coefficients
)
from backend.utils.json_helper import build_response


def transform_spltv_text(soal_text: str, konteks: str = "umum"):
    """
    Transformasi teks soal SPLTV ke konteks tertentu (teks saja)
    Fokus: menjaga struktur matematis SPLTV
    """

    # 1. Validasi input kosong
    if not soal_text or not soal_text.strip():
        return build_response(
            success=False,
            message="Teks soal kosong"
        )

    # 2. Cleaning teks
    cleaned_text = clean_text(soal_text)

    # 3. Validasi SPLTV
    if not is_spltv_question(cleaned_text):
        return build_response(
            success=False,
            message="Soal bukan termasuk SPLTV"
        )

    # 4. Tokenisasi (disiapkan untuk AI adaptif)
    tokens = tokenize_text(cleaned_text)

    # 5. Ekstraksi koefisien & konstanta SPLTV
    coefficients = extract_spltv_coefficients(cleaned_text)
    if not coefficients:
        return build_response(
            success=False,
            message="Gagal mengekstraksi koefisien SPLTV"
        )

    # 6. Transformasi konteks (narasi saja)
    transformed_text = apply_context_transformation(cleaned_text, konteks)

    return build_response(
        success=True,
        materi="SPLTV",
        konteks=konteks,
        original_soal=soal_text,
        cleaned_soal=cleaned_text,
        transformed_soal=transformed_text,
        coefficients=coefficients
    )


def apply_context_transformation(text: str, konteks: str):
    """
    Aturan transformasi konteks teks SPLTV
    Hanya mengubah narasi, tidak menyentuh persamaan matematika
    """

    context_rules = {
        "game": {
            "pedagang": "pemain game",
            "harga": "poin",
            "uang": "poin",
            "membeli": "mengumpulkan",
            "barang": "item"
        },
        "olahraga": {
            "pedagang": "pelatih",
            "membeli": "mengatur",
            "barang": "latihan",
            "harga": "durasi",
            "uang": "waktu"
        }
    }

    rules = context_rules.get(konteks, {})

    for old_word, new_word in rules.items():
        text = text.replace(old_word, new_word)

    return text

def analyze_spltv_error(evaluation_detail):
    """
    Analisis kesalahan jawaban SPLTV siswa
    Berbasis rule sederhana (NLP simbolik)
    """

    incorrect = [d for d in evaluation_detail if not d["hasil"]]

    if not incorrect:
        return {
            "error_type": "none",
            "message": "Jawaban benar"
        }

    if len(incorrect) == len(evaluation_detail):
        return {
            "error_type": "conceptual",
            "message": "Kesalahan konsep SPLTV"
        }

    return {
        "error_type": "partial",
        "message": "Sebagian persamaan belum terpenuhi"
    }