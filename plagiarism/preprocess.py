import re
import string
from typing import List

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def tokenize(text: str) -> List[str]:
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

def split_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in text.split("\n") if p.strip()]
