from google import genai
from src.utils.config import GEMINI_API_KEY  # Ensure this import is here
import json

# PASS THE KEY HERE:
client = genai.Client(api_key=GEMINI_API_KEY) 

class TriageAgent:
    def analyze(self, symptoms, city):
        # 1. IMMEDIATE EMERGENCY OVERRIDE
        s_low = symptoms.lower().strip()
        emergency_keywords = ["chest pain", "heart attack", "breathing issue", "stroke"]
        
        if any(kw in s_low for kw in emergency_keywords):
            return {
                "urgency": "emergency",
                "specialty": "Cardiology",
                "reasoning": "High-risk symptoms detected. Immediate emergency routing triggered."
            }

        prompt = f"Analyze these symptoms for a patient in {city}: {symptoms}"

        try:
            # 2. CALL AI
            response = client.models.generate_content(
                model="gemini-3.0-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "urgency": {"type": "string", "enum": ["emergency", "urgent", "normal"]},
                            "specialty": {"type": "string"},
                            "reasoning": {"type": "string"}
                        },
                        "required": ["urgency", "specialty", "reasoning"]
                    }
                }
            )

            # 3. ROBUST PARSING
            if response.text:
                result = json.loads(response.text)
                return {
                    "urgency": result.get("urgency", "normal"),
                    "specialty": result.get("specialty", "Internal Medicine").title(),
                    "reasoning": result.get("reasoning", "Analysis complete.")
                }

            raise ValueError("Empty response")

        except Exception as e:
            print(f"DEBUG: AI Error - {e}")
            return {
                "urgency": "normal",
                "specialty": "Internal Medicine",
                "reasoning": "System is optimizing. Please consult general medicine."
            }