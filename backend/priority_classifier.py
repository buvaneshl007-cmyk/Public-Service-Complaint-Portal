import re

class PriorityClassifier:
    """Intelligent priority classification based on keywords, urgency phrases, and context"""
    
    def __init__(self):
        # URGENCY INDICATORS - These override keyword matching
        # HIGH urgency phrases (immediate action required)
        self.high_urgency_phrases = [
            'urgent', 'emergency', 'immediate attention', 'asap', 'as soon as possible',
            'critical', 'hazard', 'life threatening', 'danger', 'right now',
            'immediately', 'serious', 'threatening', 'unsafe condition'
        ]
        
        # LOW urgency phrases (can wait, not urgent)
        self.low_urgency_phrases = [
            'not urgent', 'no rush', 'whenever possible', 'when you can', 
            'regular schedule', 'routine', 'at your convenience', 'no hurry',
            'eventually', 'when available', 'not an emergency', 'can wait',
            'during normal hours', 'next available', 'scheduled maintenance'
        ]
        
        # MEDIUM urgency phrases (needs attention but not critical)
        self.medium_urgency_phrases = [
            'soon', 'needs attention', 'should be fixed', 'inconvenience',
            'causing problems', 'affecting service', 'delayed'
        ]
        
        # Define priority keywords for municipality complaints
        # HIGH: Life-threatening, safety hazards, critical infrastructure
        self.high_priority_keywords = [
            'fire', 'gas leak', 'leakage', 'burst pipe', 'explosion', 
            'safety hazard', 'injury', 'accident',
            'electrical spark', 'smoke', 'overflow', 'flooding',
            'road collapse', 'tree fallen', 'exposed wire'
        ]
        
        # MEDIUM: Service disruptions, repairs needed, functionality issues
        self.medium_priority_keywords = [
            'not working', 'broken', 'malfunction', 'damaged',
            'slow service', 'partial blockage', 'dim light', 
            'needs repair', 'pothole', 'crack', 'loose',
            'stuck', 'jammed'
        ]
        
        # LOW: Routine maintenance, cleanliness, general requests
        self.low_priority_keywords = [
            'cleaning', 'garbage collection', 'street cleaning', 'sweeping',
            'dust', 'routine maintenance', 'scheduled', 'general inquiry',
            'request for', 'suggestion', 'feedback', 'normal'
        ]
    
    def classify(self, text):
        """
        Classify priority based on text content with urgency detection
        Returns: 'High', 'Medium', or 'Low'
        
        Priority Logic:
        1. First check URGENCY PHRASES (they override keyword matching)
        2. Then check PRIORITY KEYWORDS
        3. Default to Low if no clear indicators
        """
        if not text:
            return 'Low'
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # STEP 1: Check for LOW urgency phrases first (e.g., "not urgent", "whenever possible")
        # These OVERRIDE any keywords that might suggest higher priority
        if any(phrase in text_lower for phrase in self.low_urgency_phrases):
            return 'Low'
        
        # STEP 2: Check for HIGH urgency phrases (e.g., "urgent", "emergency", "immediate")
        if any(phrase in text_lower for phrase in self.high_urgency_phrases):
            return 'High'
        
        # STEP 3: Check for MEDIUM urgency phrases
        if any(phrase in text_lower for phrase in self.medium_urgency_phrases):
            return 'Medium'
        
        # STEP 4: Now check KEYWORDS (only if no urgency phrases were found)
        # Check HIGH priority keywords (critical/emergency issues)
        if any(keyword in text_lower for keyword in self.high_priority_keywords):
            return 'High'
        
        # Then check MEDIUM priority keywords (service issues, repairs)
        elif any(keyword in text_lower for keyword in self.medium_priority_keywords):
            return 'Medium'
        
        # Check LOW priority keywords (routine, cleaning, general requests)
        elif any(keyword in text_lower for keyword in self.low_priority_keywords):
            return 'Low'
        
        # Default to LOW if nothing matches
        else:
            return 'Low'
    
    def _count_matches(self, text, keywords):
        """Count how many keywords appear in text"""
        count = 0
        for keyword in keywords:
            if keyword in text:
                count += 1
        return count
    
    def get_category(self, text):
        """
        Categorize complaint based on content
        Returns: Category string
        """
        if not text:
            return 'General'
        
        text_lower = text.lower()
        
        categories = {
            'Electrical': ['power', 'electricity', 'electrical', 'light', 'bulb', 'switch', 'socket', 'spark'],
            'Plumbing': ['water', 'pipe', 'leak', 'plumbing', 'drain', 'toilet', 'sink', 'tap', 'faucet'],
            'Network/IT': ['wifi', 'internet', 'network', 'computer', 'printer', 'software', 'system', 'it'],
            'HVAC': ['heating', 'cooling', 'ac', 'air conditioning', 'temperature', 'ventilation', 'hvac'],
            'Safety': ['fire', 'safety', 'security', 'emergency', 'danger', 'hazard', 'accident'],
            'Cleaning': ['cleaning', 'dirty', 'trash', 'garbage', 'hygiene', 'sanitation'],
            'Maintenance': ['repair', 'fix', 'broken', 'maintenance', 'damage'],
            'Facilities': ['room', 'building', 'facility', 'door', 'window', 'lock', 'key']
        }
        
        # Find best matching category
        best_category = 'General'
        max_matches = 0
        
        for category, keywords in categories.items():
            matches = self._count_matches(text_lower, keywords)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        return best_category
    
    def get_priority_explanation(self, priority, text):
        """Generate explanation for why a priority was assigned"""
        text_lower = text.lower() if text else ''
        
        # Check urgency phrases first
        matched_urgency = []
        if priority == 'High':
            matched_urgency = [phrase for phrase in self.high_urgency_phrases if phrase in text_lower]
        elif priority == 'Low':
            matched_urgency = [phrase for phrase in self.low_urgency_phrases if phrase in text_lower]
        elif priority == 'Medium':
            matched_urgency = [phrase for phrase in self.medium_urgency_phrases if phrase in text_lower]
        
        if matched_urgency:
            return f"Classified as {priority} priority due to urgency: '{matched_urgency[0]}'"
        
        # Check keywords
        matched_keywords = []
        if priority == 'High':
            matched_keywords = [kw for kw in self.high_priority_keywords if kw in text_lower]
        elif priority == 'Medium':
            matched_keywords = [kw for kw in self.medium_priority_keywords if kw in text_lower]
        else:
            matched_keywords = [kw for kw in self.low_priority_keywords if kw in text_lower]
        
        if matched_keywords:
            return f"Classified as {priority} priority due to keywords: {', '.join(matched_keywords[:3])}"
        else:
            return f"Classified as {priority} priority based on content analysis"
