from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from generate_ppt import generate_pitch_deck

app = FastAPI(
    title="PitchForge AI API",
    description="Generate investor-ready pitch decks using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PitchRequest(BaseModel):
    idea: str
    customer: str = "General"
    region: str = "Global"
    constraints: str = "None"

@app.post("/generate", summary="Generate a pitch deck")
async def generate_deck(request: PitchRequest, background_tasks: BackgroundTasks):
    """
    Generate a pitch deck based on the provided startup idea and context.
    Returns the generated PPTX file.
    """
    try:
        context = {
            "customer": request.customer,
            "region": request.region,
            "constraints": request.constraints
        }
        
        # Generate the deck
        output_file = generate_pitch_deck(request.idea, context)
        
        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="Failed to generate pitch deck file")
            
        # Schedule file cleanup after response is sent (optional, but good practice)
        # background_tasks.add_task(os.remove, output_file)
        
        filename = os.path.basename(output_file)
        
        return FileResponse(
            path=output_file,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
