from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Tuple, Optional, Dict, List
import re
import random

class ConversationGenerator:
    """
    Conversation starter generation using GPT-2 Small
    Optimized for speed and natural language output
    """
    
    def __init__(self, model_name: str = "gpt2"):
        """
        Initialize GPT-2 model for conversation generation
        
        Options:
        - "gpt2": Small, fast (124M parameters)
        - "distilgpt2": Even faster, slightly lower quality (82M parameters)
        - "gpt2-medium": Better quality but slower (355M parameters)
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading {model_name} for conversation generation on {self.device}...")
        print("This may take a few minutes on first run...")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add padding token if missing
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Move model to device
        self.model.to(self.device)
        
        # Initialize generation pipeline
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1,
            model_kwargs={"torch_dtype": torch.float16} if self.device == "cuda" else {}
        )
        
        # Templates for prompt engineering
        self.prompt_templates = self._load_prompt_templates()
        
        print(f"✅ {model_name} loaded successfully!")
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load various prompt templates for different contexts"""
        return {
            "professional": """You are a professional networking coach. Generate 3 personalized conversation starters.

User's Background: {user_bio}
Event: {event_description}
Key Themes: {event_themes}

Requirements:
- Be specific and relevant
- Show genuine interest
- Connect user's expertise to the event

Conversation Starters:
1.""",
            
            "casual": """You're at a networking event. Create 3 friendly, natural conversation starters.

About the person: {user_bio}
About the event: {event_description}
Themes: {event_themes}

Make them sound natural and engaging:

1.""",
            
            "icebreaker": """Generate 3 creative icebreaker questions for a networking event.

Person's background: {user_bio}
Event context: {event_description}
Topics of interest: {event_themes}

Icebreakers:
1.""",
            
            "expert": """As a networking expert, craft 3 strategic conversation starters.

Professional background: {user_bio}
Event details: {event_description}
Themes: {event_themes}

Strategic starters:
1."""
        }
    
    def generate_starter(
        self,
        user_bio: str,
        event_description: str,
        event_themes: str,
        style: str = "professional",
        custom_prompt: Optional[str] = None,
        max_length: int = 200,
        temperature: float = 0.85,
        top_p: float = 0.9
    ) -> Tuple[str, str]:
        """
        Generate a conversation starter based on input context
        
        Args:
            user_bio: User's biography/text
            event_description: Event description
            event_themes: Extracted themes
            style: Prompt style (professional, casual, icebreaker, expert)
            custom_prompt: Override default prompt
            max_length: Maximum generation length
            temperature: Randomness control (0.0-1.0)
            top_p: Nucleus sampling parameter
        
        Returns:
            Tuple of (generated_text, prompt_used)
        """
        
        # Select or build prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            template = self.prompt_templates.get(style, self.prompt_templates["professional"])
            prompt = template.format(
                user_bio=user_bio[:200],  # Limit length to avoid token overflow
                event_description=event_description[:200],
                event_themes=event_themes[:100]
            )
        
        # Generate text
        try:
            generated = self.generator(
                prompt,
                max_length=min(max_length, 512),
                num_return_sequences=1,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1
            )
            
            # Extract and clean the generated text
            full_text = generated[0]['generated_text']
            
            # Remove the prompt from the start
            if full_text.startswith(prompt):
                starter_text = full_text[len(prompt):].strip()
            else:
                # Fallback: try to find where the prompt ends
                starter_text = full_text.strip()
                # Remove common prefixes
                starter_text = re.sub(r'^Conversation Starters:\s*', '', starter_text)
                starter_text = re.sub(r'^Icebreakers:\s*', '', starter_text)
                starter_text = re.sub(r'^Strategic starters:\s*', '', starter_text)
            
            # Clean and format the response
            starters = self._parse_and_clean_starters(starter_text)
            
            # If we got multiple starters, pick the best one
            if starters:
                selected = random.choice(starters)
                return selected, prompt
            
            # If parsing failed, return cleaned raw text
            cleaned = self._clean_text(starter_text)
            if len(cleaned) < 20:
                # Fallback to template-based generation
                fallback = self._generate_fallback_starter(user_bio, event_description, event_themes)
                return fallback, "fallback_template"
            
            return cleaned, prompt
            
        except Exception as e:
            print(f"Error generating conversation starter: {e}")
            fallback = self._generate_fallback_starter(user_bio, event_description, event_themes)
            return fallback, "fallback_template"
    
    def _parse_and_clean_starters(self, text: str) -> List[str]:
        """Parse multiple starters and clean them"""
        # Split by common separators
        separators = [r'\d+\.', r'•', r'-', r'\*']
        
        starters = []
        current_starter = ""
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a number or bullet
            is_new_starter = False
            for sep in separators:
                if re.match(sep, line):
                    is_new_starter = True
                    break
            
            if is_new_starter:
                if current_starter:
                    starters.append(self._clean_text(current_starter))
                # Remove the separator from the start
                line = re.sub(r'^\d+\.\s*|^[•\-*]\s*', '', line)
                current_starter = line
            else:
                if current_starter:
                    current_starter += " " + line
                else:
                    current_starter = line
        
        if current_starter:
            starters.append(self._clean_text(current_starter))
        
        # Filter out empty or too short starters
        starters = [s for s in starters if len(s) > 15 and len(s) < 300]
        
        return starters
    
    def _clean_text(self, text: str) -> str:
        """Clean generated text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common unwanted patterns
        text = re.sub(r'^[:\s]+', '', text)
        text = re.sub(r'\[.*?\]', '', text)  # Remove brackets
        text = re.sub(r'\(.*?\)', '', text)  # Remove parentheses (optional)
        
        # Ensure proper punctuation
        if not text.endswith(('.', '?', '!')):
            text += '.'
        
        return text.strip()
    
    def _generate_fallback_starter(self, user_bio: str, event_desc: str, themes: str) -> str:
        """Generate a fallback starter using templates"""
        # Extract key information
        bio_short = user_bio[:50].split('.')[0] if user_bio else "your expertise"
        theme_list = [t.strip() for t in themes.split(',') if t.strip()]
        main_theme = theme_list[0] if theme_list else "networking"
        
        templates = [
            f"Given your background in {bio_short}, I'm curious about your perspective on {main_theme}. What trends are you most excited about?",
            
            f"I noticed you have experience with {bio_short}. How do you see {main_theme} evolving over the next few years?",
            
            f"Your work in {bio_short} is really interesting. What brought you to this event, and what are you hoping to learn?",
            
            f"As someone with expertise in {bio_short}, I'd love to hear your thoughts on {main_theme}. What's the biggest challenge you see in this space?",
            
            f"Your background in {bio_short} caught my attention. How do you approach {main_theme} in your current role?"
        ]
        
        return random.choice(templates)
    
    def get_model_info(self) -> Dict[str, any]:
        """Return model information"""
        return {
            "model": self.model_name,
            "device": self.device,
            "parameters": "124M" if "gpt2" in self.model_name else "Unknown",
            "status": "loaded"
        }

# Singleton instance
conversation_generator = ConversationGenerator()