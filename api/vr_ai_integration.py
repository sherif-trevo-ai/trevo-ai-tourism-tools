"""
VR and AI Integration Module for Tourism Tools
This module provides AI-powered recommendations and VR experience management
for tourism businesses using machine learning and virtual reality technologies.

Features:
- AI-powered destination recommendations
- Virtual tour management
- Visitor experience personalization
- AI chatbot for customer support
- Predictive analytics for tourism trends
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Destination:
    """Data class for VR destination information"""
    id: str
    name: str
    description: str
    location: str
    rating: float
    vr_url: Optional[str] = None
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced
    duration_minutes: int = 15
    price: float = 0.0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class VRTour:
    """Data class for VR tour information"""
    id: str
    destination_id: str
    title: str
    description: str
    scenes: int
    duration_minutes: int
    created_date: str
    last_updated: str
    is_published: bool = False
    view_count: int = 0


@dataclass
class UserProfile:
    """Data class for user AI profile"""
    user_id: str
    name: str
    preferences: Dict
    visit_history: List[str]
    favorite_destinations: List[str]
    interaction_history: List[Dict]


class AIRecommendationEngine:
    """
    AI-powered recommendation engine for personalized tourism suggestions
    """
    
    def __init__(self):
        self.recommendations_cache = {}
        self.user_profiles = {}
        logger.info("AIRecommendationEngine initialized")
    
    def add_user_profile(self, profile: UserProfile) -> bool:
        """Register a new user profile"""
        try:
            self.user_profiles[profile.user_id] = profile
            logger.info(f"User profile created: {profile.user_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding user profile: {str(e)}")
            return False
    
    def get_personalized_recommendations(
        self, 
        user_id: str, 
        available_destinations: List[Destination],
        limit: int = 5
    ) -> List[Dict]:
        """
        Generate personalized destination recommendations based on user preferences
        and interaction history
        
        Args:
            user_id: The user's unique identifier
            available_destinations: List of available tourism destinations
            limit: Maximum number of recommendations to return
            
        Returns:
            List of personalized destination recommendations with scores
        """
        if user_id not in self.user_profiles:
            return self._get_default_recommendations(available_destinations, limit)
        
        user_profile = self.user_profiles[user_id]
        recommendations = []
        
        for destination in available_destinations:
            # Skip already visited destinations
            if destination.id in user_profile.visit_history:
                continue
            
            score = self._calculate_recommendation_score(
                destination, 
                user_profile
            )
            
            recommendations.append({
                "destination_id": destination.id,
                "name": destination.name,
                "location": destination.location,
                "description": destination.description,
                "rating": destination.rating,
                "recommendation_score": round(score, 2),
                "match_percentage": f"{round(score * 100, 1)}%",
                "vr_available": destination.vr_url is not None,
                "price": destination.price
            })
        
        # Sort by recommendation score and return top results
        recommendations.sort(
            key=lambda x: x['recommendation_score'], 
            reverse=True
        )
        
        cache_key = f"{user_id}_recommendations"
        self.recommendations_cache[cache_key] = recommendations
        
        return recommendations[:limit]
    
    def _calculate_recommendation_score(
        self, 
        destination: Destination, 
        user_profile: UserProfile
    ) -> float:
        """
        Calculate recommendation score using AI algorithm
        Factors: user preferences, destination rating, tags match, etc.
        """
        base_score = destination.rating / 5.0  # Normalize rating
        
        # Tag matching bonus
        tag_match_bonus = 0.0
        user_tags = user_profile.preferences.get('interest_tags', [])
        matching_tags = set(destination.tags) & set(user_tags)
        if matching_tags:
            tag_match_bonus = len(matching_tags) / len(user_tags) * 0.3
        
        # Difficulty preference
        difficulty_bonus = 0.0
        preferred_difficulty = user_profile.preferences.get('difficulty_level', 'intermediate')
        if destination.difficulty_level == preferred_difficulty:
            difficulty_bonus = 0.2
        
        # Price preference
        price_bonus = 0.0
        max_price = user_profile.preferences.get('max_price', float('inf'))
        if destination.price <= max_price:
            price_bonus = 0.1
        
        # Calculate final score (0-1)
        final_score = min(1.0, base_score + tag_match_bonus + difficulty_bonus + price_bonus)
        
        return final_score
    
    def _get_default_recommendations(
        self, 
        destinations: List[Destination],
        limit: int
    ) -> List[Dict]:
        """Get default recommendations based on rating"""
        sorted_destinations = sorted(
            destinations, 
            key=lambda x: x.rating, 
            reverse=True
        )
        
        return [
            {
                "destination_id": d.id,
                "name": d.name,
                "location": d.location,
                "description": d.description,
                "rating": d.rating,
                "recommendation_score": d.rating / 5.0,
                "match_percentage": f"{round((d.rating / 5.0) * 100, 1)}%",
                "vr_available": d.vr_url is not None,
                "price": d.price
            }
            for d in sorted_destinations[:limit]
        ]
    
    def track_user_interaction(
        self, 
        user_id: str, 
        destination_id: str, 
        interaction_type: str,
        duration_seconds: int = 0
    ) -> bool:
        """
        Track user interactions to improve recommendations
        interaction_type: 'view', 'click', 'bookmark', 'purchase'
        """
        if user_id not in self.user_profiles:
            return False
        
        try:
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "destination_id": destination_id,
                "type": interaction_type,
                "duration_seconds": duration_seconds
            }
            
            self.user_profiles[user_id].interaction_history.append(interaction)
            logger.info(f"Interaction tracked: {user_id} - {interaction_type}")
            return True
        except Exception as e:
            logger.error(f"Error tracking interaction: {str(e)}")
            return False


class VRTourManager:
    """
    Manages VR tour creation, storage, and delivery
    """
    
    def __init__(self):
        self.tours = {}
        self.tour_analytics = {}
        logger.info("VRTourManager initialized")
    
    def create_vr_tour(
        self,
        destination_id: str,
        title: str,
        description: str,
        scenes: int,
        duration_minutes: int
    ) -> Optional[VRTour]:
        """Create a new VR tour"""
        try:
            tour_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            tour = VRTour(
                id=tour_id,
                destination_id=destination_id,
                title=title,
                description=description,
                scenes=scenes,
                duration_minutes=duration_minutes,
                created_date=now,
                last_updated=now,
                is_published=False
            )
            
            self.tours[tour_id] = tour
            self.tour_analytics[tour_id] = {
                "created_date": now,
                "view_count": 0,
                "avg_session_duration": 0,
                "completion_rate": 0.0,
                "user_ratings": []
            }
            
            logger.info(f"VR tour created: {tour_id}")
            return tour
        except Exception as e:
            logger.error(f"Error creating VR tour: {str(e)}")
            return None
    
    def publish_tour(self, tour_id: str) -> bool:
        """Publish a VR tour to make it available to users"""
        if tour_id not in self.tours:
            logger.error(f"Tour not found: {tour_id}")
            return False
        
        self.tours[tour_id].is_published = True
        self.tours[tour_id].last_updated = datetime.now().isoformat()
        logger.info(f"Tour published: {tour_id}")
        return True
    
    def record_tour_view(self, tour_id: str, user_id: str, session_duration: int) -> bool:
        """Record when a user views a VR tour"""
        if tour_id not in self.tours:
            return False
        
        try:
            self.tours[tour_id].view_count += 1
            analytics = self.tour_analytics[tour_id]
            analytics["view_count"] += 1
            
            # Update average session duration
            current_avg = analytics["avg_session_duration"]
            view_count = analytics["view_count"]
            analytics["avg_session_duration"] = (
                (current_avg * (view_count - 1) + session_duration) / view_count
            )
            
            logger.info(f"Tour view recorded: {tour_id} by {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error recording tour view: {str(e)}")
            return False
    
    def get_tour_analytics(self, tour_id: str) -> Optional[Dict]:
        """Get analytics for a specific VR tour"""
        if tour_id not in self.tour_analytics:
            return None
        
        return {
            "tour_id": tour_id,
            "tour_title": self.tours[tour_id].title,
            **self.tour_analytics[tour_id],
            "avg_rating": (
                sum(self.tour_analytics[tour_id]["user_ratings"]) / 
                len(self.tour_analytics[tour_id]["user_ratings"])
                if self.tour_analytics[tour_id]["user_ratings"] else 0
            )
        }
    
    def rate_tour(self, tour_id: str, rating: float) -> bool:
        """Allow users to rate VR tours"""
        if tour_id not in self.tour_analytics or not (1 <= rating <= 5):
            return False
        
        self.tour_analytics[tour_id]["user_ratings"].append(rating)
        logger.info(f"Tour rated: {tour_id} - Rating: {rating}")
        return True


class AIChatbot:
    """
    AI-powered chatbot for customer support and tourism information
    """
    
    def __init__(self):
        self.conversation_history = {}
        self.knowledge_base = self._initialize_knowledge_base()
        logger.info("AIChatbot initialized")
    
    def _initialize_knowledge_base(self) -> Dict[str, List[str]]:
        """Initialize chatbot knowledge base with common tourism questions"""
        return {
            "vr_tours": [
                "VR tours are immersive virtual reality experiences of destinations",
                "You can access VR tours through our website",
                "VR tours are available on desktop and VR headsets"
            ],
            "booking": [
                "You can book tours through our online platform",
                "We accept multiple payment methods",
                "Cancellations are allowed up to 24 hours before tour"
            ],
            "destinations": [
                "We offer VR tours of popular tourism destinations",
                "Each destination has unique experiences",
                "Check our destination guide for more information"
            ],
            "technical_support": [
                "Ensure your device meets VR requirements",
                "Update your browser for best compatibility",
                "Contact support if you experience issues"
            ]
        }
    
    def process_query(self, user_id: str, query: str) -> Dict:
        """
        Process user query and generate response
        Uses keyword matching to find relevant answers
        """
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Store conversation
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_query": query,
            "response": ""
        }
        
        # Simple keyword-based response matching
        response = self._generate_response(query)
        conversation_entry["response"] = response
        
        self.conversation_history[user_id].append(conversation_entry)
        
        logger.info(f"Query processed for user: {user_id}")
        
        return {
            "user_id": user_id,
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85
        }
    
    def _generate_response(self, query: str) -> str:
        """Generate response based on query keywords"""
        query_lower = query.lower()
        
        # Check against knowledge base
        for category, responses in self.knowledge_base.items():
            if any(keyword in query_lower for keyword in category.split('_')):
                return responses[0]
        
        # Default response
        return (
            "Thank you for your question. "
            "Please visit our FAQ section or contact our support team "
            "for more detailed information."
        )
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Retrieve conversation history for a user"""
        return self.conversation_history.get(user_id, [])


