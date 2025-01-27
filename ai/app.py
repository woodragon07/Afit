from flask import Flask, jsonify, request

app = Flask(__name__)

# 기본 라우트
@app.route('/')
def home():
    return "Hello, Flask Server!"

# JSON 데이터 반환 예제
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "This is a JSON response from the Flask server.",
        "status": "success"
    }
    return jsonify(data)

# POST 요청 처리 예제
@app.route('/api/echo', methods=['POST'])
def echo():
    if request.is_json:
        content = request.get_json()
        return jsonify({
            "received": content,
            "status": "success"
        })
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)
