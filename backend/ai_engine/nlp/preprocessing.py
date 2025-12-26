import nltk
from nltk.tokenize import word_tokenize


def tokenize_text(text: str):
    import nltk
    nltk.download('punkt', quiet=True)
    from nltk.tokenize import word_tokenize

    return word_tokenize(text.lower())

