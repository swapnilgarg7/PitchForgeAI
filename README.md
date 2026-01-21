# PitchForgeAI

**PitchForgeAI** is an automated pitch-deck generator that converts a raw startup idea into a **polished, investor-ready PowerPoint presentation** using AI, Google Slides, and Google Sheets.

Unlike typical “AI slide generators” that output static or uneditable decks, PitchForgeAI produces **fully editable PPTX files** with structured layouts, live charts, and minimal, investor-style copy.

---

## What it does

- Takes a startup idea and structured metadata  
- Fills a professionally designed Google Slides template  
- Replaces semantic placeholders (`{{PROBLEM_1}}`, `{{SOLUTION_2}}`, etc.)  
- Updates **real, linked charts** via Google Sheets  
- Forces chart refresh programmatically  
- Exports a clean, editable **PowerPoint (.pptx)** file  

The result is a deck you can actually send to investors, not just look at.

---

## Why this project exists

Most AI pitch tools:
- Overfill slides with text  
- Generate static images instead of real slides  
- Break when charts are involved  
- Require manual cleanup before sharing  

PitchForgeAI treats slides as **infrastructure**, not text blobs.

The template is fixed.  
The data is dynamic.  
The output is deterministic and scalable.

---

## Key features

- Google OAuth based access (runs on the user’s Drive)  
- Google Slides API for layout-safe text replacement  
- Google Sheets API for dynamic chart updates  
- Forced chart refresh to avoid stale renders  
- Export to native, editable PPTX  
- Designed for automation and multi-user SaaS workflows  

---

## Tech stack

- Python  
- Google Slides API  
- Google Drive API  
- Google Sheets API  
- OAuth 2.0  
- Structured AI metadata (LLM-ready)  

---

## Architecture overview

1. User authenticates with Google OAuth  
2. Slides template is copied into user’s Drive  
3. Placeholders are replaced with structured content  
4. Linked Sheet data is updated for charts  
5. Charts are programmatically refreshed  
6. Deck is exported as an editable PPTX  

This separation keeps design stable and content flexible.

---

## Setup Instructions

### Prerequisites

- **Python 3.7+** installed on your system
- A **Google Cloud Project** with the following APIs enabled:
  - Google Slides API
  - Google Drive API
  - Google Sheets API
- **OAuth 2.0 credentials** from Google Cloud Console

---

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/swapnilgarg7/PitchForgeAI.git
cd PitchForgeAI
```

#### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### Google Cloud Setup

#### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Create Project** or select an existing one
3. Note your project ID

#### 2. Enable Required APIs

In your Google Cloud Project, enable these APIs:

- [Google Slides API](https://console.cloud.google.com/apis/library/slides.googleapis.com)
- [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
- [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)

#### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Configure the OAuth consent screen if prompted:
   - User Type: **External** (for testing) or **Internal** (for organization use)
   - Add your email as a test user
4. Choose **Desktop app** as the application type
5. Download the credentials JSON file
6. Save it as `oauth_credentials.json` in the project root directory

> **Security Note**: Never commit `oauth_credentials.json` to version control. It's already in `.gitignore`.

---

### Configuration

#### Option 1: Interactive Setup (Recommended)

Run the setup script:

```bash
python3 setup.py
```

This will guide you through creating your `.env` file with the required configuration.

#### Option 2: Manual Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and update the following **required** variables:

```bash
# Your Google Slides template ID (from the URL)
TEMPLATE_PRESENTATION_ID=your_template_id_here

# Your company/project information
COMPANY_NAME=Your Company Name
TAGLINE=Your compelling tagline
SUBTITLE=Your mission statement

# ... customize all other fields as needed
```

3. To find your Template Presentation ID:
   - Open your Google Slides template
   - Look at the URL: `https://docs.google.com/presentation/d/TEMPLATE_ID_HERE/edit`
   - Copy the ID between `/d/` and `/edit`

---

### Prepare Your Template

