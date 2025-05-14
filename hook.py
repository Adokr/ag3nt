from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        print(f"Odebrano dane: {data}")
        return "OK", 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 4000

if __name__ == '__main__':
    app.run()