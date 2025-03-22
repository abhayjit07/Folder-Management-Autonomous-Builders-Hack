from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Invalid request, 'text' field is required"}), 400

        file_content = data['text']

        #file_content is a string containing the file contents
        #call the model here or write this file somewhere and setup a routine to call the model
       

        return jsonify({"message": "Random message"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
