# VR and AI Integration Testing Guide for v1 & v2

Complete guide for testing the VR and AI tourism integration in your v1 and v2 versions.

## 🚀 Quick Start - Test in 5 Minutes

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Navigate to project
cd trevo-ai-tourism-tools
```

### Start the API Server
```bash
# Option 1: Run the v1 API server
python api/vr_ai_flask_app_v1.py

# Output should show:
# Starting VR and AI Tourism API (v1)...
# Running on http://localhost:5000
```

## 📋 Testing Checklist

### ✅ Phase 1: Server Health Check (30 seconds)

**Test 1.1: Health Endpoint**
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-03T05:30:00.000000",
  "version": "v1.0"
}
```

**Test 1.2: System Status**
```bash
curl http://localhost:5000/api/status
```

---

### ✅ Phase 2: User Management (1 minute)

**Test 2.1: Create User Profile**
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "name": "John Traveler",
    "preferences": {
      "interest_tags": ["adventure", "nature", "cultural"],
      "difficulty_level": "intermediate",
      "max_price": 500.0
    }
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "User profile created successfully",
  "user_id": "user_001",
  "timestamp": "2026-05-03T05:30:15.000000"
}
```

**Test 2.2: Create Multiple Users**
```bash
# User 2
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_002",
    "name": "Sarah Explorer",
    "preferences": {
      "interest_tags": ["relaxation", "beach", "wellness"],
      "difficulty_level": "beginner",
      "max_price": 300.0
    }
  }'

# User 3
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_003",
    "name": "Mike Adventurer",
    "preferences": {
      "interest_tags": ["hiking", "adventure", "extreme"],
      "difficulty_level": "advanced",
      "max_price": 1000.0
    }
  }'
```

---

### ✅ Phase 3: AI Recommendations (2 minutes)

**Test 3.1: Get Recommendations for User 1**
```bash
curl "http://localhost:5000/api/recommendations/user_001?limit=5"
```

Expected response shows personalized recommendations:
```json
{
  "user_id": "user_001",
  "count": 5,
  "recommendations": [
    {
      "destination_id": "dest_002",
      "name": "Mountain Adventure Trail",
      "location": "Swiss Alps",
      "recommendation_score": 0.95,
      "match_percentage": "95.0%",
      "vr_available": true,
      "price": 39.99
    },
    ...
  ],
  "timestamp": "2026-05-03T05:30:30.000000"
}
```

**Test 3.2: Compare Recommendations Across Users**
```bash
# Get recommendations for user_002 (beach/relaxation preference)
curl "http://localhost:5000/api/recommendations/user_002?limit=3"

# Get recommendations for user_003 (adventure preference)
curl "http://localhost:5000/api/recommendations/user_003?limit=3"
```

**Observation:** Notice how recommendations differ based on user preferences!

---

### ✅ Phase 4: User Interactions (1 minute)

**Test 4.1: Track User Interest in Destination**
```bash
curl -X POST http://localhost:5000/api/interactions/user_001 \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_002",
    "interaction_type": "view",
    "duration_seconds": 300
  }'
```

**Test 4.2: Track Multiple Interactions**
```bash
# Click interaction
curl -X POST http://localhost:5000/api/interactions/user_001 \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_001",
    "interaction_type": "click",
    "duration_seconds": 0
  }'

# Bookmark interaction
curl -X POST http://localhost:5000/api/interactions/user_002 \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_003",
    "interaction_type": "bookmark",
    "duration_seconds": 0
  }'
```

---

### ✅ Phase 5: VR Tours Management (2 minutes)

**Test 5.1: Create a VR Tour**
```bash
curl -X POST http://localhost:5000/api/tours \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_001",
    "title": "Ancient Temple Complex Tour",
    "description": "360-degree immersive tour of ancient temple ruins",
    "scenes": 12,
    "duration_minutes": 20
  }'
```

Expected response:
```json
{
  "success": true,
  "tour_id": "550e8400-e29b-41d4-a716-446655440000",
  "destination_id": "dest_001",
  "title": "Ancient Temple Complex Tour",
  "is_published": false,
  "timestamp": "2026-05-03T05:30:45.000000"
}
```

**Test 5.2: Publish the Tour**
```bash
# Replace with tour_id from previous response
curl -X PUT http://localhost:5000/api/tours/550e8400-e29b-41d4-a716-446655440000/publish
```

**Test 5.3: Record Tour Views**
```bash
curl -X POST http://localhost:5000/api/tours/550e8400-e29b-41d4-a716-446655440000/view \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "session_duration": 1200
  }'
