# How to Integrate VR & AI API with v1 and v2 Websites

## 📍 Where Should the API Be Located?

### **RECOMMENDED STRUCTURE** ✅

Keep the API in the `/api` folder (main level), **NOT** in v1 or v2:

```
trevo-ai-tourism-tools/
├── api/                          ← API serves BOTH v1 and v2
│   ├── vr_ai_integration.py
│   ├── vr_ai_flask_app_v1.py
│   └── vr_ai_flask_app_v2.py    (optional - for v2 specific endpoints)
├── v1/                          ← v1 website (only HTML/CSS/JS)
│   ├── index.html
│   ├── dashboard.html
│   └── vr_ai_client.js          ← Client code to call API
├── v2/                          ← v2 website (only HTML/CSS/JS)
│   ├── index.html
│   ├── dashboard.html
│   └── vr_ai_client.js          ← Client code to call API
└── requirements.txt
```

**Why?** 
- Single API serves both versions
- Easier maintenance
- Shared data and analytics
- No duplication
- Scalable architecture

---

## 🔌 Integration Steps for v1 Website

### Step 1: Add JavaScript Client to v1

Create or update `v1/vr_ai_client.js`:

```javascript
/**
 * VR and AI Client for v1 Tourism Website
 * Connects v1 website to backend API
 */

class VRTourismClient {
    constructor(apiUrl = 'http://localhost:5000/api') {
        this.apiUrl = apiUrl;
        this.userId = this.generateUserId();
        this.initialized = false;
    }

    /**
     * Generate unique user ID
     */
    generateUserId() {
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Initialize user session
     */
    async initializeUser(name = 'Visitor', preferences = {}) {
        try {
            const response = await fetch(`${this.apiUrl}/users`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: this.userId,
                    name: name,
                    preferences: {
                        interest_tags: preferences.tags || ['adventure', 'nature'],
                        difficulty_level: preferences.difficulty || 'intermediate',
                        max_price: preferences.maxPrice || 1000,
                        ...preferences
                    }
                })
            });
            
            const data = await response.json();
            if (data.success) {
                this.initialized = true;
                console.log('User initialized:', this.userId);
                return data;
            }
        } catch (error) {
            console.error('Error initializing user:', error);
        }
    }

    /**
     * Get personalized recommendations
     */
    async getRecommendations(limit = 5) {
        try {
            const response = await fetch(
                `${this.apiUrl}/recommendations/${this.userId}?limit=${limit}`
            );
            const data = await response.json();
            return data.recommendations || [];
        } catch (error) {
            console.error('Error getting recommendations:', error);
            return [];
        }
    }

    /**
     * Get all available destinations
     */
    async getDestinations() {
        try {
            const response = await fetch(`${this.apiUrl}/destinations`);
            const data = await response.json();
            return data.destinations || [];
        } catch (error) {
            console.error('Error getting destinations:', error);
            return [];
        }
    }

    /**
     * Track user interaction
     */
    async trackInteraction(destinationId, type = 'view', duration = 0) {
        try {
            const response = await fetch(
                `${this.apiUrl}/interactions/${this.userId}`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        destination_id: destinationId,
                        interaction_type: type,
                        duration_seconds: duration
                    })
                }
            );
            return await response.json();
        } catch (error) {
            console.error('Error tracking interaction:', error);
        }
    }

    /**
     * Chat with AI bot
     */
    async chat(query) {
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: this.userId,
                    query: query
                })
            });
            const data = await response.json();
            return data.response || 'No response';
        } catch (error) {
            console.error('Error in chat:', error);
            return 'Error communicating with AI';
        }
    }

    /**
     * Get chat history
     */
    async getChatHistory() {
        try {
            const response = await fetch(
                `${this.apiUrl}/chat/history/${this.userId}`
            );
            const data = await response.json();
            return data.history || [];
        } catch (error) {
            console.error('Error getting chat history:', error);
            return [];
        }
    }

    /**
     * Create VR tour
     */
    async createTour(destinationId, title, description, scenes = 10, duration = 20) {
        try {
            const response = await fetch(`${this.apiUrl}/tours`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    destination_id: destinationId,
                    title: title,
                    description: description,
                    scenes: scenes,
                    duration_minutes: duration
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error creating tour:', error);
        }
    }

    /**
     * Publish tour
     */
    async publishTour(tourId) {
        try {
            const response = await fetch(
                `${this.apiUrl}/tours/${tourId}/publish`,
                { method: 'PUT' }
            );
            return await response.json();
        } catch (error) {
            console.error('Error publishing tour:', error);
        }
    }

    /**
     * Record tour view
     */
    async recordTourView(tourId, sessionDuration = 0) {
        try {
            const response = await fetch(
                `${this.apiUrl}/tours/${tourId}/view`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: this.userId,
                        session_duration: sessionDuration
                    })
                }
            );
            return await response.json();
        } catch (error) {
            console.error('Error recording tour view:', error);
        }
    }

    /**
     * Rate tour
     */
    async rateTour(tourId, rating) {
        try {
            const response = await fetch(
                `${this.apiUrl}/tours/${tourId}/rate`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ rating: rating })
                }
            );
            return await response.json();
        } catch (error) {
            console.error('Error rating tour:', error);
        }
    }

    /**
     * Record destination visit (analytics)
     */
    async recordVisit(destinationId, durationMinutes = 0, rating = null) {
        try {
            const response = await fetch(`${this.apiUrl}/analytics/visits`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    destination_id: destinationId,
                    user_id: this.userId,
                    duration_minutes: durationMinutes,
                    rating: rating
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Error recording visit:', error);
        }
    }
}

// Global instance
const vrClient = new VRTourismClient();
```

