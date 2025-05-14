from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        res = request.get_json()

        if "input" in res:
            return jsonify({"output": res["input"]})
        
        badania = request.get_json("https://letsplay.ag3nts.org/data/badania.json")
        return badania
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()