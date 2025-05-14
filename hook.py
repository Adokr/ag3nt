from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        osoby = request.get_json("https://letsplay.ag3nts.org/data/osoby.json")
       
        print(f"Odebrano dane: {osoby}")
        return "OK", 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()