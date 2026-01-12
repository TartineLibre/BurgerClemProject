from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import config

app = Flask(__name__)
CORS(app)

COUNCIL_MEMBERS = config.COUNCIL_MEMBERS
CHAIRMAN_URL = config.CHAIRMAN_URL

print("\n" + "="*60)
print("FRONTEND STARTING WITH CONFIGURATION:")
print("="*60)
config.print_config()
print("\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health_check', methods=['GET'])
def health_check():
    """Check health of all services"""
    results = {
        'council_members': [],
        'chairman': None
    }
    
    for member in COUNCIL_MEMBERS:
        try:
            response = requests.get(f"{member['url']}/health", timeout=5)
            if response.status_code == 200:
                results['council_members'].append({
                    'id': member['id'],
                    'status': 'healthy',
                    'data': response.json()
                })
            else:
                results['council_members'].append({
                    'id': member['id'],
                    'status': 'unhealthy'
                })
        except Exception as e:
            results['council_members'].append({
                'id': member['id'],
                'status': 'unreachable',
                'error': str(e)
            })
    
    try:
        response = requests.get(f"{CHAIRMAN_URL}/health", timeout=5)
        if response.status_code == 200:
            results['chairman'] = {
                'status': 'healthy',
                'data': response.json()
            }
        else:
            results['chairman'] = {'status': 'unhealthy'}
    except Exception as e:
        results['chairman'] = {
            'status': 'unreachable',
            'error': str(e)
        }
    
    return jsonify(results)

@app.route('/submit_query', methods=['POST'])
def submit_query():
    """Handle the full council workflow"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        print(f"\n{'='*60}")
        print(f"NEW QUERY: {query}")
        print(f"{'='*60}\n")
        
        # Stage 1
        print("STAGE 1: Collecting answers from council members...")
        answers = []
        for member in COUNCIL_MEMBERS:
            try:
                print(f"  → Requesting answer from {member['id']}...")
                response = requests.post(
                    f"{member['url']}/answer",
                    json={'query': query},
                    timeout=120
                )
                if response.status_code == 200:
                    answer = response.json()
                    answers.append(answer)
                    print(f"  ✓ Received answer from {member['id']}")
            except Exception as e:
                print(f"  ✗ Error from {member['id']}: {e}")
        
        if not answers:
            return jsonify({'error': 'No answers received from council'}), 500
        
        print(f"\nStage 1 complete: {len(answers)} answers received\n")
        
        # Stage 2
        print("STAGE 2: Collecting reviews...")
        reviews = []
        for member in COUNCIL_MEMBERS:
            try:
                print(f"  → Requesting review from {member['id']}...")
                response = requests.post(
                    f"{member['url']}/review",
                    json={'query': query, 'answers': answers},
                    timeout=120
                )
                if response.status_code == 200:
                    review = response.json()
                    reviews.append(review)
                    print(f"  ✓ Received review from {member['id']}")
            except Exception as e:
                print(f"  ✗ Error from {member['id']}: {e}")
        
        print(f"\nStage 2 complete: {len(reviews)} reviews received\n")
        
        # Stage 3
        print("STAGE 3: Getting chairman synthesis...")
        try:
            print(f"  → Requesting synthesis from chairman...")
            chairman_response = requests.post(
                f"{CHAIRMAN_URL}/synthesize",
                json={
                    'query': query,
                    'answers': answers,
                    'reviews': reviews
                },
                timeout=180
            )
            
            if chairman_response.status_code == 200:
                chairman_result = chairman_response.json()
                print(f"  ✓ Synthesis complete")
            else:
                chairman_result = {'error': 'Chairman synthesis failed'}
                print(f"  ✗ Synthesis failed")
        except Exception as e:
            chairman_result = {'error': str(e)}
            print(f"  ✗ Error: {e}")
        
        print(f"\n{'='*60}")
        print("COUNCIL WORKFLOW COMPLETE")
        print(f"{'='*60}\n")
        
        return jsonify({
            'query': query,
            'stage1_answers': answers,
            'stage2_reviews': reviews,
            'stage3_synthesis': chairman_result
        })
        
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.FRONTEND_PORT, debug=True)