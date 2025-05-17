from flask import Flask, request, jsonify
import re
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    res = request.get_json(silent=True)
    if res and "input" in res:
        return jsonify({"output": res["input"]}), 200
    else:
        try:
            res = requests.get("https://letsplay.ag3nts.org/data/badania.json")
            res.raise_for_status()
            badania = res.json()
            matched = {}
            if isinstance(badania, list):
                for item in badania:
                    nazwa = item.get("nazwa", "")
                    if isinstance(nazwa, str) and re.search(r"(czas[a-z]{0,2})", nazwa.lower()) and re.search(r"(podróż[a-z]{0,4})", nazwa.lower()):
                        matched["uczelnia"] = item.get("uczelnia", "")
                        matched["sponso"] = item.get("sponsor", "")

            print(matched)
            return jsonify({"output": matched})

        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route('/webhook2', methods=['POST'])
def webhook2():
    res = request.get_json(silent=True)
    if res and "input" in res and re.match(r"test", res["input"]):
        return jsonify({"output": res["input"]}), 200
    
    else: 
        try:
            szukana_uczelnia = res["input"]
            res2 = requests.get("https://letsplay.ag3nts.org/data/osoby.json")
            osoby = res2.json()
            print("LOL")
            res3 = requests.get("https://letsplay.ag3nts.org/data/uczelnie.json")
            uczelnie = res3.json()

            matched = []
            if isinstance(osoby, list):
                for item in osoby:
                    uczelnia = item.get("uczelnia", "")
                    if szukana_uczelnia == uczelnia:
                        matched.append({"imie": item.get("imie", ""), "nazwisko": item.get("nazwisko", "")})
           

            if isinstance(uczelnie, list):
                for item in uczelnie:
                    id_uczelni = item.get("id", "")
                    if id_uczelni == szukana_uczelnia:
                        matched.append({"uczelnia": item.get("nazwa", "")})
            print(matched)
            return jsonify(matched)

        except Exception as e:
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)