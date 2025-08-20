import os
import html

def save_html_report(results, references, output_file):
    """
    Save plagiarism detection results into an HTML report.

    Args:
        results (dict): {
            "doc_scores": {doc_index: score, ...},
            "matches": [
                {
                    "doc": int,
                    "para": int or None,
                    "score": float,
                    "query_text": str,
                    "ref_text": str
                }
            ]
        }
        references (list of str): list of reference document texts
        output_file (str): path to save HTML file
    """

    html_content = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<title>Plagiarism Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 20px; background: #fafafa; }",
        "h1 { color: #333; }",
        "h2 { margin-top: 30px; }",
        "table { border-collapse: collapse; width: 100%; margin-top: 15px; }",
        "table, th, td { border: 1px solid #aaa; padding: 8px; }",
        "th { background: #eee; }",
        ".score { font-weight: bold; color: #006699; }",
        ".match { background: #fdf5e6; padding: 10px; margin-bottom: 15px; border-left: 4px solid #f39c12; }",
        ".query { color: #2c3e50; }",
        ".ref { color: #7f8c8d; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Plagiarism Detection Report</h1>",
    ]

    # --- Overall Scores Section ---
    html_content.append("<h2>Document Scores</h2>")
    html_content.append("<table>")
    html_content.append("<tr><th>Document</th><th>Score</th></tr>")
    for doc, score in results.get("doc_scores", {}).items():
        html_content.append(f"<tr><td>Document {doc}</td><td class='score'>{score:.3f}</td></tr>")
    html_content.append("</table>")

    # --- Matches Section ---
    html_content.append("<h2>Matches Found</h2>")
    for m in results.get("matches", []):
        html_content.append("<div class='match'>")
        html_content.append(f"<p><b>Document {m['doc']}</b> (Paragraph {m.get('para', 'N/A')})<br>")
        html_content.append(f"Score: <span class='score'>{m['score']:.3f}</span></p>")
        html_content.append(f"<p class='query'><b>Query Text:</b><br>{html.escape(m['query_text'])}</p>")
        html_content.append(f"<p class='ref'><b>Reference Text:</b><br>{html.escape(m['ref_text'])}</p>")
        html_content.append("</div>")

    html_content.append("</body></html>")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))


if __name__ == "__main__":
   
    results = {
        "doc_scores": {1: 0.384, 2: 0.15},
        "matches": [
            {
                "doc": 1,
                "para": 3,
                "score": 0.384,
                "query_text": "Deep learning is a subset of machine learning...",
                "ref_text": "Neural networks are a key component of deep learning..."
            }
        ]
    }

    save_html_report(results, ["doc1 content", "doc2 content"], "test_report.html")
    print("✅ Report generated: test_report.html")