### Step 2: Add Script Tag to v1/index.html

Add this in the `<head>` section of `v1/index.html`:

```html
<!-- VR and AI Integration -->
<script src="vr_ai_client.js"></script>
<script>
    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', async function() {
        await vrClient.initializeUser('v1 Visitor', {
            tags: ['adventure', 'cultural'],
            difficulty: 'intermediate',
            maxPrice: 500
        });
    });
</script>
```

### Step 3: Use in v1/dashboard.html

Example: Display recommendations in dashboard:

```html
<!-- Add this to v1/dashboard.html -->
<section id="recommendations">
    <h2>Recommended Destinations For You</h2>
    <div id="recommendations-list" class="destinations-grid">
        <!-- Will be filled by JavaScript -->
    </div>
</section>

<script>
    async function loadRecommendations() {
        const recommendations = await vrClient.getRecommendations(5);
        const container = document.getElementById('recommendations-list');
        
        recommendations.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'destination-card';
            card.innerHTML = `
                <h3>${rec.name}</h3>
                <p>${rec.location}</p>
                <div class="rating">⭐ ${rec.rating}</div>
                <div class="match">Match: ${rec.match_percentage}</div>
                <p class="price">$${rec.price}</p>
                <button onclick="selectDestination('${rec.destination_id}')">
                    View VR Tour
                </button>
            `;
            container.appendChild(card);
        });
    }

    // Load recommendations on page load
    document.addEventListener('DOMContentLoaded', loadRecommendations);

    // Handle destination selection
    async function selectDestination(destinationId) {
        await vrClient.trackInteraction(destinationId, 'click');
        console.log('Selected:', destinationId);
        // Navigate to VR viewer or open VR experience
    }
</script>
```

### Step 4: Add AI Chatbot to v1

Example: Chat widget in corner:

```html
<!-- Add to v1/index.html or v1/dashboard.html -->
<div id="chat-widget" style="position: fixed; bottom: 20px; right: 20px; width: 300px; border: 1px solid #ccc; border-radius: 8px; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 1000;">
    <div style="background: #007bff; color: white; padding: 10px; border-radius: 8px 8px 0 0; cursor: pointer;">
        <h4 style="margin: 0;">Tourism Assistant 🤖</h4>
    </div>
    
    <div id="chat-messages" style="height: 300px; overflow-y: auto; padding: 10px; border-bottom: 1px solid #eee;">
        <div style="color: #999; text-align: center; padding: 20px;">
            How can I help you today?
        </div>
    </div>
    
    <div style="padding: 10px; display: flex; gap: 5px;">
        <input type="text" id="chat-input" placeholder="Ask me anything..." 
               style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
        <button onclick="sendChatMessage()" style="padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Send</button>
    </div>
</div>

<script>
    async function sendChatMessage() {
        const input = document.getElementById('chat-input');
        const query = input.value.trim();
        
        if (!query) return;
        
        // Add user message to chat
        addChatMessage(query, 'user');
        input.value = '';
        
        // Get AI response
        const response = await vrClient.chat(query);
        addChatMessage(response, 'bot');
    }
    
    function addChatMessage(message, sender) {
        const messagesDiv = document.getElementById('chat-messages');
        const messageEl = document.createElement('div');
        messageEl.style.marginBottom = '10px';
        messageEl.style.padding = '8px';
        messageEl.style.borderRadius = '4px';
        
        if (sender === 'user') {
            messageEl.style.backgroundColor = '#e3f2fd';
            messageEl.style.marginLeft = '20px';
        } else {
            messageEl.style.backgroundColor = '#f5f5f5';
            messageEl.style.marginRight = '20px';
        }
        
        messageEl.textContent = message;
        messagesDiv.appendChild(messageEl);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    // Allow Enter key to send
    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendChatMessage();
    });
</script>
```

