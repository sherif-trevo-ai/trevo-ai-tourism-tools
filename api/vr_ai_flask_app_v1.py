"""
VR and AI Flask API for v1 Dashboard
Integrates with v1/dashboard.html and v1/index.html
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime
from api.vr_ai_integration import (
    initialize_tourism_ai_system,
    Destination,
    UserProfile
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize VR and AI system
tourism_system = initialize_tourism_ai_system()

# Sample destinations for testing
SAMPLE_DESTINATIONS = [
    Destination(
        id="dest_001",
        name="Ancient Temple Complex",
        description="Explore a centuries-old temple through VR",
        location="Southeast Asia",
        rating=4.8,
        vr_url="https://vr.example.com/temple",
        difficulty_level="intermediate",
        duration_minutes=20,
        price=29.99,
        tags=["cultural", "historical", "spiritual"]
    ),
    Destination(
        id="dest_002",
        name="Mountain Adventure Trail",
        description="Hike through scenic mountain landscapes",
        location="Swiss Alps",
        rating=4.6,
        vr_url="https://vr.example.com/mountain",
        difficulty_level="advanced",
        duration_minutes=30,
        price=39.99,
        tags=["adventure", "nature", "hiking"]
    ),
    Destination(
        id="dest_003",
        name="Tropical Beach Paradise",
        description="Relax on pristine tropical beaches",
        location="Caribbean",
        rating=4.9,
        vr_url="https://vr.example.com/beach",
        difficulty_level="beginner",
        duration_minutes=15,
        price=24.99,
        tags=["relaxation", "nature", "beach"]
    ),
    Destination(
        id="dest_004",
        name="Historic City Tour",
        description="Discover historic landmarks and architecture",
        location="Europe",
        rating=4.7,
        vr_url="https://vr.example.com/city",
        difficulty_level="beginner",
        duration_minutes=25,
        price=19.99,
        tags=["cultural", "historical", "architecture"]
    ),
    Destination(
        id="dest_005",
        name="Desert Safari Experience",
        description="Adventure through sand dunes and desert landscapes",
        location="Middle East",
        rating=4.5,
        vr_url="https://vr.example.com/desert",
        difficulty_level="intermediate",
        duration_minutes=35,
        price=44.99,
        tags=["adventure", "nature", "exotic"]
    )
]


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "v1.0"
    }), 200


@app.route('/api/status', methods=['GET'])
def system_status():
    """Get system status"""
    return jsonify({
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "recommendation_engine": "active",
            "vr_tour_manager": "active",
            "chatbot": "active",
            "analytics": "active",
            "experience_generator": "active"
        },
        "sample_destinations": len(SAMPLE_DESTINATIONS)
    }), 200


# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user profile"""
    try:
        data = request.get_json()
        
        user_profile = UserProfile(
            user_id=data.get('user_id'),
            name=data.get('name', 'Guest'),
            preferences=data.get('preferences', {}),
            visit_history=[],
            favorite_destinations=[],
            interaction_history=[]
        )
        
        success = tourism_system['recommendation_engine'].add_user_profile(user_profile)
        
        if success:
            return jsonify({
                "success": True,
                "message": "User profile created successfully",
                "user_id": user_profile.user_id,
                "timestamp": datetime.now().isoformat()
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Failed to create user profile"
            }), 400
            
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# RECOMMENDATIONS ENDPOINTS
# ============================================================================

