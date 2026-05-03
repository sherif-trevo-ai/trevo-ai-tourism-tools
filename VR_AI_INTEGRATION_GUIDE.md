# VR and AI Integration Guide

Complete guide for implementing VR and AI features in your tourism website.

## Overview

This integration provides:

- **AI-Powered Recommendations**: Personalized destination suggestions based on user preferences
- **VR Tour Management**: Create, publish, and manage virtual reality tours
- **AI Chatbot**: Customer support and tourism information
- **Analytics Engine**: Track user behavior and identify trends
- **Experience Generator**: Customize VR experiences for users

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `flask` - Web framework
- `flask-cors` - Cross-origin support
- `python-dotenv` - Environment variables
- `requests` - HTTP library

### 2. Project Structure

```
api/
├── vr_ai_integration.py      # Core AI and VR classes
├── vr_ai_flask_app.py        # Flask REST API
└── tests/
    └── test_vr_ai.py         # Unit tests

website/
├── index.html                # Main website
├── js/
│   └── vr_ai_client.js      # JavaScript client
└── css/
    └── styles.css           # Styling
```

## Core Components

### 1. AIRecommendationEngine

Provides personalized destination recommendations using AI algorithms.

**Key Methods:**
- `add_user_profile()` - Register a user
- `get_personalized_recommendations()` - Get recommendations
- `track_user_interaction()` - Track user behavior

**Example:**
```python
from vr_ai_integration import AIRecommendationEngine, UserProfile

engine = AIRecommendationEngine()

profile = UserProfile(
    user_id="user_001",
    name="John Doe",
    preferences={
        "interest_tags": ["adventure", "nature"],
        "max_price": 500.0
    },
    visit_history=[],
    favorite_destinations=[],
    interaction_history=[]
)

engine.add_user_profile(profile)

recommendations = engine.get_personalized_recommendations(
    "user_001",
    destinations,
    limit=5
)
```

### 2. VRTourManager

Manages creation, publication, and analytics for VR tours.

**Key Methods:**
- `create_vr_tour()` - Create new tour
- `publish_tour()` - Make tour public
- `record_tour_view()` - Track views
- `rate_tour()` - User ratings
- `get_tour_analytics()` - Get statistics

**Example:**
```python
from vr_ai_integration import VRTourManager

manager = VRTourManager()

tour = manager.create_vr_tour(
    destination_id="dest_001",
    title="Ancient Temple Tour",
    description="Explore a centuries-old temple",
    scenes=12,
    duration_minutes=20
)

manager.publish_tour(tour.id)

manager.record_tour_view(
    tour_id=tour.id,
    user_id="user_001",
    session_duration=1200  # seconds
)
```

### 3. AIChatbot

AI-powered customer support chatbot.

**Key Methods:**
- `process_query()` - Process user questions
- `get_conversation_history()` - Retrieve chat history

**Example:**
```python
from vr_ai_integration import AIChatbot

chatbot = AIChatbot()

response = chatbot.process_query(
    user_id="user_001",
    query="How do I access VR tours?"
)

history = chatbot.get_conversation_history("user_001")
```

### 4. TourismAnalytics

Tracks visitor data and identifies trends.

**Key Methods:**
- `record_destination_visit()` - Log visits
- `get_destination_statistics()` - Get stats
- `get_trending_destinations()` - Find popular places

**Example:**
```python
from vr_ai_integration import TourismAnalytics

analytics = TourismAnalytics()

analytics.record_destination_visit(
    destination_id="dest_001",
    user_id="user_001",
    duration_minutes=45,
    rating=4.5
)

stats = analytics.get_destination_statistics("dest_001")
trending = analytics.get_trending_destinations(days=30)
```

### 5. VRExperienceGenerator

Create custom VR experiences for users.

**Key Methods:**
- `create_experience_template()` - Define template
- `customize_experience()` - Create custom version
- `get_user_experience()` - Retrieve user's experiences

**Example:**
```python
from vr_ai_integration import VRExperienceGenerator

generator = VRExperienceGenerator()

template = generator.create_experience_template(
    template_id="tmpl_001",
    name="Adventure Tour",
    description="Exciting adventure experiences",
    difficulty="advanced",
    environment_type="outdoor"
)

experience = generator.customize_experience(
    user_id="user_001",
    template_id="tmpl_001",
    customizations={"duration": 30, "theme": "jungle"}
)
```

## REST API Endpoints

### Users

**Create User Profile**
```
POST /api/users
Content-Type: application/json

{
    "user_id": "user_001",
    "name": "John Doe",
    "preferences": {
        "interest_tags": ["adventure", "nature"],
        "difficulty_level": "intermediate",
        "max_price": 500.0
    }
}
```

### Recommendations

**Get Personalized Recommendations**
```
GET /api/recommendations/<user_id>?limit=5
```

**Track User Interaction**
```
POST /api/interactions/<user_id>
Content-Type: application/json

{
    "destination_id": "dest_001",
    "interaction_type": "view",
    "duration_seconds": 300
}
```

### VR Tours

**Create VR Tour**
```
POST /api/tours
Content-Type: application/json

{
    "destination_id": "dest_001",
    "title": "Ancient Temple Tour",
    "description": "Explore a centuries-old temple",
    "scenes": 12,
    "duration_minutes": 20
}
```

**Publish Tour**
```
PUT /api/tours/<tour_id>/publish
```

