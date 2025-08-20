from utils.pdf_reader import extract_text_from_pdf
import os
import argparse
from plagiarism import preprocess, tfidf, minhash_lsh, explain, report
from difflib import SequenceMatcher
from datetime import datetime


def load_input_text(file_path: str) -> str:
    """Loads text from a .txt or .pdf file."""
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        print(f"[INFO] Extracting text from PDF: {file_path}")
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".txt":
        print(f"[INFO] Reading text from TXT: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format. Use .txt or .pdf")


def detect_plagiarism(text, reference_documents, topk, min_score):
    norm_text = preprocess.normalize(text)
    norm_refs = [preprocess.normalize(r) for r in reference_documents]
    candidates = minhash_lsh.minhash_candidates(norm_text, norm_refs)
    scored = []
    sims = tfidf.tfidf_cosine(norm_text, [norm_refs[i] for i in candidates])
    for idx, score in zip(candidates, sims):
        if score >= min_score:
            highlighted, overlap = explain.highlight_overlap(
                preprocess.tokenize(norm_text),
                preprocess.tokenize(norm_refs[idx])
            )
            scored.append({
                "ref_index": idx,
                "score": score,
                "overlap": overlap,
                "highlighted": highlighted
            })
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:topk]


def similarity(a, b):
    """Compute similarity ratio between two texts."""
    return SequenceMatcher(None, a, b).ratio()


def detect_collisions(query_text, submissions_dir="submissions", threshold=0.7):
    """Compare new submission against past submissions for collision detection."""
    os.makedirs(submissions_dir, exist_ok=True)

    collisions = []
    for fname in os.listdir(submissions_dir):
        fpath = os.path.join(submissions_dir, fname)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            old_text = f.read()
        score = similarity(query_text, old_text)
        if score >= threshold:
            collisions.append({
                "file": fname,
                "score": score
            })
    return collisions


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True, help="Path to query file (.txt or .pdf)")
    ap.add_argument("--refs", nargs='+', required=True, help="List of reference files (.txt or .pdf)")
    ap.add_argument("--topk", type=int, default=3)
    ap.add_argument("--min_score", type=float, default=0.2)
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    text = load_input_text(args.query)
    refs = [load_input_text(r) for r in args.refs]

    results = detect_plagiarism(text, refs, args.topk, args.min_score)

    os.makedirs("submissions", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    sub_file = f"submissions/sub_{timestamp}.txt"
    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(text)

    collisions = detect_collisions(text, "submissions")

    if args.report:
        report.save_html_report(results, refs, args.report, collisions=collisions)
    else:
        print("Plagiarism Results:", results)
        print("Submission Collisions:", collisions)


