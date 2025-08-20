import os
from jinja2 import Template


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Plagiarism Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }
        h1, h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 30px; background: #fff; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        th { background: #eee; }
        .score { font-weight: bold; }
        .highlight { background: yellow; }
    </style>
</head>
<body>
    <h1>Plagiarism Detection Report</h1>

    <h2>Plagiarism Results</h2>
    {% if results %}
    <table>
        <tr>
            <th>Ref #</th>
            <th>Score</th>
            <th>Highlighted Text</th>
        </tr>
        {% for r in results %}
        <tr>
            <td>{{ r.ref_index }}</td>
            <td class="score">{{ "%.2f"|format(r.score) }}</td>
            <td>{{ r.highlighted|safe }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No plagiarism detected against reference documents.</p>
    {% endif %}

    <h2>Submission Collisions</h2>
    {% if collisions %}
    <table>
        <tr>
            <th>Previous Submission</th>
            <th>Similarity Score</th>
        </tr>
        {% for c in collisions %}
        <tr>
            <td>{{ c.file }}</td>
            <td class="score">{{ "%.2f"|format(c.score) }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No collisions detected with previous submissions.</p>
    {% endif %}
</body>
</html>
"""


def save_html_report(results, refs, output_file, collisions=None):
    """Generate and save HTML plagiarism report."""
    if collisions is None:
        collisions = []

    template = Template(HTML_TEMPLATE)
    html = template.render(results=results, collisions=collisions)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[INFO] Report saved to {output_file}")


