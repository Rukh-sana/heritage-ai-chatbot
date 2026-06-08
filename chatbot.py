"""
Gemini LLM Chatbot for Mohenjo-Daro Heritage Site
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
from .knowledge_base import kb

load_dotenv()

class HeritageChatbot:
    def __init__(self):
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.kb = kb
        
    def get_response(self, user_question):
        """Generate response using knowledge base + Gemini LLM"""
        
        # First check knowledge base
        kb_info = self.kb.get_relevant_info(user_question)
        
        # Create comprehensive prompt for Gemini
        if kb_info:
            prompt = f"""You are an expert archaeologist and tour guide specializing in Mohenjo-Daro and the Indus Valley Civilization.

IMPORTANT RULES:
1. NEVER say "As an AI, I cannot display images" - the app handles images separately
2. NEVER mention that you can't show images
3. Just provide TEXT descriptions enthusiastically
4. If asked to "show" or "display" something, describe it vividly instead

Use this accurate information from verified sources:
{kb_info}

SITE: {self.kb.site_name} (2500-1900 BCE, UNESCO World Heritage)
LOCATION: {self.kb.location}

USER QUESTION: {user_question}

INSTRUCTIONS:
1. Use the knowledge base information as your primary source
2. Provide accurate, educational, and engaging answers
3. Keep responses informative but concise (3-5 sentences normally)
4. For facts questions, use bullet points
5. Be warm and enthusiastic about the heritage site
6. Describe things vividly when asked to "show" something
7. NEVER say you can't display images - just describe what they'd see

YOUR ANSWER:"""
        else:
            prompt = f"""You are an expert archaeologist and tour guide specializing in Mohenjo-Daro and the Indus Valley Civilization.

IMPORTANT RULES:
1. NEVER say "As an AI, I cannot display images" - the app handles images separately
2. NEVER mention that you can't show images  
3. Just provide TEXT descriptions enthusiastically
4. If asked to "show" or "display" something, describe it vividly instead

SITE: {self.kb.site_name} (2500-1900 BCE, UNESCO World Heritage)
LOCATION: {self.kb.location}, Pakistan

USER QUESTION: {user_question}

INSTRUCTIONS:
1. Provide accurate archaeological information based on verified sources
2. If unsure, say "Based on available archaeological evidence..."
3. Keep responses to 3-5 sentences
4. Be educational and engaging
5. Stay focused on Mohenjo-Daro and Indus Valley Civilization
6. Describe things vividly when asked to "show" something
7. NEVER say you can't display images - just describe what they'd see

YOUR ANSWER:"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered a technical issue. Please try again. Error: {str(e)}"
    
    def get_sample_qa(self):
        """Generate 5 sample Q&A pairs"""
        questions = [
            "What is the history of Mohenjo-Daro?",
            "Describe the architecture and urban planning of Mohenjo-Daro.",
            "Why is Mohenjo-Daro important as a UNESCO World Heritage site?",
            "Give me 5 interesting facts about Mohenjo-Daro.",
            "What preservation challenges does Mohenjo-Daro face today?"
        ]
        
        qa_pairs = []
        for q in questions:
            a = self.get_response(q)
            qa_pairs.append({"question": q, "answer": a})
        
        return qa_pairs