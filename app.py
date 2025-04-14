from flask import Flask, request, jsonify, render_template
from services.sql_server_connector import fetch_sql_server_metadata
from models.gemini_model import query_gemini
from services.prompt_handler import get_default_prompt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    model = data.get('model')
    question = data.get('question')
    db_config = data.get('db_config')

    try:
        # Fetch metadata from the local SQL Server
        if db_config['type'] == 'local-sql-server':
            metadata = fetch_sql_server_metadata(db_config['host'], db_config['database'])
        else:
            return jsonify({'error': 'Unsupported database type'}), 400

        # Generate the prompt using the prompt handler
        prompt = get_default_prompt(metadata, question)

        # Query the selected AI model
        if model == 'gemini':
            response = query_gemini(prompt)
        else:
            return jsonify({'error': 'Unsupported AI model'}), 400

        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)