---

## 🔌 Integration Steps for v2 Website

The same `vr_ai_client.js` works for v2! Just follow the same steps:

### For v2/index.html:

```html
<!-- Add to v2/index.html -->
<script src="vr_ai_client.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', async function() {
        await vrClient.initializeUser('v2 Visitor', {
            tags: ['relaxation', 'beach'],
            difficulty: 'beginner',
            maxPrice: 300
        });
    });
</script>
```

### For v2/dashboard.html:

Same recommendations display code as v1, just customize styling for v2's design system.

---

## 🚀 Quick Setup Summary

### **Option A: Development (Recommended for Testing)**

```bash
# Terminal 1: Start API server
cd trevo-ai-tourism-tools
python api/vr_ai_flask_app_v1.py

# Terminal 2: Open v1 in browser
open v1/index.html  # or file:///path/to/v1/index.html

# Terminal 3: Open v2 in browser
open v2/index.html
```

**API URL for local testing:** `http://localhost:5000/api`

### **Option B: Production**

Update `vr_ai_client.js` with your production API URL:

```javascript
// Change from localhost to production
const vrClient = new VRTourismClient('https://yourdomain.com/api');
```

---

## ✅ Testing Checklist

- [ ] v1/index.html loads without errors
- [ ] v2/index.html loads without errors
- [ ] Console shows "User initialized" message
- [ ] Recommendations appear in dashboard
- [ ] Chat widget works
- [ ] Click on destination tracks interaction
- [ ] Rating a tour updates analytics

---

## 📊 Directory Structure After Integration

```
trevo-ai-tourism-tools/
├── api/
│   ├── __init__.py
│   ├── vr_ai_integration.py          ← Core classes
│   ├── vr_ai_flask_app_v1.py         ← Flask app
│   └── vr_ai_flask_app_v2.py         ← Optional: v2-specific
├── v1/
│   ├── index.html                    ← ✏️ ADD: <script src="vr_ai_client.js">
│   ├── dashboard.html                ← ✏️ ADD: Recommendations section
│   ├── vr_ai_client.js               ← ✏️ NEW: JavaScript client
│   ├── vr_ai_widget.css              ← Optional: Chat widget styling
│   └── ...
├── v2/
│   ├── index.html                    ← ✏️ ADD: <script src="vr_ai_client.js">
│   ├── dashboard.html                ← ✏️ ADD: Recommendations section
│   ├── vr_ai_client.js               ← ✏️ NEW: JavaScript client (same file)
│   └── ...
├── docs/
├── API_TESTING_GUIDE.md
├── VR_AI_INTEGRATION_GUIDE.md
├── requirements.txt
└── README.md
```

---

## 🔐 Important Notes

1. **CORS Configuration**: Already enabled in Flask app with `CORS(app)`
2. **API Endpoint**: Both v1 and v2 point to same API (`http://localhost:5000/api`)
3. **User Tracking**: Each session gets unique user ID (stored in `vrClient.userId`)
4. **Shared Data**: Analytics, recommendations, and chat history are shared across v1 and v2
5. **Database**: Currently uses in-memory storage; upgrade to PostgreSQL for production

---

## 🎯 What Gets Reflected on Websites

### On v1 Dashboard:
- ✅ Personalized destination recommendations
- ✅ AI chatbot widget
- ✅ Available VR tours with ratings
- ✅ User interaction tracking
- ✅ Trending destinations

### On v2 Dashboard:
- ✅ Same features as v1 (same API)
- ✅ Can have different UI styling
- ✅ Different user preferences per user (tracked separately)

---

## 📝 Next Steps

1. ✏️ Copy `vr_ai_client.js` to v1/ and v2/
2. ✏️ Update v1/index.html with script tag
3. ✏️ Update v2/index.html with script tag
4. ✏️ Add recommendations section to v1/dashboard.html
5. ✏️ Add recommendations section to v2/dashboard.html
6. ✏️ Add chat widget to both dashboards
7. 🧪 Test with API running locally
8. 🚀 Deploy API and update URLs for production

---

For detailed testing instructions, see: **API_TESTING_GUIDE.md**
