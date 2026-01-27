import os
import json
from typing import Dict, Any, Optional

# =============================================================================
# 1. SYSTEM PROMPT
# =============================================================================

PITCH_DECK_SCHEMA = {
    "COMPANY_NAME": "String",
    "TAGLINE": "String (max 8 words)",
    "SUBTITLE": "String (max 8 words)",
    "PROBLEM_1": "String (max 8 words)",
    "PROBLEM_2": "String (max 8 words)",
    "PROBLEM_3": "String (max 8 words)",
    "PROBLEM_4": "String (max 8 words)",
    "INSIGHT_1": "String (max 8 words)",
    "INSIGHT_2": "String (max 8 words)",
    "INSIGHT_3": "String (max 8 words)",
    "SOLUTION_1": "String (max 8 words)",
    "SOLUTION_2": "String (max 8 words)",
    "SOLUTION_3": "String (max 8 words)",
    "SOLUTION_4": "String (max 8 words)",
    "FLOW_1": "String (max 8 words)",
    "FLOW_2": "String (max 8 words)",
    "FLOW_3": "String (max 8 words)",
    "FLOW_4": "String (max 8 words)",
    "TAM_VALUE": "String with $ and B/M suffix (e.g. '$150B', '$50B'). Must include B for billions or M for millions.",
    "SAM_VALUE": "String with $ and B/M suffix (e.g. '$25B', '$10B'). Must include B for billions or M for millions.",
    "SOM_VALUE": "String with $ and M suffix (e.g. '$500M', '$100M'). Must include M for millions.",
    "WHY_NOW_1": "String (max 8 words)",
    "WHY_NOW_2": "String (max 8 words)",
    "WHY_NOW_3": "String (max 8 words)",
    "WHY_NOW_4": "String (max 8 words)",
    "BUSINESS_MODEL_1": "String (max 8 words)",
    "BUSINESS_MODEL_2": "String (max 8 words)",
    "BUSINESS_MODEL_3": "String (max 8 words)",
    "GTM_1": "String (max 8 words)",
    "GTM_2": "String (max 8 words)",
    "GTM_3": "String (max 8 words)",
    "GTM_4": "String (max 8 words)",
    "COMPETITION_1": "String (max 8 words)",
    "COMPETITION_2": "String (max 8 words)",
    "COMPETITION_3": "String (max 8 words)",
    "RISK_1": "String (max 8 words)",
    "RISK_2": "String (max 8 words)",
    "RISK_3": "String (max 8 words)",
    "VISION_STATEMENT": "String (max 12 words)"
}

SYSTEM_PROMPT = f"""You are a specialized Pitch Deck Metadata Generator.
Your ONLY job is to generate structured JSON data for a startup pitch deck based on a provided idea.

RULES:
1. Output ONLY valid JSON. No markdown formatting, no code blocks, no introductory text, no explanations.
2. The output must be a single flat JSON object.
3. Keys must EXACTLY match the provided schema.
4. Do NOT include any keys not present in the schema.
5. All values must be strings.
6. Enforce concise, investor-style language:
   - Bullet points: MAX 8 words.
   - Vision statement: MAX 12 words.
   - Be punchy, direct, and professional. Avoid fluff.
7. If you violate the format or schema, you have FAILED.

SCHEMA:
{json.dumps(PITCH_DECK_SCHEMA, indent=2)}
"""

# =============================================================================
# 2. USER PROMPT TEMPLATE
# =============================================================================

USER_PROMPT_TEMPLATE = """
Generate pitch deck metadata for the following startup idea.
Fill the schema conservatively and realistically.

STARTUP IDEA:
{idea}

TARGET CUSTOMER:
{customer}

REGION:
{region}

ADDITIONAL CONSTRAINTS:
{constraints}
"""

# =============================================================================
# 3. GENERATION FUNCTION
# =============================================================================

def generate_pitch_metadata(idea: str, context: Dict[str, Any]) -> str:
    """
    Calls an LLM API to generate pitch deck metadata.
    
    Args:
        idea: The core startup idea description.
        context: Dictionary containing 'customer', 'region', and optional 'constraints'.
        
    Returns:
        Raw text output from the LLM (expected to be JSON).
    """
    
    # Construct the full user prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        idea=idea,
        customer=context.get("customer", "General"),
        region=context.get("region", "Global"),
        constraints=context.get("constraints", "None")
    )
    
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # LLM API CALL
    from google import genai
    from dotenv import load_dotenv  
    load_dotenv() 
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=SYSTEM_PROMPT + "\n\n" + user_prompt
        )
        # Clean up response if it contains markdown code blocks
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {}


def generate_market_data(idea: str, context: Dict[str, Any]) -> Dict[str, float]:
    """
    Generates numeric market size data (TAM, SAM, SOM).
    
    Args:
        idea: Startup idea
        context: Context dictionary
        
    Returns:
        Dictionary with numeric values for TAM, SAM, SOM (in billions)
    """
    system_prompt = """You are a Market Sizing AI for startup pitch decks.
    Output ONLY a valid JSON object with realistic market size estimates.
    Values should be in BILLIONS of dollars (e.g., 50 means $50 billion).
    
    Guidelines:
    - TAM (Total Addressable Market): The entire global market opportunity. Usually $10B-$500B+
    - SAM (Serviceable Addressable Market): The segment you can realistically target. Usually 10-30% of TAM.
    - SOM (Serviceable Obtainable Market): What you can capture in 3-5 years. Usually 1-5% of SAM.
    
    Return NUMBERS ONLY (no strings, no $, no 'B').
    
    Example output for a B2B SaaS:
    {"TAM": 150, "SAM": 25, "SOM": 0.5}
    """
    
    user_prompt = f"""
    Estimate realistic market sizes for this startup:
    Idea: {idea}
    Region: {context.get('region', 'Global')}
    Target Customer: {context.get('customer', 'General')}
    
    Research the actual market and provide realistic numbers in billions.
    """
    
    from google import genai
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"TAM": 150, "SAM": 25, "SOM": 0.5}  # Realistic fallback
        
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=system_prompt + "\n\n" + user_prompt
        )
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error generating market data: {e}")
        return {"TAM": 150, "SAM": 25, "SOM": 0.5}  # Realistic fallback

if __name__ == "__main__":
    # Simple test
    test_context = {
        "customer": "Remote Doctors",
        "region": "North America",
        "constraints": "Focus on AI efficiency"
    }
    print("Testing Metadata Generation...")
    meta = generate_pitch_metadata("Uber for Doctors", test_context)
    print(json.dumps(meta, indent=2))
    
    print("\nTesting Market Data Generation...")
    market = generate_market_data("Uber for Doctors", test_context)
    print(json.dumps(market, indent=2))
