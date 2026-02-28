#!/bin/bash

# Create a concise README.md for the Lead Conversion API

cat > README.md << 'EOF'

# Lead Conversion Prediction API

Flask API serving a Random Forest model to predict banquet lead conversion (0/1) with probability percentage.

## Quick Start

1. Install: `pip install -r requirements.txt`
2. Run: `python app.py` (model must be in `model/best_model.pkl`)
3. Test:

```bash
curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "event_type": "Wedding",
    "branch": "Mumbai",
    "guest_count": 300,
    "budget": 500000,
    "lead_source": "Referral",
    "days_until_event": 45,
    "follow_up_count": 5,
    "property_visit_done": 1,
    "food_tasting_done": 1,
    "advance_paid": 0,
    "response_time_hours": 12.5
  }'
```
