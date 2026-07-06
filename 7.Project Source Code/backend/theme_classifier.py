from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import List, Dict, Tuple
import re

class ThemeClassifier:
    """
    Theme extraction using DistilBERT for zero-shot classification
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading DistilBERT for theme classification on {self.device}...")
        
        # Use a smaller, faster model for theme classification
        self.classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",  # Optimized for speed
            device=0 if self.device == "cuda" else -1
        )
        
        # Extended list of networking themes
        self.theme_candidates = [
            "artificial intelligence", "machine learning", "data science", "cloud computing",
            "cybersecurity", "blockchain", "devops", "software engineering", "web development",
            "mobile development", "ux design", "product management", "agile methodology",
            "startup", "entrepreneurship", "venture capital", "business strategy",
            "marketing", "digital marketing", "content creation", "social media",
            "finance", "fintech", "cryptocurrency", "investment banking",
            "healthcare", "biotech", "pharmaceutical", "medical devices",
            "education", "edtech", "online learning", "professional development",
            "sustainability", "green energy", "climate tech", "environmental science",
            "leadership", "team building", "organizational development", "human resources",
            "networking", "career growth", "personal branding", "public speaking",
            "diversity", "inclusion", "equity", "social impact",
            "e-commerce", "retail tech", "supply chain", "logistics",
            "real estate", "proptech", "construction", "architecture",
            "entertainment", "media", "gaming", "esports",
            "tourism", "hospitality", "food tech", "agriculture"
        ]
        
        print(f"Loaded {len(self.theme_candidates)} theme candidates")
    
    def extract_themes(self, event_description: str, top_k: int = 5) -> List[Dict[str, float]]:
        """
        Extract top themes from event description using zero-shot classification
        
        Args:
            event_description: The event description text
            top_k: Number of themes to return
        
        Returns:
            List of dictionaries with theme and confidence score
        """
        if not event_description or len(event_description.strip()) < 10:
            return []
        
        # Clean the text
        cleaned_text = self._clean_text(event_description)
        
        try:
            # Perform zero-shot classification
            result = self.classifier(
                cleaned_text,
                candidate_labels=self.theme_candidates,
                multi_label=True
            )
            
            # Extract top themes with scores
            themes = []
            for label, score in zip(result['labels'][:top_k], result['scores'][:top_k]):
                if score > 0.2:  # Confidence threshold
                    themes.append({
                        "theme": label,
                        "confidence": round(score, 3)
                    })
            
            return themes
            
        except Exception as e:
            print(f"Error in theme extraction: {e}")
            # Fallback to keyword matching
            return self._keyword_based_extraction(cleaned_text, top_k)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\-\']', '', text)
        return text.strip()
    
    def _keyword_based_extraction(self, text: str, top_k: int = 5) -> List[Dict[str, float]]:
        """Fallback: Simple keyword-based theme extraction"""
        text_lower = text.lower()
        found_themes = []
        
        for theme in self.theme_candidates:
            if theme in text_lower:
                # Calculate a simple relevance score based on frequency and position
                count = text_lower.count(theme)
                # Check if theme appears early in text (more important)
                position_score = 1.0 - (text_lower.find(theme) / len(text_lower)) if theme in text_lower else 0
                score = min(1.0, (count * 0.3) + (position_score * 0.7))
                found_themes.append({"theme": theme, "confidence": round(score, 3)})
        
        # Sort by confidence and return top_k
        found_themes.sort(key=lambda x: x['confidence'], reverse=True)
        return found_themes[:top_k]
    
    def get_theme_summary(self, event_description: str) -> str:
        """Get a comma-separated string of top themes"""
        themes = self.extract_themes(event_description, top_k=5)
        if not themes:
            return "general networking, professional development"
        return ", ".join([t['theme'] for t in themes if t['confidence'] > 0.2])

# Singleton instance
theme_classifier = ThemeClassifier()