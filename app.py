from flask import Flask, request
import re
from sympy import sympify
from sympy.core.sympify import SympifyError

app = Flask(__name__)

def normalize(query):
    q = query.lower().strip().replace("?", "")

    # Filler removal
    for f in ["what is", "what's", "calculate", "find", "compute", "solve"]:
        q = q.replace(f, " ")

    # Phrase patterns
    q = re.sub(r"divide\s+(\d+\.?\d*)\s+by\s+(\d+\.?\d*)",     r"\1/\2", q)
    q = re.sub(r"multiply\s+(\d+\.?\d*)\s+by\s+(\d+\.?\d*)",   r"\1*\2", q)
    q = re.sub(r"subtract\s+(\d+\.?\d*)\s+from\s+(\d+\.?\d*)", r"\2-\1", q)
    q = re.sub(r"(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)",          r"(\1/100)*\2", q)
    q = re.sub(r"(\d+\.?\d*)\s*squared",                        r"\1**2", q)
    q = re.sub(r"(\d+\.?\d*)\s*cubed",                          r"\1**3", q)
    q = re.sub(r"square\s+root\s+of\s+(\d+\.?\d*)",             r"sqrt(\1)", q)
    q = re.sub(r"(\d+)\s*(?:to the power of|raised to)\s*(\d+)",r"\1**\2", q)
    q = re.sub(r"\^", "**", q)

    # Word → symbol
    for word, sym in [("divided by","/"),("multiplied by","*"),
                      ("plus","+"),("minus","-"),("times","*"),("over","/"),
                      ("×","*"),("÷","/")]:
        q = q.replace(word, sym)

    q = re.sub(r'\bx\b', '*', q)
    q = re.sub(r"[^\d\.\+\-\*\/\(\)\s]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    return q

def detect_label(original, normalized):
    q = original.lower()
    if any(w in q for w in ["sum","add","plus","total"]):        return "sum"
    if any(w in q for w in ["subtract","minus","difference"]):   return "difference"
    if any(w in q for w in ["multiply","times","product"]):      return "product"
    if any(w in q for w in ["divide","quotient","divided by"]):  return "quotient"
    if any(w in q for w in ["power","squared","cubed","root"]):  return "power"
    if "**" in normalized:   return "power"
    if "+" in normalized:    return "sum"
    if "/" in normalized:    return "quotient"
    if "*" in normalized:    return "product"
    if "-" in normalized:    return "difference"
    return "result"

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running"

@app.route("/v1/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", "")).strip()

    if not query:
        return "Please provide a query."

    normalized = normalize(query)

    try:
        from sympy import sqrt, pi, E
        result = sympify(normalized, locals={"sqrt": sqrt, "pi": pi, "e": E}).evalf()
        val = float(result)
        val = int(val) if val == int(val) else round(val, 6)
        label = detect_label(query, normalized)
        return f"The {label} is {val}."
    except ZeroDivisionError:
        return "Division by zero is not allowed."
    except Exception:
        return "I could not compute the result."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
