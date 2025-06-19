from flask import Flask, request, jsonify
from rag_utils import process_pdf
from agents import analyze_pitch_deck
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 
# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

current_collection = None

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_collection
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Only PDF files are allowed."}), 400
    
    try:
        current_collection = process_pdf(file)
        return jsonify({"message": "File processed successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500

@app.route('/analyze', methods=['GET'])
def analyze_document():
    global current_collection
    if not current_collection:
        return jsonify({"error": "No document available for analysis"}), 400
    
    try:
        # Run multi-agent analysis
        analysis = analyze_pitch_deck(current_collection)
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)