```

**Test 5.4: Rate the Tour**
```bash
curl -X POST http://localhost:5000/api/tours/550e8400-e29b-41d4-a716-446655440000/rate \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4.8
  }'
```

**Test 5.5: Get Tour Analytics**
```bash
curl http://localhost:5000/api/tours/550e8400-e29b-41d4-a716-446655440000/analytics
```

Response shows:
```json
{
  "tour_id": "550e8400-e29b-41d4-a716-446655440000",
  "tour_title": "Ancient Temple Complex Tour",
  "created_date": "2026-05-03T05:30:45.000000",
  "view_count": 1,
  "avg_session_duration": 1200.0,
  "avg_rating": 4.8
}
```

---

### ✅ Phase 6: AI Chatbot (1 minute)

**Test 6.1: Ask Question**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "query": "How do I access VR tours?"
  }'
```

Expected response:
```json
{
  "user_id": "user_001",
  "query": "How do I access VR tours?",
  "response": "VR tours are immersive virtual reality experiences of destinations. You can access VR tours through our website.",
  "timestamp": "2026-05-03T05:30:55.000000",
  "confidence": 0.85
}
```

**Test 6.2: Different Questions**
```bash
# Booking question
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_002",
    "query": "How do I book a tour?"
  }'

# Technical question
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_003",
    "query": "I am having technical issues"
  }'
```

**Test 6.3: Get Chat History**
```bash
curl http://localhost:5000/api/chat/history/user_001
```

---

### ✅ Phase 7: Tourism Analytics (1 minute)

**Test 7.1: Record Destination Visits**
```bash
curl -X POST http://localhost:5000/api/analytics/visits \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_001",
    "user_id": "user_001",
    "duration_minutes": 45,
    "rating": 4.5
  }'
```

**Test 7.2: Record Multiple Visits**
```bash
# Visit 2
curl -X POST http://localhost:5000/api/analytics/visits \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_001",
    "user_id": "user_002",
    "duration_minutes": 30,
    "rating": 4.8
  }'

# Visit 3
curl -X POST http://localhost:5000/api/analytics/visits \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": "dest_002",
    "user_id": "user_001",
    "duration_minutes": 60,
    "rating": 4.9
  }'
```

**Test 7.3: Get Destination Statistics**
```bash
curl http://localhost:5000/api/analytics/destination/dest_001
```

Response shows:
```json
{
  "destination_id": "dest_001",
  "total_visits": 2,
  "average_rating": 4.65,
  "average_duration_minutes": 37.5,
  "unique_users": 2
}
```

**Test 7.4: Get Trending Destinations**
```bash
curl "http://localhost:5000/api/analytics/trending?days=30&limit=5"
```

---

### ✅ Phase 8: View All Destinations (30 seconds)

**Test 8.1: List Available Destinations**
```bash
curl http://localhost:5000/api/destinations
```

Response shows all 5 sample destinations:
```json
{
  "count": 5,
  "destinations": [
    {
      "id": "dest_001",
      "name": "Ancient Temple Complex",
      "location": "Southeast Asia",
      "rating": 4.8,
      "price": 29.99,
      "vr_available": true,
      "difficulty_level": "intermediate",
      "tags": ["cultural", "historical", "spiritual"]
    },
    ...
  ]
}
```

---

## 🧪 Automated Testing Script

Create `test_vr_ai_api.sh`:

```bash
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:5000/api"

echo -e "${BLUE}=== VR and AI Tourism API Test Suite ===${NC}\n"

# Health check
echo -e "${BLUE}1. Health Check${NC}"
curl -s $BASE_URL/health | python -m json.tool
echo -e "\n"

# Create user
echo -e "${BLUE}2. Create User${NC}"
curl -s -X POST $BASE_URL/users \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test_user_001","name":"Test User","preferences":{}}' | python -m json.tool
echo -e "\n"

# Get recommendations
echo -e "${BLUE}3. Get Recommendations${NC}"
curl -s "$BASE_URL/recommendations/test_user_001?limit=3" | python -m json.tool
echo -e "\n"

# Get destinations
echo -e "${BLUE}4. List Destinations${NC}"
curl -s $BASE_URL/destinations | python -m json.tool
echo -e "\n"

# Chat
echo -e "${BLUE}5. AI Chatbot${NC}"
curl -s -X POST $BASE_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test_user_001","query":"What are VR tours?"}' | python -m json.tool
echo -e "\n"

echo -e "${GREEN}✓ Test Suite Completed${NC}"
```

