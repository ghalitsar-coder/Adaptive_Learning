
import sys
import os

# Add the current directory to sys.path to allow imports
sys.path.append(os.getcwd())

from backend.services.transform_service import evaluate_soal_service

def test_evaluate():
    soal_text = "2x+3y+z=19, x+2y+3z=14, 3x+y+2z=20"
    konteks = "umum"
    
    # Test Case 1: Wrong Answer (Result should be False, but user says it is True)
    student_answer_wrong = {"x": 2, "y": 2, "z": 2} # 2(2)+3(2)+2 = 12 != 19
    
    print(f"Testing with soal: {soal_text}")
    print(f"Student Answer (Wrong): {student_answer_wrong}")
    
    result = evaluate_soal_service(soal_text, konteks, student_answer_wrong)
    
    print("Result:", result)
    
    if result['evaluation']['benar'] == True:
        print("BUG CONFIRMED: System says wrong answer is correct.")
    else:
        print("System correctly identified wrong answer.")

    # Test Case 2: Another answer
    student_answer_2 = {"x": 4.94, "y": 2.61, "z": 1.28}
    print(f"\nStudent Answer 2: {student_answer_2}")
    result_2 = evaluate_soal_service(soal_text, konteks, student_answer_2)
    print("Result 2:", result_2)

if __name__ == "__main__":
    test_evaluate()
