#!/usr/bin/env python3
"""
FastAPI Backend Server for AI Image Generator
Provides REST API endpoints for frontend integration
"""

import sys
import os
import json
import tempfile
import shutil
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.core.ai_image_generator import AIImageGenerator
from src.core.standard_pathway import StandardPathway
from src.core.real_products_pathway import RealProductsPathway
from config.config_settings import get_api_key, get_serpapi_key

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Generator API",
    description="Backend API for AI-powered interior design image generation",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8080"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving generated images
app.mount("/static", StaticFiles(directory="./"), name="static")

# Pydantic models for request/response
class AnalysisRequest(BaseModel):
    design_style: str
    custom_instructions: Optional[str] = ""
    design_type: str = "interior redesign"

class StandardPathwayRequest(BaseModel):
    design_style: str
    custom_instructions: Optional[str] = ""
    design_type: str = "interior redesign"

class RealProductsRequest(BaseModel):
    design_style: str
    custom_instructions: Optional[str] = ""
    design_type: str = "interior redesign"

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[Any, Any]] = None
    error: Optional[str] = None

# Global variables for API keys
openai_key = None
serpapi_key = None

@app.on_event("startup")
async def startup_event():
    """Initialize API keys on startup"""
    global openai_key, serpapi_key
    openai_key = get_api_key()
    serpapi_key = get_serpapi_key()
    
    if not openai_key:
        print("⚠️  Warning: OPENAI_API_KEY not configured")
    if not serpapi_key:
        print("⚠️  Warning: SERPAPI_KEY not configured")
    
    # Ensure directories exist
    os.makedirs("shopping_lists", exist_ok=True)
    os.makedirs("serpapi_products", exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Image Generator API",
        "status": "running",
        "openai_configured": bool(openai_key),
        "serpapi_configured": bool(serpapi_key)
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return APIResponse(
        success=True,
        message="API is healthy",
        data={
            "openai_api": "configured" if openai_key else "missing",
            "serpapi": "configured" if serpapi_key else "missing",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    design_style: str = Form(...),
    custom_instructions: str = Form(""),
    design_type: str = Form("interior redesign")
):
    """Analyze uploaded image with GPT-4o Vision"""
    
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Initialize real products pathway for analysis
        real_products_pathway = RealProductsPathway(openai_key)
        
        # Analyze the image
        analysis_results = real_products_pathway.analyze_image(
            image_path=temp_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type
        )
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not analysis_results:
            raise HTTPException(status_code=500, detail="Image analysis failed")
        
        return APIResponse(
            success=True,
            message="Image analysis completed successfully",
            data=analysis_results
        )
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/generate-standard")
async def generate_standard_pathway(
    file: UploadFile = File(...),
    design_style: str = Form(...),
    custom_instructions: str = Form(""),
    design_type: str = Form("interior redesign")
):
    """Generate design using standard pathway (AI-imagined products)"""
    
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Initialize standard pathway
        standard_pathway = StandardPathway(openai_key)
        
        # Generate design
        results = standard_pathway.generate_design(
            image_path=temp_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type
        )
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not results:
            raise HTTPException(status_code=500, detail="Standard pathway generation failed")
        
        return APIResponse(
            success=True,
            message="Standard pathway generation completed successfully",
            data=results
        )
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate-real-products")
async def generate_real_products_pathway(
    file: UploadFile = File(...),
    design_style: str = Form(...),
    custom_instructions: str = Form(""),
    design_type: str = Form("interior redesign")
):
    """Generate design using real products pathway"""
    
    if not openai_key or not serpapi_key:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key and SerpAPI key required for real products pathway"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Initialize real products pathway
        real_products_pathway = RealProductsPathway(openai_key)
        
        # Generate design with real products
        results = real_products_pathway.generate_design_with_real_products(
            image_path=temp_path,
            design_style=design_style,
            custom_instructions=custom_instructions,
            design_type=design_type,
            serpapi_key=serpapi_key
        )
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not results:
            raise HTTPException(status_code=500, detail="Real products pathway generation failed")
        
        return APIResponse(
            success=True,
            message="Real products pathway generation completed successfully",
            data=results
        )
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/shopping-lists")
async def list_shopping_lists():
    """Get list of generated shopping lists"""
    try:
        shopping_lists_dir = "shopping_lists"
        if not os.path.exists(shopping_lists_dir):
            return APIResponse(
                success=True,
                message="No shopping lists found",
                data={"shopping_lists": []}
            )
        
        files = []
        for filename in os.listdir(shopping_lists_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(shopping_lists_dir, filename)
                stat = os.stat(filepath)
                files.append({
                    "filename": filename,
                    "path": filepath,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "size": stat.st_size
                })
        
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return APIResponse(
            success=True,
            message=f"Found {len(files)} shopping lists",
            data={"shopping_lists": files}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list shopping lists: {str(e)}")

@app.get("/shopping-list/{filename}")
async def get_shopping_list(filename: str):
    """Serve a specific shopping list HTML file"""
    filepath = os.path.join("shopping_lists", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    return FileResponse(filepath, media_type="text/html")

@app.get("/images/{filepath:path}")
async def get_image(filepath: str):
    """Serve generated images"""
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(filepath)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI Image Generator API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🎯 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable auto-reload to prevent connection interruptions
        log_level="info"
    ) 