Run it:
```bash
chmod +x test_vr_ai_api.sh
./test_vr_ai_api.sh
```

---

## 🔗 Integration with v1 and v2 Websites

### For v1 (dashboard.html / index.html)

Add this to your HTML files to test VR integration:

```html
<!-- Add to v1/dashboard.html or v1/index.html -->
<script>
// VR and AI Client
const VRClient = {
    baseURL: 'http://localhost:5000/api',
    
    // Get recommendations
    async getRecommendations(userId) {
        try {
            const response = await fetch(
                `${this.baseURL}/recommendations/${userId}?limit=5`
            );
            const data = await response.json();
            console.log('Recommendations:', data.recommendations);
            return data.recommendations;
        } catch(error) {
            console.error('Error:', error);
        }
    },
    
    // Create user
    async createUser(userId, name, preferences) {
        try {
            const response = await fetch(`${this.baseURL}/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, name, preferences })
            });
            return await response.json();
        } catch(error) {
            console.error('Error:', error);
        }
    },
    
    // Chat with AI
    async chat(userId, query) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, query })
            });
            const data = await response.json();
            console.log('AI Response:', data.response);
            return data.response;
        } catch(error) {
            console.error('Error:', error);
        }
    }
};

// Initialize with current user
const currentUserId = 'visitor_' + Date.now();

// Test: Create user and get recommendations
VRClient.createUser(currentUserId, 'Visitor', {
    interest_tags: ['adventure', 'nature'],
    difficulty_level: 'intermediate',
    max_price: 500
}).then(() => {
    VRClient.getRecommendations(currentUserId);
});
</script>
```

### For v2 (index.html / dashboard.html)

Same integration applies - v2 can use the exact same client code.

---

## 📊 Testing Results Dashboard

After running all tests, you should see:

| Component | Status | Tests Passed |
|-----------|--------|-------------|
| Health Check | ✅ | 2/2 |
| User Management | ✅ | 3/3 |
| Recommendations | ✅ | 3/3 |
| Interactions | ✅ | 2/2 |
| VR Tours | ✅ | 5/5 |
| Chatbot | ✅ | 3/3 |
| Analytics | ✅ | 4/4 |
| Destinations | ✅ | 1/1 |
| **TOTAL** | **✅** | **23/23** |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python api/vr_ai_flask_app_v1.py --port 5001
```

### CORS Errors
Ensure Flask-CORS is installed:
```bash
pip install flask-cors
```

### Connection Refused
- Check server is running: `curl http://localhost:5000/api/health`
- Verify port 5000 is accessible

### JSON Parsing Errors
Use proper Content-Type headers:
```bash
curl -H "Content-Type: application/json"
```

---

## 📈 Performance Testing

Load test the API:

```bash
# Install Apache Bench
apt-get install apache2-utils  # Linux
brew install httpd             # macOS

# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:5000/api/health
```

---

## 🔒 Security Testing

**Test CORS:**
```bash
curl -H "Origin: https://example.com" \
     -H "Access-Control-Request-Method: POST" \
     http://localhost:5000/api/users
```

**Test Error Handling:**
```bash
# Invalid JSON
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d 'invalid json'

# Missing endpoint
curl http://localhost:5000/api/nonexistent
```

---

## ✅ Acceptance Criteria

Your integration is **complete** when:

- [x] All 8 test phases pass
- [x] API responds to all endpoints within 200ms
- [x] No CORS errors in browser console
- [x] v1 and v2 can call API endpoints
- [x] Recommendations change based on user preferences
- [x] Chat responds with relevant answers
- [x] Analytics track visits correctly
- [x] VR tours can be created and published

---

## 📚 Next Steps

1. **Integrate with v1 website** - Add client code to v1/dashboard.html
2. **Integrate with v2 website** - Add client code to v2/dashboard.html
3. **Database Integration** - Replace in-memory storage with PostgreSQL
4. **Authentication** - Add JWT token support
5. **Deployment** - Deploy to production server
6. **Monitoring** - Set up logging and monitoring

---

## 📞 Support

For issues or questions:
1. Check the logs: `tail -f app.log`
2. Review VR_AI_INTEGRATION_GUIDE.md
3. Check test output for error messages
4. Verify all dependencies are installed

---

## License

MIT License - See LICENSE file in repository