class TourismAnalytics:
    """
    Analytics engine for tourism data and trend prediction
    """
    
    def __init__(self):
        self.user_interactions = []
        self.destination_visits = {}
        logger.info("TourismAnalytics initialized")
    
    def record_destination_visit(
        self, 
        destination_id: str, 
        user_id: str,
        duration_minutes: int,
        rating: Optional[float] = None
    ) -> bool:
        """Record a destination visit"""
        try:
            visit_record = {
                "timestamp": datetime.now().isoformat(),
                "destination_id": destination_id,
                "user_id": user_id,
                "duration_minutes": duration_minutes,
                "rating": rating
            }
            
            self.user_interactions.append(visit_record)
            
            if destination_id not in self.destination_visits:
                self.destination_visits[destination_id] = []
            
            self.destination_visits[destination_id].append(visit_record)
            logger.info(f"Visit recorded: {destination_id}")
            return True
        except Exception as e:
            logger.error(f"Error recording visit: {str(e)}")
            return False
    
    def get_destination_statistics(self, destination_id: str) -> Optional[Dict]:
        """Get statistics for a destination"""
        if destination_id not in self.destination_visits:
            return None
        
        visits = self.destination_visits[destination_id]
        ratings = [v["rating"] for v in visits if v["rating"] is not None]
        durations = [v["duration_minutes"] for v in visits]
        
        return {
            "destination_id": destination_id,
            "total_visits": len(visits),
            "average_rating": sum(ratings) / len(ratings) if ratings else 0,
            "average_duration_minutes": sum(durations) / len(durations) if durations else 0,
            "unique_users": len(set(v["user_id"] for v in visits))
        }
    
    def get_trending_destinations(self, days: int = 30, limit: int = 5) -> List[Dict]:
        """Get trending destinations based on recent visits"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_visits = [
            v for v in self.user_interactions
            if datetime.fromisoformat(v["timestamp"]) > cutoff_date
        ]
        
        destination_counts = {}
        for visit in recent_visits:
            dest_id = visit["destination_id"]
            destination_counts[dest_id] = destination_counts.get(dest_id, 0) + 1
        
        trending = sorted(
            destination_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "destination_id": dest_id,
                "recent_visits": count,
                "trend_rank": idx + 1
            }
            for idx, (dest_id, count) in enumerate(trending[:limit])
        ]


class VRExperienceGenerator:
    """
    Generates and customizes VR experiences based on user preferences
    """
    
    def __init__(self):
        self.experience_templates = {}
        self.user_customizations = {}
        logger.info("VRExperienceGenerator initialized")
    
    def create_experience_template(
        self,
        template_id: str,
        name: str,
        description: str,
        difficulty: str,
        environment_type: str
    ) -> Dict:
        """Create a VR experience template"""
        template = {
            "template_id": template_id,
            "name": name,
            "description": description,
            "difficulty": difficulty,
            "environment_type": environment_type,
            "created_date": datetime.now().isoformat(),
            "customizable_elements": []
        }
        
        self.experience_templates[template_id] = template
        logger.info(f"Experience template created: {template_id}")
        return template
    
    def customize_experience(
        self,
        user_id: str,
        template_id: str,
        customizations: Dict
    ) -> Optional[Dict]:
        """Customize a VR experience for a user"""
        if template_id not in self.experience_templates:
            return None
        
        experience_id = str(uuid.uuid4())
        
        custom_experience = {
            "experience_id": experience_id,
            "user_id": user_id,
            "template_id": template_id,
            "customizations": customizations,
            "created_date": datetime.now().isoformat(),
            "is_active": True
        }
        
        self.user_customizations[experience_id] = custom_experience
        logger.info(f"Experience customized: {experience_id} for user: {user_id}")
        return custom_experience
    
    def get_user_experience(self, user_id: str) -> List[Dict]:
        """Get all customized experiences for a user"""
        return [
            exp for exp in self.user_customizations.values()
            if exp["user_id"] == user_id and exp["is_active"]
        ]


# Example usage and initialization function
def initialize_tourism_ai_system() -> Dict:
    """
    Initialize the complete VR and AI tourism system
    Returns: Dictionary containing all initialized components
    """
    return {
        "recommendation_engine": AIRecommendationEngine(),
        "vr_tour_manager": VRTourManager(),
        "chatbot": AIChatbot(),
        "analytics": TourismAnalytics(),
        "experience_generator": VRExperienceGenerator()
    }


if __name__ == "__main__":
    # Example initialization
    print("Initializing VR and AI Tourism System...")
    system = initialize_tourism_ai_system()
    
    # Example: Create a user profile
    user_profile = UserProfile(
        user_id="user_001",
        name="John Doe",
        preferences={
            "interest_tags": ["adventure", "nature", "cultural"],
            "difficulty_level": "intermediate",
            "max_price": 500.0
        },
        visit_history=[],
        favorite_destinations=[],
        interaction_history=[]
    )
    
    system["recommendation_engine"].add_user_profile(user_profile)
    
    # Create sample destinations
    destinations = [
        Destination(
            id="dest_001",
            name="Ancient Temple Complex",
            description="Explore a centuries-old temple through VR",
            location="Southeast Asia",
            rating=4.8,
            vr_url="https://vr.example.com/temple",
            tags=["cultural", "historical"],
            price=29.99
        ),
        Destination(
            id="dest_002",
            name="Mountain Adventure Trail",
            description="Hike through scenic mountain landscapes",
            location="Swiss Alps",
            rating=4.6,
            vr_url="https://vr.example.com/mountain",
            tags=["adventure", "nature"],
            price=39.99
        )
    ]
    
    # Get recommendations
    recommendations = system["recommendation_engine"].get_personalized_recommendations(
        "user_001",
        destinations,
        limit=5
    )
    
    print("\nPersonalized Recommendations:")
    for rec in recommendations:
        print(f"  - {rec['name']}: {rec['recommendation_score']} match")
    
    print("\nVR and AI Tourism System initialized successfully!")