1. Create a Google Slides presentation to use as your template
2. Add placeholders using the format: `{{PLACEHOLDER_NAME}}`
   - Example: `{{COMPANY_NAME}}`, `{{PROBLEM_1}}`, `{{SOLUTION_1}}`
3. (Optional) Link Google Sheets charts for dynamic data visualization
4. Share the template with yourself or make it accessible to your Google account

See `.env.example` for all available placeholder variables.

---

### Usage

#### Run the generator

```bash
python3 generate_ppt.py
```

#### First-time authentication

On your first run:
1. A browser window will open for Google OAuth authentication
2. Sign in with your Google account
3. Grant the requested permissions
4. The credentials will be saved locally in `token.pickle`

#### Output

The script will:
- ✓ Copy your template presentation
- ✓ Replace all placeholders with your data from `.env`
- ✓ Update any linked charts with market data
- ✓ Export the final deck as `output_pitch_deck.pptx`

You'll see output like:

```
============================================================
PitchForge AI - Pitch Deck Generator
============================================================
Copying template presentation: 1XV-Zf1r...
✓ Presentation copied successfully: 1Pyp1oV...
Replacing text placeholders...
✓ Replaced 39 text placeholders
Updating market chart data...
✓ Market data updated in sheet
✓ Refreshed 1 chart(s)
Exporting presentation to output_pitch_deck.pptx...
✓ Presentation exported successfully
============================================================
✓ DONE! Your pitch deck is ready.
  File: output_pitch_deck.pptx
  Google Slides: https://docs.google.com/presentation/d/...
============================================================
```

---

### Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TEMPLATE_PRESENTATION_ID` | ✅ | Google Slides template ID | `1XV-Zf1r7Qvz...` |
| `COMPANY_NAME` | ✅ | Your company name | `MediLoop` |
| `TAGLINE` | ✅ | Company tagline | `AI powered patient follow ups` |
| `OAUTH_CREDENTIALS_PATH` | ⚪ | Path to OAuth credentials | `oauth_credentials.json` |
| `OUTPUT_FILE_NAME` | ⚪ | Output filename | `output_pitch_deck.pptx` |

See [CONFIG_TEMPLATE.md](CONFIG_TEMPLATE.md) for a complete list of all 40+ available variables.

---

### Troubleshooting

#### "Missing required environment variable" error

- Ensure you've created a `.env` file (copy from `.env.example`)
- Check that all required variables are set
- Run `python3 setup.py` for interactive configuration

#### OAuth authentication issues

- Delete `token.pickle` to force re-authentication
- Verify your `oauth_credentials.json` is valid
- Ensure all required APIs are enabled in Google Cloud Console
- Check that your Google account has access to the template

#### "No module named 'dotenv'" error

```bash
pip install -r requirements.txt
```

#### Charts not updating

- Ensure your template has linked Google Sheets charts
- Verify the `MARKET_SHEET_ID` in your `.env` file
- The script will skip chart updates if none are found (this is normal)

---

### Project Structure

```
PitchForgeAI/
├── generate_ppt.py          # Main script
├── setup.py                 # Interactive setup helper
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template (safe to commit)
├── .env                    # Your config (gitignored)
├── .gitignore              # Git ignore rules
├── CONFIG_TEMPLATE.md      # Configuration guide
├── oauth_credentials.json  # OAuth credentials (gitignored)
├── token.pickle            # Cached OAuth token (gitignored)
└── output_pitch_deck.pptx  # Generated deck (gitignored)
```

---

### Security Best Practices

✅ **DO:**
- Keep `oauth_credentials.json` and `token.pickle` private
- Use `.env` for all sensitive configuration
- Share `.env.example` with your team (without real values)
- Regularly rotate OAuth credentials
- Review Google Cloud Console for unusual API activity

❌ **DON'T:**
- Commit `.env` or `oauth_credentials.json` to version control
- Share your OAuth credentials publicly
- Hardcode sensitive data in source code
- Use production credentials for testing

---

