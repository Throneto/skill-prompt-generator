#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT Skill Tool - Generates PPT images using Nano Banana Pro logic.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Optional, Any

# Add project root and external dependency to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
external_dir = os.path.join(project_root, 'mcp_server', 'external', 'NanoBanana-PPT-Skills')
sys.path.insert(0, external_dir)

try:
    from google import genai
    from google.genai import types
    # Import functions from the cloned repo
    # We need to make sure the import works. 
    # generate_ppt.py is in the root of external_dir.
    # Since we added external_dir to sys.path, we can import generate_ppt directly if it was a module,
    # but it's a script. We can import it as a module.
    import generate_ppt as nanobanana_lib
except ImportError as e:
    # Handle cases where dependencies are missing
    nanobanana_lib = None
    print(f"Warning: Failed to import dependencies: {e}")

def _get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    return genai.Client(api_key=api_key)

def _generate_plan(content: str, pages: int) -> Dict:
    """Generate the slide plan using Gemini."""
    client = _get_gemini_client()
    
    prompt = f"""
    You are a professional PPT planner.
    Based on the following content, generate a slide plan for a {pages}-page presentation.
    
    Content:
    {content}
    
    Output strictly in the following JSON format without markdown code blocks:
    {{
      "title": "Presentation Title",
      "slides": [
        {{
          "slide_number": 1,
          "page_type": "cover",
          "content": "Title and Subtitle"
        }},
        {{
          "slide_number": 2,
          "page_type": "content",
          "content": "Key point 1..."
        }},
        ...
        {{
          "slide_number": {pages},
          "page_type": "summary",
          "content": "Conclusion"
        }}
      ]
    }}
    
    Valid page_types: "cover", "content", "data", "summary".
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT'],
            temperature=0.7
        )
    )
    
    text = response.text
    # Clean up markdown if present
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    
    return json.loads(text.strip())

def generate_ppt(description: str, pages: int = 5, style: str = "gradient-glass", resolution: str = "2K") -> str:
    """
    Generates a PPT based on the description.
    
    Args:
        description: The content or topic of the presentation.
        pages: Number of slides (default 5).
        style: Style name ('gradient-glass' or 'vector-illustration').
        resolution: '2K' or '4K'.
        
    Returns:
        JSON string with result summary.
    """
    if not nanobanana_lib:
        return json.dumps({"error": "Dependency 'NanoBanana-PPT-Skills' or 'google-genai' not found."})

    try:
        # 1. Generate Plan
        print(f"Generating plan for: {description[:50]}...")
        plan = _generate_plan(description, pages)
        
        # 2. Setup Output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(external_dir, "outputs", timestamp)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        
        # 3. Resolve Style Path
        style_filename = f"{style}.md"
        style_path = os.path.join(external_dir, "styles", style_filename)
        if not os.path.exists(style_path):
            # Fallback to gradient-glass if not found
            style_path = os.path.join(external_dir, "styles", "gradient-glass.md")
        
        # Load style template using the imported function
        style_template = nanobanana_lib.load_style_template(style_path)
        
        # 4. Generate Slides
        results = []
        total_slides = len(plan['slides'])
        
        for slide in plan['slides']:
            slide_num = slide['slide_number']
            page_type = slide.get('page_type', 'content')
            content = slide['content']
            
            # Generate Prompt
            prompt = nanobanana_lib.generate_prompt(
                style_template, 
                page_type, 
                content, 
                slide_num, 
                total_slides
            )
            
            # Generate Image
            # nanobanana_lib.generate_slide returns the path or None
            # It requires GEMINI_API_KEY env var
            image_path = nanobanana_lib.generate_slide(prompt, slide_num, output_dir, resolution)
            
            results.append({
                "slide": slide_num,
                "status": "success" if image_path else "failed",
                "path": image_path
            })
            
        # 5. Generate HTML Viewer
        html_path = nanobanana_lib.generate_viewer_html(output_dir, total_slides, os.path.join(external_dir, "templates", "viewer.html"))
        
        return json.dumps({
            "status": "completed",
            "output_dir": output_dir,
            "html_viewer": html_path,
            "slides": results
        }, indent=2, ensure_ascii=False)
        
    except Exception as e:
        import traceback
        return json.dumps({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, indent=2)

if __name__ == "__main__":
    # Simple test
    print(generate_ppt("A presentation about AI Agents", pages=3))
