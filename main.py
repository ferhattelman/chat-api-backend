from flask import Flask, request, jsonify
from processing import preprocessing, postprocessing
import asyncio

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_route():
    try:
        text = request.json.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400
        result = asyncio.run(preprocessing(text))
        return jsonify({"processed": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/postprocess", methods=["POST"])
def postprocess_route():
    try:
        text = request.json.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400
        result = asyncio.run(postprocessing(text))
        return jsonify({"postprocessed": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ping", methods=["GET"])
def ping():
    return "✅ Backend is alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
