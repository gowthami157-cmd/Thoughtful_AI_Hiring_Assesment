import re
import time
from typing import List, Dict, Tuple, Optional
from datetime import datetime

class ChatService:
    """Service class for handling chat interactions and question matching."""
    
    PREDEFINED_DATA = [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
    ]
    
    FALLBACK_RESPONSES = [
        "I'm here to help you learn about Thoughtful AI's automation agents. Could you ask me about EVA, CAM, PHIL, or our general services?",
        "I specialize in questions about Thoughtful AI's healthcare automation solutions. What would you like to know about our agents?",
        "I'm designed to help with questions about Thoughtful AI's services. Feel free to ask about our eligibility verification, claims processing, or payment posting agents!",
        "That's an interesting question! I'm focused on helping with Thoughtful AI-related inquiries. How can I assist you with our automation agents?"
    ]
    
    SIMILARITY_THRESHOLD = 0.1
    
    @staticmethod
    def preprocess_text(text: str) -> List[str]:
        """Preprocess text by converting to lowercase and extracting meaningful words."""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Split into words and filter out short words
        words = [word for word in text.split() if len(word) > 2]
        return words
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate similarity between two texts using word overlap."""
        words1 = set(ChatService.preprocess_text(text1))
        words2 = set(ChatService.preprocess_text(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    @staticmethod
    def enhanced_similarity(user_input: str, question: str) -> float:
        """Enhanced similarity calculation with key term boosting."""
        base_similarity = ChatService.calculate_similarity(user_input, question)
        
        # Key terms that should boost similarity scores
        key_terms = ['eva', 'cam', 'phil', 'agent', 'eligibility', 'claims', 'payment', 'benefits', 'thoughtful']
        user_lower = user_input.lower()
        question_lower = question.lower()
        
        boost = 0
        for term in key_terms:
            if term in user_lower and term in question_lower:
                boost += 0.2
        
        return min(base_similarity + boost, 1.0)
    
    @classmethod
    def find_best_match(cls, user_input: str) -> Tuple[Optional[Dict], float]:
        """Find the best matching question from predefined data."""
        if not user_input or not user_input.strip():
            return None, 0.0
        
        best_match = None
        best_score = 0.0
        
        for item in cls.PREDEFINED_DATA:
            score = cls.enhanced_similarity(user_input, item["question"])
            if score > best_score:
                best_score = score
                best_match = item
        
        return best_match, best_score
    
    @classmethod
    def process_user_input(cls, user_input: str) -> Dict[str, any]:
        """Process user input and return appropriate response."""
        try:
            # Input validation
            if not user_input or not user_input.strip():
                raise ValueError("Please enter a valid question.")
            
            if len(user_input.strip()) > 500:
                raise ValueError("Please keep your question under 500 characters.")
            
            trimmed_input = user_input.strip()
            
            # Find best matching question
            best_match, best_score = cls.find_best_match(trimmed_input)
            
            # Simulate processing time for more natural interaction
            time.sleep(0.5)
            
            if best_match and best_score > cls.SIMILARITY_THRESHOLD:
                response_message = best_match["answer"]
            else:
                # Use random fallback response
                import random
                response_message = random.choice(cls.FALLBACK_RESPONSES)
            
            return {
                "message": response_message,
                "is_from_agent": True,
                "timestamp": datetime.now(),
                "success": True
            }
            
        except Exception as e:
            return {
                "message": str(e) if isinstance(e, ValueError) else "I encountered an error processing your request. Please try again.",
                "is_from_agent": True,
                "timestamp": datetime.now(),
                "success": False
            }
    
    @staticmethod
    def create_user_message(user_input: str) -> Dict[str, any]:
        """Create a user message object."""
        return {
            "message": user_input,
            "is_from_agent": False,
            "timestamp": datetime.now(),
            "success": True
        }