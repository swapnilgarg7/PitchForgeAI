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
    "TAM_VALUE": "String (e.g. '$10B')",
    "SAM_VALUE": "String (e.g. '$2B')",
    "SOM_VALUE": "String (e.g. '$200M')",
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
        Dictionary with numeric values for TAM, SAM, SOM
    """
    system_prompt = """You are a Market Sizing AI.
    Output ONLY a valid JSON object with numeric values (in billions for TAM/SAM, millions for SOM, or as appropriate).
    Do not use strings, currency symbols, or suffixes. Return NUMBERS only.
    
    Required keys:
    - TAM (Total Addressable Market in Billions)
    - SAM (Serviceable Addressable Market in Billions)
    - SOM (Serviceable Obtainable Market in Billions)
    
    Example output:
    {"TAM": 10.5, "SAM": 2.1, "SOM": 0.5}
    """
    
    user_prompt = f"""
    Estimate conservative market sizes for:
    Idea: {idea}
    Region: {context.get('region', 'Global')}
    Target: {context.get('customer', 'General')}
    """
    
    from google import genai
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"TAM": 10, "SAM": 5, "SOM": 1} # Fallback
        
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=system_prompt + "\n\n" + user_prompt
        )
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error generating market data: {e}")
        return {"TAM": 10, "SAM": 5, "SOM": 1} # Fallback

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
