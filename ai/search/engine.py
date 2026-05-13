"""
AI Smart Search Engine
=======================
Advanced search with semantic, voice, and natural language support.

Features:
- Semantic Search
- Voice Search
- Natural Language Processing
- Image Recognition (OCR)
- Multi-language Support

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

import re
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
from enum import Enum


class SearchType(Enum):
    """Types of search."""
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    VOICE = "voice"
    NATURAL_LANGUAGE = "natural_language"
    OCR = "ocr"
    IMAGE = "image"


class SmartSearchEngine:
    """
    Advanced AI-powered search engine for IPTV and media content.
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize the smart search engine.
        
        Args:
            language: Default search language ('en' or 'ar')
        """
        self.language = language
        self.search_index = {}
        self.semantic_model = None
        self.voice_recognizer = None
        self.ocr_engine = None
        
        # Load models lazily
        self._models_loaded = False
        
    def _load_models(self):
        """Load AI models for search."""
        if self._models_loaded:
            return
        
        try:
            # Try to load sentence transformers for semantic search
            from sentence_transformers import SentenceTransformer
            model_name = "paraphrase-multilingual-MiniLM-L12-v2"
            self.semantic_model = SentenceTransformer(model_name)
            print(f"Loaded semantic model: {model_name}")
        except ImportError:
            print("Sentence transformers not installed, using keyword search fallback")
        
        try:
            # Try to load speech recognition
            import speech_recognition as sr
            self.voice_recognizer = sr.Recognizer()
            print("Voice recognizer initialized")
        except ImportError:
            print("Speech recognition not available")
        
        try:
            # Try to load OCR
            import pytesseract
            self.ocr_engine = pytesseract
            print("OCR engine initialized")
        except ImportError:
            print("OCR not available")
        
        self._models_loaded = True
    
    async def search(self, query: str, 
                    search_type: SearchType = SearchType.SEMANTIC,
                    filters: Optional[Dict[str, Any]] = None,
                    limit: int = 20) -> List[Dict[str, Any]]:
        """
        Perform intelligent search.
        
        Args:
            query: Search query
            search_type: Type of search to perform
            filters: Additional filters (category, country, etc.)
            limit: Maximum results to return
            
        Returns:
            List of matching results
        """
        self._load_models()
        
        if search_type == SearchType.SEMANTIC:
            return await self._semantic_search(query, filters, limit)
        
        elif search_type == SearchType.VOICE:
            return await self._voice_search(query, filters, limit)
        
        elif search_type == SearchType.NATURAL_LANGUAGE:
            return await self._natural_language_search(query, filters, limit)
        
        elif search_type == SearchType.OCR:
            return await self._ocr_search(query, filters, limit)
        
        else:
            return await self._keyword_search(query, filters, limit)
    
    async def _semantic_search(self, query: str, 
                              filters: Optional[Dict[str, Any]],
                              limit: int) -> List[Dict[str, Any]]:
        """Perform semantic similarity search."""
        if self.semantic_model is None:
            # Fallback to keyword search
            return await self._keyword_search(query, filters, limit)
        
        try:
            # Encode query
            query_embedding = self.semantic_model.encode([query])[0]
            
            # Search through indexed content
            results = []
            for item_id, item_data in self.search_index.items():
                if 'embedding' not in item_data:
                    continue
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(
                    query_embedding, 
                    item_data['embedding']
                )
                
                if similarity > 0.3:  # Threshold
                    result = item_data.copy()
                    result['score'] = float(similarity)
                    results.append(result)
            
            # Sort by score
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # Apply filters
            if filters:
                results = self._apply_filters(results, filters)
            
            return results[:limit]
            
        except Exception as e:
            print(f"Semantic search error: {e}")
            return await self._keyword_search(query, filters, limit)
    
    async def _keyword_search(self, query: str,
                             filters: Optional[Dict[str, Any]],
                             limit: int) -> List[Dict[str, Any]]:
        """Perform traditional keyword search."""
        query_lower = query.lower()
        results = []
        
        for item_id, item_data in self.search_index.items():
            # Search in title, description, tags
            searchable_text = f"{item_data.get('title', '')} {item_data.get('description', '')} {item_data.get('tags', '')}".lower()
            
            if query_lower in searchable_text:
                result = item_data.copy()
                result['score'] = 1.0
                results.append(result)
        
        # Apply filters
        if filters:
            results = self._apply_filters(results, filters)
        
        # Sort by relevance
        results.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        
        return results[:limit]
    
    async def _voice_search(self, audio_input: str,
                           filters: Optional[Dict[str, Any]],
                           limit: int) -> List[Dict[str, Any]]:
        """Process voice input and search."""
        if self.voice_recognizer is None:
            print("Voice recognition not available")
            return []
        
        try:
            # Convert speech to text
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            # If audio_input is a file path
            if Path(audio_input).exists():
                with sr.AudioFile(audio_input) as source:
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio, language=self.language)
            else:
                # Assume it's already transcribed text
                text = audio_input
            
            # Search with transcribed text
            return await self._natural_language_search(text, filters, limit)
            
        except Exception as e:
            print(f"Voice search error: {e}")
            return []
    
    async def _natural_language_search(self, query: str,
                                      filters: Optional[Dict[str, Any]],
                                      limit: int) -> List[Dict[str, Any]]:
        """Process natural language queries."""
        # Extract intent and entities
        processed_query = self._parse_natural_language(query)
        
        # Update filters with extracted entities
        if filters is None:
            filters = {}
        
        if 'category' in processed_query:
            filters['category'] = processed_query['category']
        
        if 'country' in processed_query:
            filters['country'] = processed_query['country']
        
        if 'year' in processed_query:
            filters['year'] = processed_query['year']
        
        # Perform search with extracted query
        search_query = processed_query.get('query', query)
        return await self._semantic_search(search_query, filters, limit)
    
    async def _ocr_search(self, image_path: str,
                         filters: Optional[Dict[str, Any]],
                         limit: int) -> List[Dict[str, Any]]:
        """Extract text from image and search."""
        if self.ocr_engine is None:
            print("OCR not available")
            return []
        
        try:
            import cv2
            from PIL import Image
            
            # Read image
            image = cv2.imread(image_path)
            
            # Preprocess for better OCR
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text
            text = self.ocr_engine.image_to_string(thresh, lang='eng+ara')
            
            # Search with extracted text
            return await self._keyword_search(text.strip(), filters, limit)
            
        except Exception as e:
            print(f"OCR search error: {e}")
            return []
    
    def _parse_natural_language(self, query: str) -> Dict[str, Any]:
        """Parse natural language query to extract intent and entities."""
        result = {'query': query}
        
        query_lower = query.lower()
        
        # Detect category intent
        category_patterns = {
            'sports': ['sport', 'football', 'soccer', 'basketball', 'tennis'],
            'movies': ['movie', 'film', 'cinema'],
            'series': ['series', 'show', 'tv show', 'episode'],
            'news': ['news', 'breaking'],
            'kids': ['kids', 'children', 'cartoon'],
            'documentary': ['documentary', 'docu'],
            'music': ['music', 'song', 'concert'],
        }
        
        for category, keywords in category_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                result['category'] = category
                break
        
        # Detect country
        country_patterns = {
            'egypt': ['egypt', 'egyptian'],
            'saudi': ['saudi', 'saudi arabia'],
            'uae': ['uae', 'emirates', 'dubai'],
            'usa': ['usa', 'american', 'us'],
            'uk': ['uk', 'british', 'united kingdom'],
        }
        
        for country, keywords in country_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                result['country'] = country
                break
        
        # Detect year
        year_match = re.search(r'\b(19|20)\d{2}\b', query)
        if year_match:
            result['year'] = int(year_match.group())
        
        # Detect quality
        quality_patterns = {
            '4k': ['4k', 'ultra hd', 'uhd'],
            'hd': ['hd', 'high definition'],
            'fhd': ['full hd', '1080p'],
        }
        
        for quality, keywords in quality_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                result['quality'] = quality
                break
        
        return result
    
    def _apply_filters(self, results: List[Dict], 
                      filters: Dict[str, Any]) -> List[Dict]:
        """Apply filters to search results."""
        filtered = []
        
        for result in results:
            match = True
            
            for key, value in filters.items():
                if key in result:
                    if result[key] != value:
                        match = False
                        break
            
            if match:
                filtered.append(result)
        
        return filtered
    
    def _cosine_similarity(self, vec1: List[float], 
                          vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def index_content(self, items: List[Dict[str, Any]]):
        """
        Index content for search.
        
        Args:
            items: List of content items to index
        """
        self._load_models()
        
        for item in items:
            item_id = item.get('id')
            if not item_id:
                continue
            
            # Create searchable text
            text = f"{item.get('title', '')} {item.get('description', '')} {item.get('tags', '')}"
            
            # Generate embedding if semantic model available
            if self.semantic_model:
                embedding = self.semantic_model.encode([text])[0]
                item['embedding'] = embedding.tolist()
            
            self.search_index[item_id] = item
        
        print(f"Indexed {len(items)} items")
    
    def clear_index(self):
        """Clear the search index."""
        self.search_index = {}
        print("Search index cleared")


# Singleton instance
_search_engine: Optional[SmartSearchEngine] = None


def get_search_engine(language: str = "en") -> SmartSearchEngine:
    """Get or create the smart search engine singleton."""
    global _search_engine
    if _search_engine is None:
        _search_engine = SmartSearchEngine(language)
    return _search_engine


async def smart_search(query: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Convenience function for smart search.
    
    Args:
        query: Search query
        **kwargs: Additional arguments
        
    Returns:
        List of search results
    """
    engine = get_search_engine()
    return await engine.search(query, **kwargs)
