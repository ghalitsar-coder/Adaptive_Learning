
import re
import math

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
        # Change: parse as float to support decimal answers
        x = float(student_answer.get("x"))
        y = float(student_answer.get("y"))
        z = float(student_answer.get("z"))
    except:
        return {
            "valid": False,
            "message": "Jawaban siswa tidak valid"
        }

    results = []
    
    # Tolerance for float comparison
    epsilon = 0.5 

    for idx, eq in enumerate(coefficients):
        left_value = (
            eq["x"] * x +
            eq["y"] * y +
            eq["z"] * z
        )

        # Change: Use tolerance for comparison
        is_correct = abs(left_value - eq["const"]) < epsilon
        
        # Debug print
        print(f"Eq {idx+1}: {eq['x']}*{x} + {eq['y']}*{y} + {eq['z']}*{z} = {left_value}. Target: {eq['const']}. Correct? {is_correct}")

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

def main():
    soal_text = "2x+3y+z=19, x+2y+3z=14, 3x+y+2z=20"
    print(f"Soal: {soal_text}")
    
    coefs = extract_spltv_coefficients(soal_text)
    print(f"Coefficients: {coefs}")
    
    if not coefs:
        print("Failed to extract coefficients")
        return

    # Test Case 1: Wrong Answer
    wrong_answer = {"x": 2, "y": 2, "z": 2} # From user prompt (first one)
    print(f"\nEvaluating Wrong Answer: {wrong_answer}")
    res1 = evaluate_spltv_answer(coefs, wrong_answer)
    print(f"Result: {res1['benar']}")
    
    # Test Case 2: Another answer
    answer2 = {"x": 4.94, "y": 2.61, "z": 1.28}
    print(f"\nEvaluating Answer 2: {answer2}")
    res2 = evaluate_spltv_answer(coefs, answer2)
    print(f"Result: {res2['benar']}")

if __name__ == "__main__":
    main()
