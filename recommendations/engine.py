"""
Finovate StreamX AI - Netflix-style AI Recommendations Engine
Personalized content recommendations based on user behavior
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import random


@dataclass
class UserPreference:
    """User viewing preferences"""
    favorite_categories: List[str] = field(default_factory=list)
    favorite_languages: List[str] = field(default_factory=list)
    favorite_countries: List[str] = field(default_factory=list)
    preferred_quality: str = "HD"
    watch_time_peak: str = "evening"  # morning, afternoon, evening, night
    average_session_duration: float = 60.0  # minutes


@dataclass
class ContentItem:
    """Content item for recommendation"""
    id: str
    name: str
    category: str
    subcategory: Optional[str] = None
    language: str = "en"
    country: str = "US"
    quality: str = "HD"
    popularity_score: float = 0.5
    rating: float = 0.0
    tags: List[str] = field(default_factory=list)
    release_date: Optional[datetime] = None
    duration: Optional[float] = None  # minutes


@dataclass
class WatchHistory:
    """User watch history entry"""
    content_id: str
    watched_at: datetime
    completion_percentage: float
    duration_watched: float
    rating_given: Optional[float] = None
    device_type: str = "desktop"


class AIRecommendationEngine:
    """
    Netflix-style AI Recommendation Engine
    
    Features:
    - Collaborative filtering
    - Content-based filtering
    - Context-aware recommendations
    - Mood-based suggestions
    - Time-based personalization
    """
    
    def __init__(self):
        self.user_preferences: Dict[str, UserPreference] = {}
        self.watch_history: Dict[str, List[WatchHistory]] = {}
        self.content_library: List[ContentItem] = []
        self.user_sessions: Dict[str, List[Dict]] = {}
        
    async def initialize(self):
        """Initialize recommendation engine"""
        print("🧠 Initializing AI Recommendation Engine...")
        await self._load_content_library()
        print(f"✓ Loaded {len(self.content_library)} content items")
        
    async def _load_content_library(self):
        """Load content library (mock data - will integrate with IPTV/Database)"""
        categories = ["Sports", "Movies", "Series", "News", "Documentary", "Kids", "Music"]
        countries = ["US", "UK", "EG", "SA", "AE", "FR", "DE", "IT", "ES"]
        languages = ["en", "ar", "fr", "de", "es", "it"]
        
        for i in range(100):
            category = random.choice(categories)
            item = ContentItem(
                id=f"content_{i}",
                name=f"{category} Channel {i+1}",
                category=category,
                language=random.choice(languages),
                country=random.choice(countries),
                quality=random.choice(["SD", "HD", "FHD", "4K"]),
                popularity_score=random.uniform(0.1, 1.0),
                rating=random.uniform(3.0, 5.0),
                tags=[category.lower(), f"channel_{i+1}"],
                release_date=datetime.now() - timedelta(days=random.randint(0, 365)),
                duration=random.uniform(30, 180) if category in ["Movies", "Series"] else None
            )
            self.content_library.append(item)
    
    def add_watch_history(self, user_id: str, history: WatchHistory):
        """Add watch history for user"""
        if user_id not in self.watch_history:
            self.watch_history[user_id] = []
        self.watch_history[user_id].append(history)
        
        # Update user preferences
        self._update_user_preferences(user_id, history)
    
    def _update_user_preferences(self, user_id: str, history: WatchHistory):
        """Update user preferences based on watch history"""
        # Find content item
        content = next((c for c in self.content_library if c.id == history.content_id), None)
        if not content:
            return
        
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreference()
        
        prefs = self.user_preferences[user_id]
        
        # Update favorite categories
        if history.completion_percentage > 70:
            if content.category not in prefs.favorite_categories:
                prefs.favorite_categories.append(content.category)
        
        # Update favorite languages
        if content.language not in prefs.favorite_languages:
            if len(prefs.favorite_languages) < 3:
                prefs.favorite_languages.append(content.language)
        
        # Update favorite countries
        if content.country not in prefs.favorite_countries:
            if len(prefs.favorite_countries) < 3:
                prefs.favorite_countries.append(content.country)
    
    async def get_recommendations(
        self,
        user_id: str,
        limit: int = 20,
        context: Optional[Dict[str, Any]] = None
    ) -> List[ContentItem]:
        """
        Get personalized recommendations for user
        
        Args:
            user_id: User identifier
            limit: Number of recommendations
            context: Additional context (time, mood, device, etc.)
        
        Returns:
            List of recommended content items
        """
        if user_id not in self.user_preferences:
            # Cold start - return popular content
            return self._get_popular_content(limit)
        
        prefs = self.user_preferences[user_id]
        history = self.watch_history.get(user_id, [])
        
        # Calculate scores for all content
        scored_content = []
        for content in self.content_library:
            score = self._calculate_content_score(user_id, content, prefs, history, context)
            scored_content.append((content, score))
        
        # Sort by score and return top N
        scored_content.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored_content[:limit]]
    
    def _calculate_content_score(
        self,
        user_id: str,
        content: ContentItem,
        prefs: UserPreference,
        history: List[WatchHistory],
        context: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate recommendation score for content"""
        score = 0.0
        
        # Category preference (weight: 0.3)
        if content.category in prefs.favorite_categories:
            score += 0.3
        
        # Language preference (weight: 0.15)
        if content.language in prefs.favorite_languages:
            score += 0.15
        
        # Country preference (weight: 0.15)
        if content.country in prefs.favorite_countries:
            score += 0.15
        
        # Quality match (weight: 0.1)
        if content.quality == prefs.preferred_quality or \
           (content.quality == "4K" and prefs.preferred_quality in ["HD", "FHD"]):
            score += 0.1
        
        # Popularity (weight: 0.1)
        score += content.popularity_score * 0.1
        
        # Rating (weight: 0.1)
        score += (content.rating / 5.0) * 0.1
        
        # Not recently watched bonus (weight: 0.1)
        recently_watched = any(
            h.content_id == content.id and 
            (datetime.now() - h.watched_at).days < 7
            for h in history
        )
        if not recently_watched:
            score += 0.1
        
        # Context-aware adjustments
        if context:
            score += self._apply_context_boost(content, context)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _apply_context_boost(self, content: ContentItem, context: Dict[str, Any]) -> float:
        """Apply context-based score boosts"""
        boost = 0.0
        
        # Time of day
        hour = datetime.now().hour
        time_of_day = "night"
        if 6 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 22:
            time_of_day = "evening"
        
        if context.get("time_of_day") == time_of_day:
            boost += 0.05
        
        # Mood-based (if provided)
        mood = context.get("mood")
        if mood == "relaxed" and content.category in ["Documentary", "Music"]:
            boost += 0.1
        elif mood == "excited" and content.category == "Sports":
            boost += 0.1
        elif mood == "entertained" and content.category in ["Movies", "Series"]:
            boost += 0.1
        
        # Weekend vs Weekday
        is_weekend = datetime.now().weekday() >= 5
        if context.get("is_weekend") == is_weekend:
            boost += 0.03
        
        return boost
    
    def _get_popular_content(self, limit: int) -> List[ContentItem]:
        """Get popular content for cold start"""
        sorted_content = sorted(
            self.content_library,
            key=lambda x: (x.popularity_score, x.rating),
            reverse=True
        )
        return sorted_content[:limit]
    
    async def get_mood_recommendations(
        self,
        user_id: str,
        mood: str,
        limit: int = 10
    ) -> List[ContentItem]:
        """Get recommendations based on current mood"""
        context = {"mood": mood}
        return await self.get_recommendations(user_id, limit, context)
    
    async def get_continue_watching(self, user_id: str) -> List[Dict[str, Any]]:
        """Get content that user hasn't finished watching"""
        history = self.watch_history.get(user_id, [])
        
        continue_watching = []
        for h in history:
            if 10 < h.completion_percentage < 90:
                content = next((c for c in self.content_library if c.id == h.content_id), None)
                if content:
                    continue_watching.append({
                        "content": content,
                        "progress": h.completion_percentage,
                        "last_watched": h.watched_at,
                        "remaining_time": h.duration_watched * (100 - h.completion_percentage) / 100
                    })
        
        # Sort by most recently watched
        continue_watching.sort(key=lambda x: x["last_watched"], reverse=True)
        return continue_watching[:10]
    
    async def get_similar_content(
        self,
        user_id: str,
        content_id: str,
        limit: int = 10
    ) -> List[ContentItem]:
        """Get content similar to specified item"""
        content = next((c for c in self.content_library if c.id == content_id), None)
        if not content:
            return []
        
        similar = []
        for item in self.content_library:
            if item.id == content_id:
                continue
            
            similarity_score = 0.0
            
            # Same category
            if item.category == content.category:
                similarity_score += 0.4
            
            # Same language
            if item.language == content.language:
                similarity_score += 0.2
            
            # Same country
            if item.country == content.country:
                similarity_score += 0.2
            
            # Similar tags
            common_tags = set(item.tags) & set(content.tags)
            similarity_score += len(common_tags) * 0.05
            
            if similarity_score > 0.3:
                similar.append((item, similarity_score))
        
        similar.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in similar[:limit]]
    
    async def generate_personalized_homepage(
        self,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[ContentItem]]:
        """
        Generate personalized homepage sections
        
        Returns dict with sections like:
        - Continue Watching
        - Recommended For You
        - Trending Now
        - Based on Recent Activity
        - Mood-based Picks
        """
        homepage = {}
        
        # Continue Watching
        homepage["continue_watching"] = await self.get_continue_watching(user_id)
        
        # Top Recommendations
        homepage["recommended_for_you"] = await self.get_recommendations(
            user_id, limit=15, context=context
        )
        
        # Trending Now
        homepage["trending_now"] = self._get_popular_content(10)
        
        # Category-specific recommendations
        if user_id in self.user_preferences:
            prefs = self.user_preferences[user_id]
            for category in prefs.favorite_categories[:3]:
                category_items = [
                    c for c in self.content_library
                    if c.category == category
                ]
                if category_items:
                    homepage[f"top_{category.lower()}"] = sorted(
                        category_items,
                        key=lambda x: x.popularity_score,
                        reverse=True
                    )[:10]
        
        return homepage


