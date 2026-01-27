# PitchForgeAI

**PitchForgeAI** is a full-stack AI pitch deck generator that converts a raw startup idea into a **polished, investor-ready PowerPoint presentation** using Google Gemini AI, Google Slides, and Google Sheets.

---

## ✨ Features

- 🤖 **AI-Powered Content**: Google Gemini generates structured pitch deck copy
- 📊 **Dynamic Charts**: Real-time market data (TAM/SAM/SOM) with live chart updates
- 🎨 **Modern Web UI**: Next.js frontend with dark theme
- ⚡ **FastAPI Backend**: RESTful API for deck generation
- 📥 **Editable Output**: Export to native PowerPoint (.pptx)

---

## 🏗️ Architecture

```
PitchForgeAI/
├── backend/                 # FastAPI + Python
│   ├── app.py              # API endpoints
│   ├── generate_ppt.py     # Core generation logic
│   ├── ai_generator.py     # Gemini AI integration
│   └── requirements.txt
└── frontend/               # Next.js + TypeScript
    └── app/
        ├── page.tsx        # Main UI
        └── layout.tsx
```

**Flow:**
1. User enters startup idea in web UI
2. Frontend calls `/generate` API
3. Gemini AI creates structured metadata + market data
4. Google Slides template is populated
5. Charts are updated via Google Sheets
6. PPTX file is returned for download

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 18+
- Google Cloud Project with Slides, Drive, Sheets APIs enabled
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 1. Clone & Setup Backend

```bash
git clone https://github.com/swapnilgarg7/PitchForgeAI.git
cd PitchForgeAI/backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GEMINI_API_KEY and TEMPLATE_PRESENTATION_ID
```

### 2. Setup Frontend

```bash
cd ../frontend
npm install
```

### 3. Run Both Servers

**Backend** (port 8000):
```bash
cd backend && uvicorn app:app --reload
```

**Frontend** (port 3000):
```bash
cd frontend && npm run dev
```

### 4. Generate a Deck

Open http://localhost:3000 and enter your startup idea!

---

## 🔧 Configuration

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `TEMPLATE_PRESENTATION_ID` | Google Slides template ID |

### Google Sheets Chart Format

For market data display, use this custom number format in your linked sheet:
```
$#,##0"M"
```

This displays values in millions (e.g., 500 → $500M, 25000 → $25,000M).

---

## 📡 API Reference

### POST /generate

Generate a pitch deck from a startup idea.

**Request:**
```json
{
  "idea": "Uber for dog walking",
  "customer": "Busy pet owners",
  "region": "US",
  "constraints": "Safety focus"
}
```

**Response:** Downloads `.pptx` file

### GET /health

Health check endpoint.

---

## 🛡️ Security

- ✅ Keep `oauth_credentials.json`, `token.pickle`, and `.env` private
- ✅ All sensitive files are gitignored
- ❌ Never commit API keys

---

## 📄 License

MIT
