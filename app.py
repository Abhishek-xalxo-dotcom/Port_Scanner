from flask import Flask, render_template, request, jsonify
from scanner import scan_target

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    target = data.get("target", "").strip()

    if not target:
        return jsonify({"error": "Target is required"}), 400

    results = scan_target(target)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
