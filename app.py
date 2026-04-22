from flask import Flask, request
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running"

@app.route("/v1/answer", methods=["POST"])
def answer():
    try:
        data = request.get_json(silent=True) or {}
        query = str(data.get("query", "")).lower().strip()

        # extract numbers
        nums = list(map(int, re.findall(r'-?\d+', query)))

        # LEVEL 1 exact expected output
        if "+" in query or "add" in query or "sum" in query:
            total = sum(nums)
            return f"The sum is {total}.", 200, {
                "Content-Type": "text/plain; charset=utf-8"
            }

        # fallback if only two numbers given
        if len(nums) >= 2:
            total = sum(nums)
            return f"The sum is {total}.", 200, {
                "Content-Type": "text/plain; charset=utf-8"
            }

        return "Invalid query", 200, {
            "Content-Type": "text/plain; charset=utf-8"
        }

    except:
        return "Error", 200, {
            "Content-Type": "text/plain; charset=utf-8"
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
