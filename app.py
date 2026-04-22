from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "API Running"

@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")

    nums = list(map(int, re.findall(r'\d+', query)))
    total = sum(nums)

    return jsonify({
        "output": f"The sum is {total}."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
