# 📚 Plagiarism Detector

A lightweight **plagiarism detection pipeline** built with Python.  
It supports **text (`.txt`)** and **PDF (`.pdf`)** files, uses **TF-IDF similarity + MinHash LSH** for candidate retrieval, and generates an **HTML report** with highlighted overlapping text.

---

## ✨ Features
- **Extract text** from PDF and TXT documents  
- **Normalize and tokenize** text for fair comparison  
- **Candidate pruning** with MinHash + LSH  
- **Similarity scoring** with TF-IDF cosine similarity  
- **Overlap highlighting** for explainability  
- **Generates a clean HTML report** with results  

---

⚙️ **Installation**

1. Clone the repository  
```bash
git clone https://github.com/<your-username>/plagiarism_detector.git
cd plagiarism_detector

2. Create a virtual environment

python -m venv .venv
.venv\Scripts\activate     # On Windows
source .venv/bin/activate  # On Linux/Mac

3. Run the plagiarism detector with:

python detector.py --query sample_data/query.pdf --refs sample_data/doc1.txt sample_data/doc2.txt sample_data/doc3.txt sample_data/doc4.txt sample_data/doc5.txt --report report.html




