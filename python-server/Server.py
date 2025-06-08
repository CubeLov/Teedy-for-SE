from flask import Flask, request, jsonify
from Translate import translate_text
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/api/python-translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data['text']
        source_lang = data['source']
        target_lang = data['target']
        result = translate_text(text, source_lang, target_lang)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5001)
