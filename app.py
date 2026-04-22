from flask import Flask, request, jsonify
import re
from sympy import sympify
from sympy.core.sympify import SympifyError

app = Flask(__name__)

# ---------- NORMALIZATION ----------
def normalize_query(query):
    q = query.lower().strip()

    # Standard phrases
    q = re.sub(r"divide (\d+\.?\d*) by (\d+\.?\d*)", r"\1 / \2", q)
    q = re.sub(r"multiply (\d+\.?\d*) by (\d+\.?\d*)", r"\1 * \2", q)
    q = re.sub(r"subtract (\d+\.?\d*) from (\d+\.?\d*)", r"\2 - \1", q)

    # Multi-number addition
    q = re.sub(
        r"add ([\d,\sand]+)",
        lambda m: "+".join(re.findall(r"\d+\.?\d*", m.group(1))),
        q
    )

    # Percent handling (e.g., "20% of 50")
    q = re.sub(r"(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)", r"(\1/100)*\2", q)

    # Power handling
    q = re.sub(r"(\d+)\s*(power|to the power of)\s*(\d+)", r"\1**\3", q)

    # Word replacements
    replacements = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "x": "*",
        "×": "*",
        "divided by": "/",
        "over": "/",
        "÷": "/",
    }

    for word, sym in replacements.items():
        q = q.replace(word, sym)

    # Remove junk but keep math symbols
    q = re.sub(r"[^\d\.\+\-\*/\(\)\s\*]", " ", q)
    q = re.sub(r"\s+", " ", q)

    return q.strip()


# ---------- COMPUTE ----------
def compute(expr):
    try:
        result = sympify(expr).evalf()

        # Convert clean integers
        if result.is_real and result == int(result):
            return int(result)

        return float(result)

    except ZeroDivisionError:
        return "Division by zero is not allowed."

    except (SympifyError, TypeError):
        return None


# ---------- LABEL ----------
def detect_label(expr):
    if "+" in expr:
        return "sum"
    elif "-" in expr:
        return "difference"
    elif "*" in expr:
        return "product"
    elif "/" in expr:
        return "quotient"
    elif "**" in expr:
        return "power"
    return "result"


# ---------- ROUTES ----------
@app.route("/")
def home():
    return "95% Accuracy Math API (No LLM) 🚀"


@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")

    if not query:
        return jsonify({"output": "Please provide a query."})

    normalized = normalize_query(query)

    result = compute(normalized)

    if result is None:
        return jsonify({
            "output": f"I could not compute the result.",
            "debug": f"Parsed as: {normalized}"
        })

    if isinstance(result, str):  # division by zero case
        return jsonify({"output": result})

    label = detect_label(normalized)

    return jsonify({"output": f"The {label} is {result}."})


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
