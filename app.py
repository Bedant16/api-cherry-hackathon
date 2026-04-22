from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route("/", methods=["POST"])
def answer():
    data = request.json
    query = data.get("query", "")
    assets = data.get("assets", [])
    
    # Fetch asset content if any
    asset_context = ""
    for url in assets:
        # fetch and append url content
        pass

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=100,
        system="""Answer questions in one concise sentence matching this style:
- Math sums: 'The sum is X.'
- Math differences: 'The difference is X.'  
- General: one direct sentence only. No extra words.""",
        messages=[{"role": "user", "content": query + asset_context}]
    )
    
    return jsonify({"output": message.content[0].text})

if __name__ == "__main__":
    app.run(port=8000)
