from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama2')
MEMBER_ID = os.getenv('MEMBER_ID', 'member1')

@app.route('/health', methods=['GET'])
def health_check():
    """Check if the service and Ollama are running"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            return jsonify({
                'status': 'healthy',
                'member_id': MEMBER_ID,
                'model': MODEL_NAME,
                'ollama_status': 'connected'
            }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'member_id': MEMBER_ID,
            'error': str(e)
        }), 503

@app.route('/answer', methods=['POST'])
def generate_answer():
    """Generate an answer to the user query"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Call Ollama API
        ollama_response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                'model': MODEL_NAME,
                'prompt': f"Answer the following question concisely and accurately:\n\n{query}",
                'stream': False
            },
            timeout=120
        )
        
        if ollama_response.status_code == 200:
            result = ollama_response.json()
            return jsonify({
                'member_id': MEMBER_ID,
                'model': MODEL_NAME,
                'answer': result.get('response', '')
            }), 200
        else:
            return jsonify({'error': 'Ollama API error'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/review', methods=['POST'])
def review_answers():
    """Review and rank other members' answers"""
    try:
        data = request.json
        query = data.get('query', '')
        answers = data.get('answers', [])
        
        if not query or not answers:
            return jsonify({'error': 'Invalid request'}), 400
        
        # Anonymize answers
        anonymous_answers = []
        for idx, ans in enumerate(answers):
            if ans['member_id'] != MEMBER_ID:
                anonymous_answers.append({
                    'id': f"Answer_{idx+1}",
                    'text': ans['answer']
                })
        
        # Create review prompt
        answers_text = "\n\n".join([
            f"{ans['id']}:\n{ans['text']}" 
            for ans in anonymous_answers
        ])
        
        review_prompt = f"""Original Question: {query}

Below are multiple answers to this question. Evaluate each answer based on accuracy, insight, and completeness.

{answers_text}

Rank these answers from best to worst. Provide your ranking as a comma-separated list of IDs (e.g., "Answer_2, Answer_1, Answer_3").
Then briefly explain your reasoning for the top-ranked answer.

Format your response as:
RANKING: [your ranking]
REASONING: [your explanation]"""

        # Call Ollama for review
        ollama_response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                'model': MODEL_NAME,
                'prompt': review_prompt,
                'stream': False
            },
            timeout=120
        )
        
        if ollama_response.status_code == 200:
            result = ollama_response.json()
            review_text = result.get('response', '')
            
            # Parse ranking
            ranking = []
            reasoning = ""
            for line in review_text.split('\n'):
                if 'RANKING:' in line.upper():
                    ranking_str = line.split(':', 1)[1].strip()
                    ranking = [r.strip() for r in ranking_str.split(',')]
                elif 'REASONING:' in line.upper():
                    reasoning = line.split(':', 1)[1].strip()
            
            return jsonify({
                'member_id': MEMBER_ID,
                'ranking': ranking,
                'reasoning': reasoning,
                'full_review': review_text
            }), 200
        else:
            return jsonify({'error': 'Ollama API error'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)