from flask import Flask, request
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running"

@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", ""))

    numbers = re.findall(r"\d+", query)
    total = sum(map(int, numbers))

    return f"The sum is {total}.", 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
