from flask import Flask, request, jsonify
import re
import operator

app = Flask(__name__)

# Safely evaluate simple math expressions
def safe_eval(expr):
    expr = expr.strip()
    # Handle basic operations: +, -, *, /
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '×': operator.mul,
        'x': operator.mul,
        '/': operator.truediv,
        '÷': operator.truediv,
    }

    # Try to match: number op number (with optional spaces)
    match = re.search(r'(-?\d+\.?\d*)\s*([+\-*/×x÷])\s*(-?\d+\.?\d*)', expr)
    if match:
        a = float(match.group(1))
        op_sym = match.group(2)
        b = float(match.group(3))
        result = ops[op_sym](a, b)
        # Return int if result is whole number
        return int(result) if result == int(result) else result

    # Fallback: sum all numbers found
    nums = list(map(float, re.findall(r'-?\d+\.?\d*', expr)))
    if nums:
        total = sum(nums)
        return int(total) if total == int(total) else total

    return None

def format_result(result):
    """Format result to match expected output style."""
    if result is None:
        return "I could not compute the result."
    return f"The sum is {result}."

@app.route("/")
def home():
    return "API is running"

@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").lower()

    result = safe_eval(query)

    # Detect operation type for better output phrasing
    if re.search(r'[+]|add|plus|sum|total', query):
        label = "sum"
    elif re.search(r'[-]|subtract|minus|difference', query):
        label = "difference"
    elif re.search(r'[*×x]|multiply|times|product', query):
        label = "product"
    elif re.search(r'[/÷]|divide|quotient', query):
        label = "quotient"
    else:
        label = "sum"

    if result is not None:
        val = int(result) if isinstance(result, float) and result == int(result) else result
        response = f"The {label} is {val}."
    else:
        response = "I could not compute the result."

    return jsonify({"output": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