**Record Tour View**
```
POST /api/tours/<tour_id>/view
Content-Type: application/json

{
    "user_id": "user_001",
    "session_duration": 1200
}
```

**Rate Tour**
```
POST /api/tours/<tour_id>/rate
Content-Type: application/json

{
    "rating": 4.5
}
```

**Get Tour Analytics**
```
GET /api/tours/<tour_id>/analytics
```

### Chatbot

**Send Chat Message**
```
POST /api/chat
Content-Type: application/json

{
    "user_id": "user_001",
    "query": "How do I access VR tours?"
}
```

**Get Chat History**
```
GET /api/chat/history/<user_id>
```

### Analytics

**Record Destination Visit**
```
POST /api/analytics/visits
Content-Type: application/json

{
    "destination_id": "dest_001",
    "user_id": "user_001",
    "duration_minutes": 45,
    "rating": 4.5
}
```

**Get Destination Statistics**
```
GET /api/analytics/destination/<destination_id>
```

**Get Trending Destinations**
```
GET /api/analytics/trending?days=30&limit=5
```

### Experiences

**Create Custom Experience**
```
POST /api/experiences
Content-Type: application/json

{
    "user_id": "user_001",
    "template_id": "tmpl_001",
    "customizations": {"duration": 30, "theme": "jungle"}
}
```

**Get User Experiences**
```
GET /api/experiences/<user_id>
```

### Health & Status

**Health Check**
```
GET /api/health
```

**System Status**
```
GET /api/status
```

## Running the API Server

### Development Mode

```bash
python api/vr_ai_flask_app.py
```

Server will run on `http://localhost:5000`

### Production Deployment

1. Install production WSGI server:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 api.vr_ai_flask_app:app
   ```

3. Configure with your web server (Nginx/Apache)

## JavaScript Client Integration

### Basic Setup

```javascript
const VRClient = {
    baseURL: 'http://localhost:5000/api',
    
    // Get recommendations
    async getRecommendations(userId, limit = 5) {
        const response = await fetch(
            `${this.baseURL}/recommendations/${userId}?limit=${limit}`
        );
        return await response.json();
    },
    
    // Track interaction
    async trackInteraction(userId, destinationId, type) {
        const response = await fetch(
            `${this.baseURL}/interactions/${userId}`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    destination_id: destinationId,
                    interaction_type: type,
                    duration_seconds: 0
                })
            }
        );
        return await response.json();
    },
    
    // Chat with AI bot
    async chat(userId, query) {
        const response = await fetch(
            `${this.baseURL}/chat`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    query: query
                })
            }
        );
        return await response.json();
    }
};

// Usage
VRClient.getRecommendations('user_001').then(data => {
    console.log('Recommendations:', data.recommendations);
});
```

## Features in Detail

### AI Recommendation Algorithm

The recommendation engine uses multiple factors:

1. **Base Rating** (40%) - Destination rating (0-5 stars)
2. **Tag Matching** (30%) - Match user interests with destination tags
3. **Difficulty Level** (20%) - Match preferred difficulty
4. **Price Match** (10%) - Check if within budget

Final score ranges from 0 to 1 (100%).

### VR Tour Analytics

Tracked metrics:
- View count
- Average session duration
- User ratings
- Completion rate
- Viewer demographics

### AI Chatbot Knowledge Base

Categories:
- VR tours information
- Booking and payments
- Destinations guide
- Technical support

### Tourism Trends

Analytics identifies:
- Most visited destinations
- Popular time periods
- User segments and preferences
- Revenue opportunities

## Security Considerations

### API Key Protection

```python
@app.route('/api/protected', methods=['GET'])
@require_api_key
def protected_endpoint():
    return jsonify({"data": "protected"})
```

Set API key in environment:
```bash
export API_KEY='your_secure_key'
```

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Data Privacy

- User profiles are stored in-memory (consider database for production)
- Implement proper authentication
- Encrypt sensitive data
- Regular security audits

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_recommendations_cached(user_id):
    return recommendation_engine.get_personalized_recommendations(
        user_id,
        destinations
    )
```

### Database Integration

Replace in-memory storage with database:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/tourism_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
```

## Testing

### Unit Tests

```python
import unittest
from vr_ai_integration import *

class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AIRecommendationEngine()
    
    def test_add_user_profile(self):
        profile = UserProfile(
            user_id="test_001",
            name="Test User",
            preferences={},
            visit_history=[],
            favorite_destinations=[],
            interaction_history=[]
        )
        result = self.engine.add_user_profile(profile)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest tests/
```

## Troubleshooting

### API Connection Issues

1. Check server is running
2. Verify correct URL and port
3. Check CORS configuration
4. Review API logs

### Recommendation Issues

1. Ensure user profile is created
2. Check user preferences format
3. Verify destination data
4. Check recommendation scores

### VR Tour Problems

1. Verify VR URL format
2. Check scene configuration
3. Test video playback
4. Review browser compatibility

## Future Enhancements

- [ ] Real-time multiplayer VR tours
- [ ] Advanced ML models for recommendations
- [ ] 3D destination scanning
- [ ] AI-generated tour narration
- [ ] Blockchain for booking verification
- [ ] IoT sensor integration
- [ ] AR overlay features
- [ ] Voice-controlled navigation

## Support and Documentation

- GitHub Issues: Report bugs and feature requests
- Documentation: See inline code comments
- Examples: Check vr_ai_integration.py for usage examples
- API Tests: Use provided test cases

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please follow CONTRIBUTING.md guidelines.
