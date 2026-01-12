from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import traceback
import sys

app = Flask(__name__)
CORS(app)


OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'phi')
PORT = int(os.getenv('PORT', 5000))

print(f"\n{'='*40}")
print(f"CHAIRMAN STARTING...")
print(f"Model: {MODEL_NAME}")
print(f"Port: {PORT}")
print(f"Ollama: {OLLAMA_HOST}")
print(f"{'='*40}\n")

@app.route('/health', methods=['GET'])
def health_check():
    """Check if the chairman service is running"""
    try:
        # Test connection to Ollama
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            return jsonify({
                'status': 'healthy',
                'role': 'chairman',
                'model': MODEL_NAME,
                'ollama_status': 'connected'
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'role': 'chairman',
                'error': 'Ollama responded but with error'
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'role': 'chairman',
            'error': str(e)
        }), 503

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Synthesize all answers and reviews into a final response"""
    try:
        print("\n--- NEW SYNTHESIS REQUEST RECEIVED ---")
        
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        query = data.get('query', '')
        answers = data.get('answers', [])
        reviews = data.get('reviews', [])
        
        print(f"Query: {query}")
        print(f"Answers received: {len(answers)}")
        print(f"Reviews received: {len(reviews)}")

        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Build synthesis prompt
        answers_text = "\n\n".join([
            f"Response from {ans.get('member_id', 'Unknown')} (Model: {ans.get('model', 'Unknown')}):\n{ans.get('answer', 'No text')}"
            for ans in answers
        ])
        
        reviews_text = "\n\n".join([
            f"Review by {rev.get('member_id', 'Unknown')}:\nRanking: {', '.join(rev.get('ranking', []))}\nReasoning: {rev.get('reasoning', 'N/A')}"
            for rev in reviews
        ])
        
        synthesis_prompt = f"""You are the Chairman of an LLM Council. 
ORIGINAL QUESTION: {query}

COUNCIL RESPONSES:
{answers_text}

PEER REVIEWS:
{reviews_text}

Based on these responses and reviews, provide a final, synthesized answer that represents the best collective wisdom.
Your final answer:"""

        print(f"Sending prompt to Ollama ({len(synthesis_prompt)} chars)...")
        print("Waiting for generation (Timeout: 300s)...")

        # Call Ollama for synthesis
        ollama_response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                'model': MODEL_NAME,
                'prompt': synthesis_prompt,
                'stream': False,
                # Options pour éviter de dépasser la mémoire
                'options': {
                    'num_ctx': 2048, # Contexte large pour lire toutes les réponses
                    'temperature': 0.7
                }
            },
            timeout=300  # 5 minutes timeout
        )
        
        if ollama_response.status_code == 200:
            result = ollama_response.json()
            generated_text = result.get('response', '')
            print("✓ Synthesis generated successfully!")
            
            return jsonify({
                'role': 'chairman',
                'model': MODEL_NAME,
                'final_answer': generated_text
            }), 200
        else:
            # GESTION D'ERREUR DETAILLEE
            error_msg = f"Ollama Error ({ollama_response.status_code}): {ollama_response.text}"
            print(f"!!! {error_msg} !!!")
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        # GESTION DE CRASH PYTHON
        print("!!! PYTHON EXCEPTION !!!")
        traceback.print_exc()
        return jsonify({'error': f"Server Exception: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)