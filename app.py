from flask import Flask, request, jsonify, render_template
from model.cyclone import chatbot_response
from model.resume_analyzer import analyze_resume, format_report_as_html

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").strip()

    if not msg:
        return jsonify({"response": "Please type a message first!"}), 400

    reply = chatbot_response(msg)
    return jsonify({"response": reply})

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume_api():
    """API endpoint to analyze resume"""
    try:
        data = request.get_json()
        resume_text = data.get("resume", "").strip()
        company = data.get("company", "Cyclone")

        if not resume_text:
            return jsonify({
                "success": False,
                "error": "No resume text provided"
            }), 400

        # Analyze the resume
        report = analyze_resume(resume_text, company)
        
        return jsonify({
            "success": True,
            "report": report,
            "html": format_report_as_html(report)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/health")
def health():
    bot_name = "Skill Sync"
    return jsonify({"status": "ok", "bot": bot_name})

if __name__ == "__main__":
    port = 5000
    app.run(debug=True, port=port)