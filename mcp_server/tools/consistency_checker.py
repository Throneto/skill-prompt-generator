#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consistency Checker Tool - Check element combinations for consistency
"""

import json
from typing import Dict, List, Tuple


# Ethnicity to typical features mapping
ETHNICITY_FEATURES = {
    'East_Asian': {
        'typical_eye_colors': ['brown', 'dark brown', 'black'],
        'typical_hair_colors': ['black', 'dark brown'],
        'incompatible_eye_colors': ['blue', 'green', 'gray', 'hazel'],
        'incompatible_hair_colors': ['blonde', 'red', 'auburn']
    },
    'European': {
        'typical_eye_colors': ['blue', 'green', 'gray', 'brown', 'hazel'],
        'typical_hair_colors': ['blonde', 'brown', 'black', 'red', 'auburn'],
        'incompatible_eye_colors': [],
        'incompatible_hair_colors': []
    },
    'African': {
        'typical_eye_colors': ['brown', 'dark brown', 'black'],
        'typical_hair_colors': ['black', 'dark brown'],
        'incompatible_eye_colors': ['blue', 'green', 'gray'],
        'incompatible_hair_colors': ['blonde', 'red']
    }
}

# Era compatibility rules
ERA_COMPATIBILITY = {
    'ancient': {
        'compatible_lighting': ['natural', 'dramatic', 'soft', 'cinematic', 'zhang_yimou'],
        'incompatible_lighting': ['neon', 'studio_flash'],
        'compatible_clothing': ['traditional_chinese', 'kimono', 'traditional'],
        'incompatible_clothing': ['modern', 'casual', 'business']
    },
    'modern': {
        'compatible_lighting': ['natural', 'neon', 'studio', 'soft', 'dramatic', 'cinematic'],
        'incompatible_lighting': [],
        'compatible_clothing': ['modern', 'casual', 'business', 'formal'],
        'incompatible_clothing': []
    }
}


def check_consistency(elements: List[Dict], intent: Dict) -> Dict:
    """
    Check consistency of element combinations.
    
    Args:
        elements: List of selected elements
        intent: User intent structure
    
    Returns:
        Consistency report with issues and suggestions
    """
    issues = []
    suggestions = []
    
    # Extract relevant info from intent
    ethnicity = intent.get('subject', {}).get('ethnicity', 'East_Asian')
    era = intent.get('scene', {}).get('era', 'modern')
    
    # Build element lookup
    elem_by_category = {}
    for elem in elements:
        category = elem.get('category', elem.get('field_name', 'unknown'))
        elem_by_category[category] = elem
    
    # Check 1: Ethnicity vs Eye/Hair color consistency
    if ethnicity in ETHNICITY_FEATURES:
        features = ETHNICITY_FEATURES[ethnicity]
        
        # Check eye color
        eye_elem = elem_by_category.get('eye_types') or elem_by_category.get('facial.eyes')
        if eye_elem:
            eye_name = eye_elem.get('name', '').lower()
            for incompatible in features['incompatible_eye_colors']:
                if incompatible in eye_name:
                    issues.append({
                        'type': 'ethnicity_eye_mismatch',
                        'severity': 'high',
                        'description': f'Eye color "{eye_name}" is unusual for {ethnicity}',
                        'element': eye_elem.get('element_id')
                    })
                    suggestions.append({
                        'field': 'eye_color',
                        'current': eye_name,
                        'suggested': features['typical_eye_colors'][0],
                        'reason': f'{ethnicity} typically has {", ".join(features["typical_eye_colors"])} eyes'
                    })
        
        # Check hair color
        hair_elem = elem_by_category.get('hairstyles') or elem_by_category.get('styling.hairstyle')
        if hair_elem:
            hair_name = hair_elem.get('name', '').lower()
            for incompatible in features['incompatible_hair_colors']:
                if incompatible in hair_name:
                    issues.append({
                        'type': 'ethnicity_hair_mismatch',
                        'severity': 'medium',
                        'description': f'Hair color "{hair_name}" is unusual for {ethnicity}',
                        'element': hair_elem.get('element_id')
                    })
    
    # Check 2: Era vs Lighting/Clothing consistency
    if era in ERA_COMPATIBILITY:
        compat = ERA_COMPATIBILITY[era]
        
        # Check lighting
        lighting_elem = elem_by_category.get('lighting_techniques') or elem_by_category.get('lighting.lighting_type')
        if lighting_elem:
            lighting_name = lighting_elem.get('name', '').lower()
            for incompatible in compat['incompatible_lighting']:
                if incompatible in lighting_name:
                    issues.append({
                        'type': 'era_lighting_mismatch',
                        'severity': 'medium',
                        'description': f'Lighting "{lighting_name}" is anachronistic for {era} era',
                        'element': lighting_elem.get('element_id')
                    })
                    suggestions.append({
                        'field': 'lighting',
                        'current': lighting_name,
                        'suggested': compat['compatible_lighting'][0],
                        'reason': f'{era} era works better with {", ".join(compat["compatible_lighting"][:3])} lighting'
                    })
        
        # Check clothing
        clothing_elem = elem_by_category.get('clothing_styles') or elem_by_category.get('styling.clothing')
        if clothing_elem:
            clothing_name = clothing_elem.get('name', '').lower()
            for incompatible in compat['incompatible_clothing']:
                if incompatible in clothing_name:
                    issues.append({
                        'type': 'era_clothing_mismatch',
                        'severity': 'high',
                        'description': f'Clothing "{clothing_name}" is anachronistic for {era} era',
                        'element': clothing_elem.get('element_id')
                    })
    
    # Check 3: Duplicate elements
    seen_templates = {}
    for elem in elements:
        template = elem.get('template', elem.get('ai_prompt_template', ''))
        if template in seen_templates:
            issues.append({
                'type': 'duplicate',
                'severity': 'low',
                'description': f'Duplicate element template detected',
                'element': elem.get('element_id')
            })
        else:
            seen_templates[template] = elem.get('element_id')
    
    # Generate report
    report = {
        'is_consistent': len([i for i in issues if i['severity'] in ['high', 'medium']]) == 0,
        'total_issues': len(issues),
        'high_severity': len([i for i in issues if i['severity'] == 'high']),
        'medium_severity': len([i for i in issues if i['severity'] == 'medium']),
        'low_severity': len([i for i in issues if i['severity'] == 'low']),
        'issues': issues,
        'suggestions': suggestions
    }
    
    return report


def format_report(report: Dict) -> str:
    """Format consistency report as readable string."""
    lines = []
    
    if report['is_consistent']:
        lines.append("✅ 一致性检查通过")
    else:
        lines.append("⚠️ 发现一致性问题")
    
    lines.append(f"\n问题统计: 高 {report['high_severity']} | 中 {report['medium_severity']} | 低 {report['low_severity']}")
    
    if report['issues']:
        lines.append("\n问题详情:")
        for issue in report['issues']:
            severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[issue['severity']]
            lines.append(f"  {severity_icon} [{issue['type']}] {issue['description']}")
    
    if report['suggestions']:
        lines.append("\n修正建议:")
        for sug in report['suggestions']:
            lines.append(f"  • {sug['field']}: {sug['current']} → {sug['suggested']}")
            lines.append(f"    原因: {sug['reason']}")
    
    return '\n'.join(lines)


def format_report_json(report: Dict) -> str:
    """Format report as JSON string."""
    return json.dumps(report, ensure_ascii=False, indent=2)
