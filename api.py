import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'best_model.pkl')
model = joblib.load(MODEL_PATH)

def compute_derived_features(data):
    derived = {}
    derived['budget_per_guest'] = data['budget'] / data['guest_count']
    derived['engagement_score'] = (
        data['follow_up_count'] * 0.3 +
        data['property_visit_done'] * 2.5 +
        data['food_tasting_done'] * 3.5 +
        data['advance_paid'] * 4.0
    )
    derived['urgency_index'] = 1.0 / data['days_until_event']
    return derived

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_json = request.get_json()
        if not input_json:
            return jsonify({'error': 'No input data provided'}), 400

        derived = compute_derived_features(input_json)

        columns_order = [
            'event_type', 'branch', 'guest_count', 'budget', 'lead_source',
            'days_until_event', 'follow_up_count', 'property_visit_done',
            'food_tasting_done', 'advance_paid', 'response_time_hours',
            'budget_per_guest', 'engagement_score', 'urgency_index'
        ]
        input_data = {**input_json, **derived}
        input_df = pd.DataFrame([input_data])[columns_order]

        pred_class = model.predict(input_df)[0]
        pred_proba = model.predict_proba(input_df)[0][1]

        response = {
            'predicted_class': int(pred_class),
            'probability_percent': round(pred_proba * 100, 2)
        }
        return jsonify(response)

    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'guest_count and days_until_event must be non-zero'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)