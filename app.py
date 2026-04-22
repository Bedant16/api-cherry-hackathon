from flask import Flask, request
import re

app = Flask(__name__)

def normalize_query(query):
    q = query.lower().strip()
    q = re.sub(r"\b(what is|calculate|find|the|result of)\b", "", q)
    q = q.replace("plus", "+")
    q = q.replace("minus", "-")
    q = q.replace("times", "*")
    q = q.replace("divided by", "/")
    q = re.sub(r"[^0-9\.\+\-\*/\(\)\s]", " ", q)
    q = re.sub(r"\s+", " ", q)
    return q.strip()

@app.route("/")
def home():
    return "API is running"

@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", ""))

    nums = list(map(int, re.findall(r'-?\d+', query)))
    total = sum(nums)

    return f"The sum is {total}.", 200, {
        "Content-Type": "text/plain; charset=utf-8"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
