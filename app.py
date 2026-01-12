from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import config
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

app = Flask(__name__)
CORS(app)

# Use configuration from config.py
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
    """Check health of all services in parallel"""
    results = {
        'council_members': [],
        'chairman': None
    }
    
    def check_member(member):
        try:
            response = requests.get(f"{member['url']}/health", timeout=5)
            if response.status_code == 200:
                return {
                    'id': member['id'],
                    'status': 'healthy',
                    'data': response.json()
                }
            else:
                return {
                    'id': member['id'],
                    'status': 'unhealthy'
                }
        except Exception as e:
            return {
                'id': member['id'],
                'status': 'unreachable',
                'error': str(e)
            }
    
    def check_chairman():
        try:
            response = requests.get(f"{CHAIRMAN_URL}/health", timeout=5)
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'data': response.json()
                }
            else:
                return {'status': 'unhealthy'}
        except Exception as e:
            return {
                'status': 'unreachable',
                'error': str(e)
            }
    
    # Parallel health checks
    with ThreadPoolExecutor(max_workers=len(COUNCIL_MEMBERS) + 1) as executor:
        # Submit all member checks
        member_futures = {executor.submit(check_member, member): member for member in COUNCIL_MEMBERS}
        chairman_future = executor.submit(check_chairman)
        
        # Collect member results
        for future in as_completed(member_futures):
            results['council_members'].append(future.result())
        
        # Get chairman result
        results['chairman'] = chairman_future.result()
    
    return jsonify(results)

@app.route('/submit_query', methods=['POST'])
def submit_query():
    """Handle the full council workflow with parallelization"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        print(f"\n{'='*60}")
        print(f"NEW QUERY: {query}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # ============================================
        # Stage 1: Collect answers in PARALLEL
        # ============================================
        print("STAGE 1: Collecting answers from council members (PARALLEL)...")
        
        def get_answer(member):
            try:
                print(f"  → Requesting answer from {member['id']}...")
                response = requests.post(
                    f"{member['url']}/answer",
                    json={'query': query},
                    timeout=300
                )
                if response.status_code == 200:
                    answer = response.json()
                    print(f"  ✓ Received answer from {member['id']}")
                    return answer
                else:
                    print(f"  ✗ Bad response from {member['id']}")
                    return None
            except Exception as e:
                print(f"  ✗ Error from {member['id']}: {e}")
                return None
        
        answers = []
        with ThreadPoolExecutor(max_workers=len(COUNCIL_MEMBERS)) as executor:
            future_to_member = {executor.submit(get_answer, member): member for member in COUNCIL_MEMBERS}
            
            for future in as_completed(future_to_member):
                result = future.result()
                if result:
                    answers.append(result)
        
        if not answers:
            return jsonify({'error': 'No answers received from council'}), 500
        
        stage1_time = time.time() - start_time
        print(f"\nStage 1 complete: {len(answers)} answers in {stage1_time:.1f}s\n")
        
        # ============================================
        # Stage 2: Get reviews in PARALLEL
        # ============================================
        print("STAGE 2: Collecting reviews (PARALLEL)...")
        
        def get_review(member):
            try:
                print(f"  → Requesting review from {member['id']}...")
                response = requests.post(
                    f"{member['url']}/review",
                    json={'query': query, 'answers': answers},
                    timeout=300
                )
                if response.status_code == 200:
                    review = response.json()
                    print(f"  ✓ Received review from {member['id']}")
                    return review
                else:
                    print(f"  ✗ Bad response from {member['id']}")
                    return None
            except Exception as e:
                print(f"  ✗ Error from {member['id']}: {e}")
                return None
        
        reviews = []
        with ThreadPoolExecutor(max_workers=len(COUNCIL_MEMBERS)) as executor:
            future_to_member = {executor.submit(get_review, member): member for member in COUNCIL_MEMBERS}
            
            for future in as_completed(future_to_member):
                result = future.result()
                if result:
                    reviews.append(result)
        
        stage2_time = time.time() - start_time - stage1_time
        print(f"\nStage 2 complete: {len(reviews)} reviews in {stage2_time:.1f}s\n")
        
        # ============================================
        # Stage 3: Get chairman synthesis
        # ============================================
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
                timeout=400
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
        
        total_time = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"COUNCIL WORKFLOW COMPLETE in {total_time:.1f}s")
        print(f"  Stage 1 (answers): {stage1_time:.1f}s")
        print(f"  Stage 2 (reviews): {stage2_time:.1f}s")
        print(f"  Stage 3 (synthesis): {total_time - stage1_time - stage2_time:.1f}s")
        print(f"{'='*60}\n")
        
        return jsonify({
            'query': query,
            'stage1_answers': answers,
            'stage2_reviews': reviews,
            'stage3_synthesis': chairman_result,
            'timing': {
                'total': total_time,
                'stage1': stage1_time,
                'stage2': stage2_time,
                'stage3': total_time - stage1_time - stage2_time
            }
        })
        
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.FRONTEND_PORT, debug=True)