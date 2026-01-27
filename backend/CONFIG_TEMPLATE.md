# PitchForge AI Configuration Template
# 
# This file documents all available configuration options.
# Copy .env.example to .env and customize for your project.

## AI Configuration
# Get your API key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

## Google API Configuration
# These IDs can be found in the URLs of your Google Slides/Sheets
TEMPLATE_PRESENTATION_ID=your_template_presentation_id_here
MARKET_SHEET_ID=your_market_sheet_id_here

## OAuth Settings
# Path to your OAuth credentials JSON file from Google Cloud Console
OAUTH_CREDENTIALS_PATH=oauth_credentials.json

## Output Settings
OUTPUT_PRESENTATION_NAME=Generated Pitch Deck
OUTPUT_FILE_NAME=output_pitch_deck.pptx

## Pitch Deck Content
# Customize all the following values for your specific pitch deck

### Company Information
COMPANY_NAME=Your Company Name
TAGLINE=Your compelling tagline
SUBTITLE=Your subtitle or mission

### Problem Statements (4 key problems you're solving)
PROBLEM_1=First major problem
PROBLEM_2=Second major problem
PROBLEM_3=Third major problem
PROBLEM_4=Fourth major problem

### Key Insights (3 important insights)
INSIGHT_1=First key insight
INSIGHT_2=Second key insight
INSIGHT_3=Third key insight

### Solution Points (4 solution features)
SOLUTION_1=First solution feature
SOLUTION_2=Second solution feature
SOLUTION_3=Third solution feature
SOLUTION_4=Fourth solution feature

### Product Flow (4 steps showing how it works)
FLOW_1=First step in user flow
FLOW_2=Second step in user flow
FLOW_3=Third step in user flow
FLOW_4=Fourth step in user flow

### Market Size
# Display values (with currency symbols)
TAM_VALUE=$100B
SAM_VALUE=$50B
SOM_VALUE=$5B

# Numeric values (for charts, in billions)
TAM_NUMERIC=100
SAM_NUMERIC=50
SOM_NUMERIC=5

### Why Now (4 timing factors)
WHY_NOW_1=First market timing factor
WHY_NOW_2=Second market timing factor
WHY_NOW_3=Third market timing factor
WHY_NOW_4=Fourth market timing factor

### Business Model (3 revenue streams)
BUSINESS_MODEL_1=First revenue stream
BUSINESS_MODEL_2=Second revenue stream
BUSINESS_MODEL_3=Third revenue stream

### Go-to-Market Strategy (4 GTM tactics)
GTM_1=First GTM approach
GTM_2=Second GTM approach
GTM_3=Third GTM approach
GTM_4=Fourth GTM approach

### Competition (3 competitive advantages)
COMPETITION_1=First competitive advantage
COMPETITION_2=Second competitive advantage
COMPETITION_3=Third competitive advantage

### Risks (3 key risks and mitigations)
RISK_1=First identified risk
RISK_2=Second identified risk
RISK_3=Third identified risk

### Vision
VISION_STATEMENT=Your long-term vision statement
