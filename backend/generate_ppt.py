"""
PitchForge AI - Automated Pitch Deck Generator
Generates customized pitch decks using Google Slides API and environment-based configuration.
"""

import os
import pickle
import time
from typing import Dict, Any

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from ai_generator import generate_pitch_metadata, generate_market_data

# Load environment variables from .env file
load_dotenv()

# Google API Scopes
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Token file for storing OAuth credentials
TOKEN_FILE = "token.pickle"


def get_env_variable(key: str, default: str = None) -> str:
    """
    Retrieve environment variable with error handling.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value
        
    Raises:
        ValueError: If required variable is missing and no default provided
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def authenticate_google_services():
    """
    Authenticate with Google APIs using OAuth 2.0.
    
    Returns:
        Tuple of (slides_service, drive_service, sheets_service)
    """
    creds = None
    oauth_creds_path = get_env_variable("OAUTH_CREDENTIALS_PATH", "oauth_credentials.json")
    
    # Load existing credentials from token file
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    
    # Refresh or obtain new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            if not os.path.exists(oauth_creds_path):
                raise FileNotFoundError(
                    f"OAuth credentials file not found: {oauth_creds_path}\n"
                    "Please download your OAuth credentials from Google Cloud Console."
                )
            print("Initiating OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(oauth_creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
        print("Credentials saved successfully.")
    
    # Build service clients
    slides_service = build("slides", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)
    
    return slides_service, drive_service, sheets_service


def get_user_input() -> Dict[str, Any]:
    """
    Get startup idea and context from user input.
    
    Returns:
        Dictionary with idea and context
    """
    print("\n📝 Tell us about your startup:")
    idea = input("What is your startup idea? ").strip()
    customer = input("Who is your target customer? ").strip()
    region = input("Target region (e.g., US, Global)? ").strip()
    constraints = input("Any specific constraints/focus? ").strip()
    
    return {
        "idea": idea,
        "context": {
            "customer": customer,
            "region": region,
            "constraints": constraints
        }
    }


def prepare_placeholders(generated_data: Dict[str, str]) -> Dict[str, str]:
    """
    Format generated data into placeholder format.
    
    Args:
        generated_data: Raw dictionary from LLM
        
    Returns:
        Dictionary mapping {{KEY}} to value
    """
    return {f"{{{{{key}}}}}": value for key, value in generated_data.items()}


def copy_template_presentation(drive_service, template_id: str, output_name: str) -> str:
    """
    Create a copy of the template presentation.
    
    Args:
        drive_service: Google Drive API service instance
        template_id: ID of the template presentation
        output_name: Name for the new presentation
        
    Returns:
        ID of the newly created presentation
    """
    print(f"Copying template presentation: {template_id}")
    copied = drive_service.files().copy(
        fileId=template_id,
        body={"name": output_name},
        supportsAllDrives=True
    ).execute()
    
    presentation_id = copied["id"]
    print(f"✓ Presentation copied successfully: {presentation_id}")
    return presentation_id


def replace_text_placeholders(slides_service, presentation_id: str, placeholders: Dict[str, str]):
    """
    Replace all text placeholders in the presentation.
    
    Args:
        slides_service: Google Slides API service instance
        presentation_id: ID of the presentation to update
        placeholders: Dictionary of placeholder mappings
    """
    print("Replacing text placeholders...")
    requests = []
    for key, value in placeholders.items():
        requests.append({
            "replaceAllText": {
                "containsText": {"text": key, "matchCase": True},
                "replaceText": value
            }
        })
    
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": requests}
    ).execute()
    print(f"✓ Replaced {len(placeholders)} text placeholders")


def update_market_chart(slides_service, sheets_service, presentation_id: str, market_data: Dict[str, float]):
    """
    Update the market size chart with new data.
    
    Args:
        slides_service: Google Slides API service instance
        sheets_service: Google Sheets API service instance
        presentation_id: ID of the presentation
        market_data: Dictionary with market size values
    """
    print("Updating market chart data...")
    
    # Get presentation details to find linked charts
    presentation = slides_service.presentations().get(
        presentationId=presentation_id
    ).execute()
    
    chart_object_ids = []
    linked_sheet_ids = set()
    
    # Find all linked Sheets charts
    for slide in presentation.get("slides", []):
        for element in slide.get("pageElements", []):
            if "sheetsChart" in element:
                chart_object_ids.append(element["objectId"])
                linked_sheet_ids.add(element["sheetsChart"]["spreadsheetId"])
    
    if not linked_sheet_ids:
        print("⚠ Warning: No linked Sheets charts found in presentation")
        return
    
    # Use the first linked sheet
    sheet_id = list(linked_sheet_ids)[0]
    print(f"Found linked sheet: {sheet_id}")
    
    # Get sheet metadata to find chart tab
    sheet_meta = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    
    chart_tab_name = None
    for sheet in sheet_meta["sheets"]:
        title = sheet["properties"]["title"]
        if title.startswith("[Chart"):
            chart_tab_name = title
            break
    
    # Fallback to first sheet if no chart tab found
    if not chart_tab_name:
        chart_tab_name = sheet_meta["sheets"][0]["properties"]["title"]
    
    print(f"Using chart tab: {chart_tab_name}")
    
    # Convert billions to millions for chart (format divides by 1000)
    # TAM/SAM are in billions, SOM is in billions too (0.5 = 500M)
    tam_millions = market_data.get("TAM", 150) * 1000  # 150B = 150,000M
    sam_millions = market_data.get("SAM", 25) * 1000   # 25B = 25,000M
    som_millions = market_data.get("SOM", 0.5) * 1000  # 0.5B = 500M
    
    sheet_values = [
        ["Metric", "Value"],
        ["TAM", tam_millions],
        ["SAM", sam_millions],
        ["SOM", som_millions]
    ]
    
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"'{chart_tab_name}'!A1:B4",
        valueInputOption="RAW",
        body={"values": sheet_values}
    ).execute()
    print("✓ Market data updated in sheet")
    
    # Refresh charts in presentation
    if chart_object_ids:
        refresh_requests = [
            {"refreshSheetsChart": {"objectId": chart_id}}
            for chart_id in chart_object_ids
        ]
        
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": refresh_requests}
        ).execute()
        print(f"✓ Refreshed {len(chart_object_ids)} chart(s)")
        
        # Allow time for charts to refresh
        time.sleep(2)


def export_presentation(drive_service, presentation_id: str, output_file: str):
    """
    Export the presentation as a PowerPoint file.
    
    Args:
        drive_service: Google Drive API service instance
        presentation_id: ID of the presentation to export
        output_file: Path to save the exported file
    """
    print(f"Exporting presentation to {output_file}...")
    request = drive_service.files().export_media(
        fileId=presentation_id,
        mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    
    with open(output_file, "wb") as f:
        f.write(request.execute())
    
    print(f"✓ Presentation exported successfully: {output_file}")


def generate_pitch_deck(idea: str, context: Dict[str, str]) -> str:
    """
    Orchestrates the pitch deck generation process.
    
    Args:
        idea: Startup idea description
        context: Dictionary with customer, region, and constraints
        
    Returns:
        Path to the generated PPTX file
    """
    print(f"\n🤖 Generating pitch deck for: {idea}")
    
    # 1. Generate Content with AI
    print("   Generating structured metadata...")
    generated_content = generate_pitch_metadata(idea, context)
    
    print("   Generating market data...")
    market_data = generate_market_data(idea, context)
    
    # Load configuration from environment
    template_id = get_env_variable("TEMPLATE_PRESENTATION_ID")
    output_name = f"Pitch Deck - {generated_content.get('COMPANY_NAME', 'Startup')}"
    output_filename = f"pitch_deck_{int(time.time())}.pptx"
    output_file = os.path.join(os.getcwd(), output_filename)
    
    # Authenticate with Google services
    slides_service, drive_service, sheets_service = authenticate_google_services()
    
    # Prepare placeholders
    placeholders = prepare_placeholders(generated_content)
    
    # Create presentation
    presentation_id = copy_template_presentation(drive_service, template_id, output_name)
    
    # Update content
    replace_text_placeholders(slides_service, presentation_id, placeholders)
    update_market_chart(slides_service, sheets_service, presentation_id, market_data)
    
    # Export final presentation
    export_presentation(drive_service, presentation_id, output_file)
    
    return output_file


def main():
    """Main execution function."""
    try:
        print("=" * 60)
        print("PitchForge AI - Pitch Deck Generator")
        print("=" * 60)
        
        # 1. Get User Input
        user_data = get_user_input()
        
        # 2. Generate Deck
        output_file = generate_pitch_deck(user_data["idea"], user_data["context"])
        
        print("=" * 60)
        print("✓ DONE! Your pitch deck is ready.")
        print(f"  File: {output_file}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
