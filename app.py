import os
from flask import Flask, request, jsonify
import nltk
nltk.download('stopwords')
from pyresparser import ResumeParser

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return """
    <body style='text-align: center;'>
        <form method="post" action="/" enctype = "multipart/form-data">
            <input name="file" type="file"/>
            <button>Submit</button>
        </form>
    </body>
    """


@app.route('/', methods=['POST'])
def parse_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        file = request.files['file']
        if file.filename.endswith('.pdf') == False:
            return jsonify({'error': 'File must be a PDF'})
        file_path = os.path.join(os.getcwd(), file.filename)
        file.save(file_path)

        data = ResumeParser(file_path).get_extracted_data()
        os.remove(file_path)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": e})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True,
            host='0.0.0.0', port=os.getenv('PORT', 9050))
