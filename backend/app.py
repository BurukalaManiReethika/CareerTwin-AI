from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS = [
    "python",
    "java",
    "sql",
    "react",
    "flask",
    "django",
    "javascript",
    "c++"
]

@app.route("/")
def home():
    return {"message": "CareerTwin AI Backend Running"}

@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    file = request.files["resume"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    reader = PdfReader(filepath)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    found_skills = []

    lower_text = text.lower()

    for skill in SKILLS:
        if skill in lower_text:
            found_skills.append(skill)

    return jsonify({
        "skills": found_skills,
        "skill_count": len(found_skills)
    })

if __name__ == "__main__":
    app.run(debug=True)
