import re
import numpy as np

def is_spltv_question(text: str) -> bool:
    """
    Validasi apakah teks mengandung soal SPLTV
    """

    if not text or not text.strip():
        return False

    # Normalisasi teks: lower case dan ganti koma dengan newline
    text = text.lower().replace(',', '\n')

    # 1. Cari semua persamaan (mengandung '=')
    # Gunakan splitlines untuk keamanan lebih baik daripada regex kompleks
    equations = [line for line in text.split('\n') if '=' in line]
    
    if len(equations) < 3:
        return False

    # 2. Deteksi variabel x, y, z
    variables = set(re.findall(r'\b[x y z]\b', text.replace('+', ' ').replace('-', ' ')))
    if len(variables) < 3:
        return False

    # 3. Tolak non-linear (x^2, xy, dll)
    non_linear_patterns = [
        r'x\s*\^',
        r'y\s*\^',
        r'z\s*\^',
        r'xy',
        r'xz',
        r'yz'
    ]

    for pattern in non_linear_patterns:
        if re.search(pattern, text):
            return False

    return True

def extract_spltv_coefficients(text: str):
    """
    Ekstraksi koefisien x, y, z dan konstanta dari SPLTV
    Return: list of dict
    """
    
    # Normalisasi: ganti koma dengan newline agar regex bekerja per baris
    text = text.replace(',', '\n')

    equations = re.findall(r'([^\n=]+)=([^\n]+)', text)

    results = []

    for left, right in equations:
        eq_data = {
            "x": 0,
            "y": 0,
            "z": 0,
            "const": 0
        }

        # Ambil konstanta (kanan)
        try:
            # Cari angka di ruas kanan
            const_match = re.search(r'-?\d+', right)
            if not const_match:
                 continue # Skip jika tidak ada konstanta
            eq_data["const"] = int(const_match.group(0))
        except:
            continue

        # Normalisasi sisi kiri
        left = left.replace('-', '+-')

        # Cari koefisien tiap variabel
        for var in ["x", "y", "z"]:
            pattern = rf'([+-]?\d*){var}'
            match = re.search(pattern, left)

            if match:
                coef = match.group(1)

                if coef in ["", "+"]:
                    eq_data[var] = 1
                elif coef == "-":
                    eq_data[var] = -1
                else:
                    try:
                        eq_data[var] = int(coef)
                    except ValueError:
                         eq_data[var] = 1 # Fallback mechanism

        results.append(eq_data)

    return results if len(results) >= 3 else None

def evaluate_spltv_answer(coefficients, student_answer):
    """
    Evaluasi jawaban siswa terhadap SPLTV

    coefficients: list of dict [{x,y,z,const}, ...]
    student_answer: dict {"x": int, "y": int, "z": int}
    """

    try:
        x = int(student_answer.get("x"))
        y = int(student_answer.get("y"))
        z = int(student_answer.get("z"))
    except:
        return {
            "valid": False,
            "message": "Jawaban siswa tidak valid"
        }

    results = []

    for idx, eq in enumerate(coefficients):
        left_value = (
            eq["x"] * x +
            eq["y"] * y +
            eq["z"] * z
        )

        is_correct = left_value == eq["const"]

        results.append({
            "persamaan_ke": idx + 1,
            "hasil": is_correct,
            "nilai_dihitung": left_value,
            "nilai_seharusnya": eq["const"]
        })

    final_result = all(item["hasil"] for item in results)

    return {
        "valid": True,
        "benar": final_result,
        "detail": results
    }

def solve_spltv_numpy(coefficients):
    """
    Menyelesaikan SPLTV menggunakan NumPy
    """

    if not coefficients or len(coefficients) != 3:
        return None

    try:
        A = []
        B = []

        for eq in coefficients:
            A.append([eq["x"], eq["y"], eq["z"]])
            B.append(eq["const"])

        A = np.array(A, dtype=float)
        B = np.array(B, dtype=float)

        solution = np.linalg.solve(A, B)

        return {
            "x": round(solution[0], 3),
            "y": round(solution[1], 3),
            "z": round(solution[2], 3)
        }

    except Exception as e:
        return None