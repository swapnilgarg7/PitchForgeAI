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

