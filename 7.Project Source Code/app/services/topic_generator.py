"""
Topic Generator Service - Conversation Generation using GPT-2
Based on your documentation: Epic 2 - Topic Generator Service
"""

from transformers import pipeline, set_seed
from typing import List
import random

# Set seed for reproducibility
set_seed(42)

# Load model once at startup
print("Loading GPT-2 model for conversation generation...")
generator = pipeline(
    "text-generation",
    model="gpt2",
    max_length=80
)
print("✅ GPT-2 loaded successfully!")


def generate_topics(
    themes: List[str],
    user_interests: List[str],
    max_suggestions: int = 3
) -> List[str]:
    """
    Generate conversation starters using GPT-2
    
    Args:
        themes: Extracted event themes
        user_interests: User's interests/interests list
        max_suggestions: Number of suggestions to return
    
    Returns:
        List of conversation starter suggestions
    """
    if not themes:
        themes = ["professional networking"]
    
    if not user_interests:
        user_interests = ["meeting new people"]
    
    # Build a structured prompt
    themes_str = ", ".join(themes[:3])
    interests_str = ", ".join(user_interests[:3])
    
    prompt = f"""You are a professional at a networking event about {themes_str}.
Your interests include {interests_str}.
Generate {max_suggestions} natural conversation starters:
1."""
    
    try:
        # Generate text
        result = generator(
            prompt,
            max_length=80,
            temperature=0.85,
            top_p=0.9,
            do_sample=True,
            pad_token_id=50256  # GPT-2's EOS token
        )
        
        # Extract and clean the generated text
        generated_text = result[0]['generated_text']
        
        # Remove the prompt from the start
        if generated_text.startswith(prompt):
            raw_suggestions = generated_text[len(prompt):].strip()
        else:
            raw_suggestions = generated_text.strip()
        
        # Split into separate suggestions
        suggestions = _clean_suggestions(raw_suggestions, max_suggestions)
        
        return suggestions if suggestions else _fallback_suggestions(themes, user_interests)
        
    except Exception as e:
        print(f"⚠️ Generation error: {e}")
        return _fallback_suggestions(themes, user_interests)


def _clean_suggestions(raw_text: str, max_count: int) -> List[str]:
    """Clean and parse generated suggestions"""
    # Split by newline or numbered list
    lines = raw_text.split('\n')
    suggestions = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove numbering or bullets
        cleaned = line.lstrip('0123456789.·•-* ').strip()
        
        # Keep only if it's a reasonable length
        if len(cleaned) > 10 and len(cleaned) < 150:
            suggestions.append(cleaned)
        
        if len(suggestions) >= max_count:
            break
    
    return suggestions


def _fallback_suggestions(themes: List[str], interests: List[str]) -> List[str]:
    """Fallback: template-based suggestions if GPT-2 fails"""
    theme = themes[0] if themes else "networking"
    interest = interests[0] if interests else "professional development"
    
    templates = [
        f"I'm really excited to learn more about {theme}. What brings you here today?",
        f"Your background in {interest} sounds fascinating. How did you get started?",
        f"I noticed you're interested in {theme}. What do you think are the biggest trends right now?",
        f"With your experience in {interest}, I'd love to hear your perspective on {theme}.",
        f"What's the most interesting thing you've learned about {theme} recently?"
    ]
    
    # Shuffle and return
    random.shuffle(templates)
    return templates[:3]