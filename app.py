def normalize_query(query):
    q = query.lower().strip()

    # Remove filler words safely
    q = re.sub(r"\b(what is|calculate|find|the|result of)\b", "", q)

    # ----- STRUCTURED PHRASES -----
    q = re.sub(r"divide (\d+\.?\d*) by (\d+\.?\d*)", r"\1/\2", q)
    q = re.sub(r"multiply (\d+\.?\d*) by (\d+\.?\d*)", r"\1*\2", q)
    q = re.sub(r"subtract (\d+\.?\d*) from (\d+\.?\d*)", r"\2-\1", q)

    # Multi-number add
    def nums(text):
        return re.findall(r"\d+\.?\d*", text)

    q = re.sub(r"(add|sum of) ([\d,\sand]+)",
               lambda m: "+".join(nums(m.group(2))), q)

    q = re.sub(r"(product of) ([\d,\sand]+)",
               lambda m: "*".join(nums(m.group(2))), q)

    q = re.sub(r"(difference between) (\d+\.?\d*) and (\d+\.?\d*)",
               r"\2-\3", q)

    q = re.sub(r"(quotient of) (\d+\.?\d*) and (\d+\.?\d*)",
               r"\2/\3", q)

    # Percent
    q = re.sub(r"(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)", r"(\1/100)*\2", q)

    # Power
    q = re.sub(r"(\d+)\s*(power|to the power of)\s*(\d+)", r"\1**\3", q)

    # Word replacements (VERY IMPORTANT ORDER)
    replacements = {
        "divided by": "/",
        "plus": "+",
        "minus": "-",
        "times": "*",
        "x": "*",
        "×": "*",
        "over": "/",
        "÷": "/",
    }

    for word, sym in replacements.items():
        q = q.replace(word, sym)

    # 🚨 CRITICAL FIX: DO NOT REMOVE OPERATORS
    q = re.sub(r"[^0-9\.\+\-\*/\(\)\s]", " ", q)
    q = re.sub(r"\s+", " ", q)

    return q.strip()
