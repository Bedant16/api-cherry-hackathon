from flask import Flask, request, jsonify
import re
import ast
import operator

app = Flask(__name__)

# Allowed operators
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}

# Safe evaluator using AST
def safe_eval(expr):
    try:
        node = ast.parse(expr, mode='eval').body
        return evaluate(node)
    except Exception:
        return None

def evaluate(node):
    if isinstance(node, ast.Num):  # numbers
        return node.n

    elif isinstance(node, ast.BinOp):  # binary operations
        left = evaluate(node.left)
        right = evaluate(node.right)
        op = OPS[type(node.op)]

        if op == operator.truediv and right == 0:
            raise ZeroDivisionError

        return op(left, right)

    elif isinstance(node, ast.UnaryOp):  # negative numbers
        return OPS[type(node.op)](evaluate(node.operand))

    else:
        raise TypeError(node)

# Convert natural language → math expression
def normalize_query(query):
    query = query.lower()

    replacements = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "times": "*",
        "multiply": "*",
        "x": "*",
        "×": "*",
        "divide": "/",
        "divided by": "/",
        "÷": "/",
        "power": "**",
    }

    for word, sym in replacements.items():
        query = query.replace(word, sym)

    # remove unwanted words
    query = re.sub(r"[^\d\.\+\-\*/\(\)\s]", " ", query)
    query = re.sub(r"\s+", " ", query)

    return query.strip()

# Detect operation type
def detect_label(query):
    if re.search(r"\+", query):
        return "sum"
    elif re.search(r"-", query):
        return "difference"
    elif re.search(r"\*", query):
        return "product"
    elif re.search(r"/", query):
        return "quotient"
    elif re.search(r"\*\*", query):
        return "power"
    return "result"

@app.route("/")
def home():
    return "Optimized Math API is running 🚀"

@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")

    if not query:
        return jsonify({"output": "Please provide a query."})

    normalized = normalize_query(query)

    try:
        result = safe_eval(normalized)

        if result is None:
            return jsonify({"output": "I could not compute the result."})

        # format result
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        label = detect_label(normalized)

        return jsonify({"output": f"The {label} is {result}."})

    except ZeroDivisionError:
        return jsonify({"output": "Division by zero is not allowed."})

    except Exception:
        return jsonify({"output": "Invalid expression."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
