from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        res = request.get_json()

        if "input" in res:
            return jsonify({"output": res["input"]}), 200
        
        badania = request.get_json("https://letsplay.ag3nts.org/data/badania.json")
        
        matched = []
        if isinstance(badania, list):
            for item in badania:
                nazwa = item.get("nazwa", "")
                if isinstance(nazwa, str) and re.search(r"(czas[a-z]{0,2})", nazwa.lower()) and re.search(r"(podróż[a-z]{0,4})", nazwa.lower()):
                    matched.append(item.get("uczelnia", ""))
                    matched.append(item.get("sponsor", ""))

        return jsonify({"uczelnia": matched[0],
                        "sponsor": matched[1]})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()