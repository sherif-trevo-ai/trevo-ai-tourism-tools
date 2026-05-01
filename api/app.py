from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.content_generator import TrevoContentGenerator

app = Flask(__name__)
CORS(app)

content_gen = TrevoContentGenerator()

# محاكاة قاعدة بيانات بسيطة في الذاكرة لتبدو المنصة "حية"
system_data = {
    "total_campaigns_run": 0
}

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "Trevo Enterprise OS Online", "version": "1.5.0-MVP"})

@app.route('/api/generate-ai-content', methods=['POST'])
def generate_ai_content():
    data = request.json
    location = data.get('location', 'Unknown Destination')
    style = data.get('style', 'luxury')
    audience = data.get('audience', 'High Net Worth Individuals') # إضافة الجمهور
    
    copy = content_gen.generate_copy(location, style, audience)
    system_data["total_campaigns_run"] += 1
    
    return jsonify({
        "copy": copy, 
        "campaigns_run": system_data["total_campaigns_run"]
    })

@app.route('/api/calculate-roi', methods=['POST'])
def calculate_roi():
    data = request.json
    revenue = float(data.get('revenue', 0))
    cost = float(data.get('cost', 1))
    roi = round(((revenue - cost) / cost) * 100, 2)
    return jsonify({"roi_percentage": roi})

if __name__ == '__main__':
    app.run(debug=True, port=5000)