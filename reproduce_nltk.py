
from backend.ai_engine.nlp.preprocessing import tokenize_text

try:
    print("Testing tokenization...")
    tokens = tokenize_text("Hello world")
    print(f"Tokens: {tokens}")
    print("SUCCESS: Tokenization works")
except LookupError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"ERROR: {e}")
