#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Element Query Tool - Query elements from Universal Elements Library
"""

import sys
import os
import json
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from element_db import ElementDB


# Category mapping from framework fields to database categories
FIELD_TO_CATEGORY = {
    'styling.makeup': 'makeup_styles',
    'styling.clothing': 'clothing_styles',
    'styling.hairstyle': 'hairstyles',
    'styling.accessories': 'accessories',
    'lighting.lighting_type': 'lighting_techniques',
    'facial.eyes': 'eye_types',
    'facial.face_shape': 'face_shapes',
    'facial.nose': 'nose_types',
    'facial.lips': 'lip_types',
    'expression.facial_expression': 'expressions',
    'expression.pose': 'poses',
    'subject.ethnicity': 'ethnicities',
    'subject.age_range': 'age_ranges',
    'technical.art_style': 'art_styles',
    'technical.camera': 'camera_settings',
    'scene.atmosphere': 'atmospheres',
    'scene.environment': 'environments'
}

# Domain statistics cache
_domain_stats_cache = None


def get_db_path() -> str:
    """Get the database path."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'extracted_results', 'elements.db')


def query_elements(
    domain: str,
    category: str,
    keywords: List[str] = None,
    limit: int = 10
) -> List[Dict]:
    """
    Query elements from the Universal Elements Library.
    
    Args:
        domain: Domain ID (portrait/art/design/product/video/common)
        category: Category ID (makeup_styles/lighting_techniques/etc)
        keywords: Optional search keywords
        limit: Maximum number of results
    
    Returns:
        List of element dictionaries
    """
    db = ElementDB(get_db_path())
    
    try:
        # Query elements by domain and category
        elements = db.search_by_domain(
            domain_id=domain,
            category_id=category,
            limit=limit * 3 if keywords else limit  # Get more if filtering
        )
        
        # If keywords provided, filter and score
        if keywords and elements:
            scored_elements = []
            for elem in elements:
                score = calculate_relevance(elem, keywords)
                if score > 0:
                    elem['relevance_score'] = score
                    scored_elements.append(elem)
            
            # Sort by relevance score
            scored_elements.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            elements = scored_elements[:limit]
        
        # Format elements for output
        result = []
        for elem in elements:
            result.append({
                'element_id': elem.get('element_id'),
                'name': elem.get('name'),
                'chinese_name': elem.get('chinese_name'),
                'template': elem.get('ai_prompt_template', '')[:200],  # Truncate for readability
                'keywords': elem.get('keywords', ''),
                'reusability_score': elem.get('reusability_score', 0),
                'relevance_score': elem.get('relevance_score', 0)
            })
        
        return result
    
    finally:
        db.close()


def calculate_relevance(element: Dict, keywords: List[str]) -> float:
    """
    Calculate relevance score for an element against keywords.
    
    Args:
        element: Element dictionary
        keywords: List of search keywords
    
    Returns:
        Relevance score (0.0 - 1.0)
    """
    if not keywords:
        return 0.5
    
    # Combine searchable fields
    searchable = ' '.join([
        str(element.get('name', '')),
        str(element.get('chinese_name', '')),
        str(element.get('keywords', '')),
        str(element.get('ai_prompt_template', ''))
    ]).lower()
    
    # Count keyword matches
    matches = sum(1 for kw in keywords if kw.lower() in searchable)
    
    return matches / len(keywords)


def query_by_field(field_name: str, keywords: List[str] = None, domain: str = 'portrait', limit: int = 10) -> List[Dict]:
    """
    Query elements by framework field name.
    
    Args:
        field_name: Field name like 'styling.makeup'
        keywords: Search keywords
        domain: Domain to search in
        limit: Result limit
    
    Returns:
        List of matching elements
    """
    category = FIELD_TO_CATEGORY.get(field_name)
    if not category:
        return []
    
    return query_elements(domain, category, keywords, limit)


def get_domain_stats(domain: str = None) -> Dict:
    """
    Get statistics about the element library.
    
    Args:
        domain: Specific domain or None for all
    
    Returns:
        Statistics dictionary
    """
    global _domain_stats_cache
    
    db = ElementDB(get_db_path())
    
    try:
        stats = db.get_stats()
        
        result = {
            'total_elements': stats.get('total_elements', 0),
            'domains': {}
        }
        
        # Get domain breakdown
        if 'domains' in stats:
            for d in stats['domains']:
                if domain is None or d['domain_id'] == domain:
                    result['domains'][d['domain_id']] = {
                        'name': d.get('name', d['domain_id']),
                        'element_count': d.get('element_count', 0)
                    }
        
        return result
    
    finally:
        db.close()


def format_elements_json(elements: List[Dict]) -> str:
    """Format elements list as pretty JSON string."""
    return json.dumps(elements, ensure_ascii=False, indent=2)


def format_stats_json(stats: Dict) -> str:
    """Format stats as pretty JSON string."""
    return json.dumps(stats, ensure_ascii=False, indent=2)
