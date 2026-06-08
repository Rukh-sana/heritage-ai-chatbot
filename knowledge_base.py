"""
Knowledge Base for Mohenjo-Daro
Reliable sources: UNESCO, Department of Archaeology Pakistan, Britannica
"""

class MohenjoDaroKB:
    def __init__(self):
        self.site_name = "Mohenjo-Daro"
        self.location = "Larkana District, Sindh, Pakistan"
        
        self.data = {
            "history": """Mohenjo-Daro, meaning 'Mound of the Dead' in Sindhi, was built around 2500 BCE as one of the largest settlements of the ancient Indus Valley Civilization. It was one of the world's earliest major cities, contemporary with ancient Egypt and Mesopotamia. The city was abandoned around 1900 BCE, possibly due to climate change or river migration. It was rediscovered in 1922 by archaeologist R. D. Banerji and became a UNESCO World Heritage Site in 1980.""",
            
            "architecture": """Mohenjo-Daro showcases remarkable urban planning: grid-like street system with precise orientation, advanced water management with over 700 wells, the Great Bath (a 12m x 7m brick-lined pool for ritual bathing), covered drainage systems running beneath streets, multi-story houses built with standardized fire-baked bricks, and a Citadel mound for public buildings. Main avenues were up to 10 meters wide.""",
            
            "importance": """Mohenjo-Daro is critically important as a UNESCO World Heritage Site (1980). It represents the best-preserved urban center of the Indus Valley Civilization, showing South Asia's first urban society from 2500-1900 BCE. It demonstrates advanced engineering, social organization, and contains famous artifacts like the 'Dancing Girl' bronze statue and 'Priest-King' sculpture.""",
            
            "interesting_facts": [
                "The city had over 700 wells - one of the ancient world's best water systems",
                "Mohenjo-Daro means 'Mound of the Dead' in Sindhi language",
                "The city's original name remains unknown as Indus script is still undeciphered",
                "Each house had its own bathroom and toilet connected to covered drains",
                "The Great Bath could hold approximately 90,000 liters of water",
                "No evidence of palaces or temples - suggesting an egalitarian society",
                "Standardized brick sizes (1:2:4 ratio) were used across all buildings",
                "Seals found indicate active trade with Mesopotamia and other regions"
            ],
            
            "preservation": """Mohenjo-Daro faces serious preservation challenges: rising water table causing salt crystallization damage to brick structures, flooding from the Indus River, insufficient international conservation funding, climate change impacts, and uncontrolled tourism causing physical damage. UNESCO provides technical assistance for preservation efforts.""",
            
            "visitor_info": """Mohenjo-Daro is located 28 km from Larkana city, Sindh, Pakistan. Best time to visit is November to February when temperatures are moderate. Entry fee is PKR 500 for Pakistanis and PKR 1000 for foreigners. The on-site museum displays artifacts including seals, pottery, and jewelry. Guided tours are available in English, Urdu, and Sindhi."""
        }
    
    def get_relevant_info(self, question):
        """Get relevant info based on question keywords"""
        q = question.lower()
        
        if any(word in q for word in ['history', 'origin', 'when', 'built', 'found', 'discover', 'age', 'ancient', 'civilization']):
            return self.data["history"]
        elif any(word in q for word in ['architecture', 'build', 'structure', 'design', 'great bath', 'drain', 'brick', 'grid', 'layout', 'city planning', 'urban']):
            return self.data["architecture"]
        elif any(word in q for word in ['important', 'significance', 'unesco', 'heritage', 'value', 'why famous', 'wonder', 'world heritage']):
            return self.data["importance"]
        elif any(word in q for word in ['fact', 'interesting', 'unique', 'amazing', 'surprising', 'tell me about']):
            return "\n".join([f"• {fact}" for fact in self.data["interesting_facts"]])
        elif any(word in q for word in ['preservation', 'protect', 'conservation', 'damage', 'threat', 'risk', 'challenge', 'problem']):
            return self.data["preservation"]
        elif any(word in q for word in ['visit', 'tourist', 'ticket', 'entry', 'travel', 'location', 'where', 'timing', 'fee', 'museum']):
            return self.data["visitor_info"]
        
        return None

# Create global instance
kb = MohenjoDaroKB()