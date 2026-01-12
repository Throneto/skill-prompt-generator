#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Composer Tool - Compose elements into final prompt
"""

import sys
import os
import json
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from intelligent_generator import IntelligentGenerator
except ImportError:
    IntelligentGenerator = None


# Template for manual composition when engine not available
PROMPT_TEMPLATE = """
{subject_desc}, {styling_desc}, {lighting_desc}, {technical_desc}
""".strip()


def compose_prompt(
    elements: List[Dict],
    mode: str = 'auto',
    keywords_limit: int = 3,
    subject_desc: str = ''
) -> str:
    """
    Compose elements into a final AI image prompt.
    
    Args:
        elements: List of selected elements
        mode: Composition mode (simple/auto/detailed)
        keywords_limit: Max keywords per element
        subject_desc: Optional subject description override
    
    Returns:
        Complete prompt string
    """
    # Try using the core engine
    if IntelligentGenerator:
        try:
            gen = IntelligentGenerator()
            prompt = gen.compose_prompt(elements, mode=mode, keywords_limit=keywords_limit)
            gen.close()
            return prompt
        except Exception as e:
            # Fall back to manual composition
            pass
    
    # Manual composition fallback
    return compose_prompt_manual(elements, mode, keywords_limit, subject_desc)


def compose_prompt_manual(
    elements: List[Dict],
    mode: str = 'auto',
    keywords_limit: int = 3,
    subject_desc: str = ''
) -> str:
    """
    Manual prompt composition without the core engine.
    
    Args:
        elements: List of elements
        mode: Composition mode
        keywords_limit: Keywords limit
        subject_desc: Subject description
    
    Returns:
        Composed prompt
    """
    parts = []
    
    # Group elements by category
    by_category = {}
    for elem in elements:
        cat = elem.get('category', elem.get('field_name', 'other'))
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(elem)
    
    # Subject description
    if subject_desc:
        parts.append(subject_desc)
    elif 'subject' in by_category or 'ethnicities' in by_category:
        subject_parts = []
        for elem in by_category.get('ethnicities', []) + by_category.get('subject', []):
            template = elem.get('template', elem.get('ai_prompt_template', ''))
            if template:
                subject_parts.append(extract_keywords(template, keywords_limit))
        if subject_parts:
            parts.append(', '.join(subject_parts))
    
    # Styling (makeup, clothing, hair)
    styling_cats = ['makeup_styles', 'clothing_styles', 'hairstyles', 'styling.makeup', 'styling.clothing', 'styling.hairstyle']
    styling_parts = []
    for cat in styling_cats:
        for elem in by_category.get(cat, []):
            template = elem.get('template', elem.get('ai_prompt_template', ''))
            if template:
                styling_parts.append(extract_keywords(template, keywords_limit))
    if styling_parts:
        parts.append(', '.join(styling_parts))
    
    # Lighting
    lighting_cats = ['lighting_techniques', 'lighting.lighting_type']
    lighting_parts = []
    for cat in lighting_cats:
        for elem in by_category.get(cat, []):
            template = elem.get('template', elem.get('ai_prompt_template', ''))
            if template:
                lighting_parts.append(extract_keywords(template, keywords_limit))
    if lighting_parts:
        parts.append(', '.join(lighting_parts))
    
    # Technical (art style, camera)
    tech_cats = ['art_styles', 'camera_settings', 'technical.art_style']
    tech_parts = []
    for cat in tech_cats:
        for elem in by_category.get(cat, []):
            template = elem.get('template', elem.get('ai_prompt_template', ''))
            if template:
                tech_parts.append(extract_keywords(template, keywords_limit))
    if tech_parts:
        parts.append(', '.join(tech_parts))
    
    # Quality tags
    if mode in ['auto', 'detailed']:
        parts.append('high quality, detailed, professional')
    
    # Build final prompt
    prompt = ', '.join(filter(None, parts))
    
    # Clean up
    prompt = clean_prompt(prompt)
    
    return prompt


def extract_keywords(template: str, limit: int = 3) -> str:
    """
    Extract key phrases from a template.
    
    Args:
        template: Element template text
        limit: Max phrases to extract
    
    Returns:
        Extracted keywords string
    """
    if not template:
        return ''
    
    # Split by common delimiters
    import re
    phrases = re.split(r'[,;.]', template)
    
    # Clean and limit
    cleaned = []
    for phrase in phrases[:limit]:
        phrase = phrase.strip()
        if phrase and len(phrase) > 2:
            cleaned.append(phrase)
    
    return ', '.join(cleaned)


def clean_prompt(prompt: str) -> str:
    """
    Clean up the prompt text.
    
    Args:
        prompt: Raw prompt
    
    Returns:
        Cleaned prompt
    """
    import re
    
    # Remove extra whitespace
    prompt = ' '.join(prompt.split())
    
    # Remove duplicate commas
    prompt = re.sub(r',\s*,', ',', prompt)
    
    # Remove leading/trailing commas
    prompt = prompt.strip(', ')
    
    # Capitalize first letter
    if prompt:
        prompt = prompt[0].upper() + prompt[1:]
    
    return prompt


def format_prompt_output(prompt: str, elements_used: int = 0) -> str:
    """
    Format the prompt output with metadata.
    
    Args:
        prompt: The generated prompt
        elements_used: Number of elements used
    
    Returns:
        Formatted output string
    """
    lines = [
        "✨ 生成的提示词",
        "─" * 50,
        prompt,
        "─" * 50,
        f"📊 统计: {len(prompt.split())} 词 | {elements_used} 个元素"
    ]
    return '\n'.join(lines)