# Singleton instance
recommendation_engine = AIRecommendationEngine()


async def initialize_recommendations():
    """Initialize the recommendation engine"""
    await recommendation_engine.initialize()


if __name__ == "__main__":
    # Test the recommendation engine
    import asyncio
    
    async def test():
        await initialize_recommendations()
        
        # Simulate some watch history
        user_id = "test_user"
        for i in range(10):
            history = WatchHistory(
                content_id=f"content_{i}",
                watched_at=datetime.now() - timedelta(days=i),
                completion_percentage=random.uniform(50, 100),
                duration_watched=random.uniform(30, 120),
                rating_given=random.uniform(3.5, 5.0) if random.random() > 0.5 else None
            )
            recommendation_engine.add_watch_history(user_id, history)
        
        # Get recommendations
        recs = await recommendation_engine.get_recommendations(user_id, limit=10)
        print(f"\n🎯 Top 10 Recommendations for {user_id}:")
        for i, rec in enumerate(recs, 1):
            print(f"{i}. {rec.name} ({rec.category}) - Score: {rec.popularity_score:.2f}")
        
        # Get personalized homepage
        homepage = await recommendation_engine.generate_personalized_homepage(user_id)
        print(f"\n📱 Homepage sections generated: {list(homepage.keys())}")
    
    asyncio.run(test())