@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get personalized recommendations for a user"""
    try:
        limit = request.args.get('limit', 5, type=int)
        
        recommendations = tourism_system['recommendation_engine'].get_personalized_recommendations(
            user_id,
            SAMPLE_DESTINATIONS,
            limit=limit
        )
        
        return jsonify({
            "user_id": user_id,
            "count": len(recommendations),
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/interactions/<user_id>', methods=['POST'])
def track_interaction(user_id):
    """Track user interaction with a destination"""
    try:
        data = request.get_json()
        
        success = tourism_system['recommendation_engine'].track_user_interaction(
            user_id=user_id,
            destination_id=data.get('destination_id'),
            interaction_type=data.get('interaction_type', 'view'),
            duration_seconds=data.get('duration_seconds', 0)
        )
        
        return jsonify({
            "success": success,
            "user_id": user_id,
            "interaction_tracked": success,
            "timestamp": datetime.now().isoformat()
        }), 200 if success else 400
        
    except Exception as e:
        logger.error(f"Error tracking interaction: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# VR TOURS ENDPOINTS
# ============================================================================

@app.route('/api/tours', methods=['POST'])
def create_tour():
    """Create a new VR tour"""
    try:
        data = request.get_json()
        
        tour = tourism_system['vr_tour_manager'].create_vr_tour(
            destination_id=data.get('destination_id'),
            title=data.get('title'),
            description=data.get('description'),
            scenes=data.get('scenes', 10),
            duration_minutes=data.get('duration_minutes', 20)
        )
        
        if tour:
            return jsonify({
                "success": True,
                "tour_id": tour.id,
                "destination_id": tour.destination_id,
                "title": tour.title,
                "is_published": tour.is_published,
                "timestamp": datetime.now().isoformat()
            }), 201
        else:
            return jsonify({"error": "Failed to create tour"}), 400
            
    except Exception as e:
        logger.error(f"Error creating tour: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/tours/<tour_id>/publish', methods=['PUT'])
def publish_tour(tour_id):
    """Publish a VR tour"""
    try:
        success = tourism_system['vr_tour_manager'].publish_tour(tour_id)
        
        return jsonify({
            "success": success,
            "tour_id": tour_id,
            "published": success,
            "timestamp": datetime.now().isoformat()
        }), 200 if success else 404
        
    except Exception as e:
        logger.error(f"Error publishing tour: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/tours/<tour_id>/view', methods=['POST'])
def record_tour_view(tour_id):
    """Record a user viewing a VR tour"""
    try:
        data = request.get_json()
        
        success = tourism_system['vr_tour_manager'].record_tour_view(
            tour_id=tour_id,
            user_id=data.get('user_id'),
            session_duration=data.get('session_duration', 0)
        )
        
        return jsonify({
            "success": success,
            "tour_id": tour_id,
            "timestamp": datetime.now().isoformat()
        }), 200 if success else 404
        
    except Exception as e:
        logger.error(f"Error recording tour view: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/tours/<tour_id>/rate', methods=['POST'])
def rate_tour(tour_id):
    """Rate a VR tour"""
    try:
        data = request.get_json()
        rating = data.get('rating', 0)
        
        success = tourism_system['vr_tour_manager'].rate_tour(tour_id, rating)
        
        return jsonify({
            "success": success,
            "tour_id": tour_id,
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        }), 200 if success else 400
        
    except Exception as e:
        logger.error(f"Error rating tour: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/tours/<tour_id>/analytics', methods=['GET'])
def get_tour_analytics(tour_id):
    """Get analytics for a VR tour"""
    try:
        analytics = tourism_system['vr_tour_manager'].get_tour_analytics(tour_id)
        
        if analytics:
            return jsonify(analytics), 200
        else:
            return jsonify({"error": "Tour not found"}), 404
            
    except Exception as e:
        logger.error(f"Error getting tour analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# CHATBOT ENDPOINTS
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process user query with AI chatbot"""
    try:
        data = request.get_json()
        
        response = tourism_system['chatbot'].process_query(
            user_id=data.get('user_id'),
            query=data.get('query')
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat/history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get conversation history for a user"""
    try:
        history = tourism_system['chatbot'].get_conversation_history(user_id)
        
        return jsonify({
            "user_id": user_id,
            "message_count": len(history),
            "history": history,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.route('/api/analytics/visits', methods=['POST'])
def record_visit():
    """Record a destination visit"""
    try:
        data = request.get_json()
        
        success = tourism_system['analytics'].record_destination_visit(
            destination_id=data.get('destination_id'),
            user_id=data.get('user_id'),
            duration_minutes=data.get('duration_minutes', 0),
            rating=data.get('rating')
        )
        
        return jsonify({
            "success": success,
            "timestamp": datetime.now().isoformat()
        }), 200 if success else 400
        
    except Exception as e:
        logger.error(f"Error recording visit: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics/destination/<destination_id>', methods=['GET'])
def get_destination_stats(destination_id):
    """Get statistics for a destination"""
    try:
        stats = tourism_system['analytics'].get_destination_statistics(destination_id)
        
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No data for destination"}), 404
            
    except Exception as e:
        logger.error(f"Error getting destination stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics/trending', methods=['GET'])
def get_trending():
    """Get trending destinations"""
    try:
        days = request.args.get('days', 30, type=int)
        limit = request.args.get('limit', 5, type=int)
        
        trending = tourism_system['analytics'].get_trending_destinations(
            days=days,
            limit=limit
        )
        
        return jsonify({
            "trending_destinations": trending,
            "period_days": days,
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting trending: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# EXPERIENCE ENDPOINTS
# ============================================================================

@app.route('/api/experiences', methods=['POST'])
def create_experience():
    """Create a custom VR experience"""
    try:
        data = request.get_json()
        
        experience = tourism_system['experience_generator'].customize_experience(
            user_id=data.get('user_id'),
            template_id=data.get('template_id'),
            customizations=data.get('customizations', {})
        )
        
        if experience:
            return jsonify({
                "success": True,
                "experience_id": experience['experience_id'],
                "user_id": experience['user_id'],
                "template_id": experience['template_id'],
                "timestamp": datetime.now().isoformat()
            }), 201
        else:
            return jsonify({"error": "Failed to create experience"}), 400
            
    except Exception as e:
        logger.error(f"Error creating experience: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/experiences/<user_id>', methods=['GET'])
def get_user_experiences(user_id):
    """Get all experiences for a user"""
    try:
        experiences = tourism_system['experience_generator'].get_user_experience(user_id)
        
        return jsonify({
            "user_id": user_id,
            "experience_count": len(experiences),
            "experiences": experiences,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting experiences: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# DESTINATIONS ENDPOINT
# ============================================================================

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Get all available destinations"""
    try:
        destinations = [
            {
                "id": d.id,
                "name": d.name,
                "location": d.location,
                "description": d.description,
                "rating": d.rating,
                "price": d.price,
                "vr_available": d.vr_url is not None,
                "difficulty_level": d.difficulty_level,
                "duration_minutes": d.duration_minutes,
                "tags": d.tags
            }
            for d in SAMPLE_DESTINATIONS
        ]
        
        return jsonify({
            "count": len(destinations),
            "destinations": destinations,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting destinations: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("Starting VR and AI Tourism API (v1)...")
    logger.info("Available endpoints:")
    logger.info("  POST   /api/users")
    logger.info("  GET    /api/recommendations/<user_id>")
    logger.info("  POST   /api/chat")
    logger.info("  POST   /api/tours")
    logger.info("  GET    /api/destinations")
    logger.info("  GET    /api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
