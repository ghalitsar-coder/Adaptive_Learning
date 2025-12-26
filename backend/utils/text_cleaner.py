import re


def clean_text(text: str) -> str:
    """
    Membersihkan teks soal matematika
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()
