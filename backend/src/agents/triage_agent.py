from google import genai
from src.utils.config import GEMINI_API_KEY
import json

client = genai.Client(api_key=GEMINI_API_KEY)


class TriageAgent:
    def analyze(self, symptoms, city):

        prompt = f"""
You are a medical triage AI for India.

Analyze symptoms and return structured JSON.

Symptoms: {symptoms}
City: {city}
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "urgency": {
                                "type": "string",
                                "enum": ["emergency", "urgent", "normal"]
                            },
                            "specialty": {
                                "type": "string",
                                "enum": [
                                    "Cardiology", "Neurology", "Orthopedics",
                                    "ENT", "Oncology", "Dermatology",
                                    "Internal Medicine", "Pediatrics",
                                    "Psychiatry", "Gastroenterology"
                                ]
                            },
                            "reasoning": {
                                "type": "string"
                            }
                        },
                        "required": ["urgency", "specialty", "reasoning"]
                    }
                }
            )

            return response.parsed  # 🔥 THIS avoids json.loads()

        except Exception as e:
            print("Gemini Error:", str(e))
            raise Exception("Triage model failed.")