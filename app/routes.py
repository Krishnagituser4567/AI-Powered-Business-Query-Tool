from flask import render_template, request, jsonify
from app import app
from services.sql_server_connector import fetch_sql_server_metadata
from services.prompt_handler import get_default_prompt
from models.gemini_model import query_gemini
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt')
def prompt():
    default_prompt = get_default_prompt(metadata="Sample metadata", question=None)
    return render_template('prompt.html', default_prompt=default_prompt)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    model = data.get('model')  # Get the model from the UI
    api_key = data.get('api_key')
    question = data.get('question')
    db_config = data.get('db_config')

    try:
        # Store the API key in the environment variables dynamically
        if model.startswith('gemini'):
            os.environ['GEMINI_API_KEY'] = api_key
        elif model == 'text-davinci-003':
            os.environ['OPENAI_API_KEY'] = api_key
        elif model == 'azure-ai':
            os.environ['AZURE_API_KEY'] = api_key
        else:
            return jsonify({'error': 'Unsupported AI model'}), 400

        # Fetch metadata from the local SQL Server
        if db_config['type'] == 'local-sql-server':
            metadata = fetch_sql_server_metadata(db_config['host'], db_config['database'])
        else:
            return jsonify({'error': 'Unsupported database type'}), 400

        # Generate the prompt using the prompt handler
        prompt = get_default_prompt(metadata, question)

        # Query the selected AI model
        if model.startswith('gemini'):
            response = query_gemini(prompt, model=model)
        else:
            return jsonify({'error': 'Unsupported AI model'}), 400

        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500