#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intent Parser Tool - Parse user natural language into structured intent
"""

import json
import re
from typing import Dict, List, Optional


# Domain keywords mapping
DOMAIN_KEYWORDS = {
    'portrait': ['人像', '人物', '女性', '男性', '肖像', '女孩', '男孩', '少女', '美女', 'portrait', 'woman', 'man', 'girl'],
    'art': ['水墨', '油画', '艺术', '绘画', '国画', '山水', '静物', 'art', 'painting', 'watercolor'],
    'design': ['海报', '设计', 'UI', '布局', 'Bento', '玻璃态', 'poster', 'design', 'layout'],
    'product': ['产品', '商品', '摄影', '静物', '包装', 'product', 'commercial'],
    'video': ['视频', '镜头', '运镜', '转场', 'video', 'camera movement']
}

# Era keywords
ERA_KEYWORDS = {
    'ancient': ['古装', '古代', '汉服', '传统', '古风', '仙剑', '武侠', 'ancient', 'traditional'],
    'modern': ['现代', '时尚', '当代', 'modern', 'contemporary'],
    'republic_of_china': ['民国', '旗袍', 'republic']
}

# Lighting keywords
LIGHTING_KEYWORDS = {
    'cinematic': ['电影级', '电影', 'cinematic'],
    'natural': ['自然光', 'natural'],
    'dramatic': ['戏剧性', '戏剧', 'dramatic'],
    'neon': ['霓虹', '赛博朋克', 'neon', 'cyberpunk'],
    'soft': ['柔光', '柔和', 'soft'],
    'zhang_yimou': ['张艺谋'],
    'film_noir': ['黑色电影', 'film noir']
}

# Director style keywords
DIRECTOR_KEYWORDS = {
    'zhang_yimou': ['张艺谋'],
    'tsui_hark': ['徐克'],
    'wong_kar_wai': ['王家卫']
}

# Clothing keywords
CLOTHING_KEYWORDS = {
    'traditional_chinese': ['古装', '汉服', '传统服饰', '中式'],
    'kimono': ['和服'],
    'modern': ['现代', '时尚'],
    'business': ['职业装', '西装'],
    'casual': ['休闲'],
    'formal': ['礼服']
}

# Makeup keywords
MAKEUP_KEYWORDS = {
    'traditional_chinese': ['古风妆', '传统妆', '中式妆'],
    'traditional_japanese': ['日式妆'],
    'k_beauty': ['韩系', '韩妆'],
    'c_beauty': ['中系'],
    'natural': ['自然', '淡妆']
}


def detect_domain(text: str) -> str:
    """Detect the domain from user input text."""
    text_lower = text.lower()
    
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                scores[domain] += 1
    
    # Default to portrait if no clear match
    best_domain = max(scores, key=scores.get)
    return best_domain if scores[best_domain] > 0 else 'portrait'


def detect_value(text: str, keywords_map: Dict[str, List[str]], default: str) -> str:
    """Detect a value based on keywords mapping."""
    text_lower = text.lower()
    
    for value, keywords in keywords_map.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return value
    
    return default


def detect_gender(text: str) -> str:
    """Detect gender from text."""
    male_keywords = ['男', '男性', '男孩', '少年', 'man', 'boy', 'male']
    female_keywords = ['女', '女性', '女孩', '少女', '美女', 'woman', 'girl', 'female']
    
    text_lower = text.lower()
    
    for kw in male_keywords:
        if kw in text_lower:
            return 'male'
    
    for kw in female_keywords:
        if kw in text_lower:
            return 'female'
    
    return 'female'  # Default


def detect_ethnicity(text: str) -> str:
    """Detect ethnicity from text."""
    ethnicity_map = {
        'East_Asian': ['亚洲', '中国', '日本', '韩国', '东亚', 'asian', 'chinese', 'japanese', 'korean'],
        'European': ['欧洲', '西方', '白人', 'european', 'western', 'caucasian'],
        'African': ['非洲', '黑人', 'african'],
        'South_Asian': ['南亚', '印度', 'indian', 'south asian'],
        'Latin': ['拉丁', 'latin', 'hispanic']
    }
    
    text_lower = text.lower()
    
    for ethnicity, keywords in ethnicity_map.items():
        for kw in keywords:
            if kw in text_lower:
                return ethnicity
    
    # Default to East Asian for Chinese context
    if any(ord(c) > 127 for c in text):  # Contains non-ASCII (likely Chinese)
        return 'East_Asian'
    
    return 'East_Asian'


def detect_age_range(text: str) -> str:
    """Detect age range from text."""
    age_map = {
        'child': ['儿童', '小孩', 'child', 'kid'],
        'teen': ['少年', '青少年', 'teen', 'teenager'],
        'young_adult': ['年轻', '青年', '少女', '少年', 'young'],
        'adult': ['成年', '成人', 'adult'],
        'middle_aged': ['中年', 'middle aged'],
        'elderly': ['老年', '老人', 'elderly', 'old']
    }
    
    text_lower = text.lower()
    
    for age, keywords in age_map.items():
        for kw in keywords:
            if kw in text_lower:
                return age
    
    return 'young_adult'


def parse_intent(user_request: str, domain_hint: str = 'auto') -> Dict:
    """
    Parse user natural language request into structured intent.
    
    Args:
        user_request: The user's description
        domain_hint: Domain hint (portrait/art/design/product/video/auto)
    
    Returns:
        Structured intent dictionary
    """
    # Detect domain
    if domain_hint == 'auto':
        domain = detect_domain(user_request)
    else:
        domain = domain_hint
    
    intent = {
        'domain': domain,
        'raw_request': user_request
    }
    
    if domain == 'portrait':
        # Subject
        intent['subject'] = {
            'gender': detect_gender(user_request),
            'ethnicity': detect_ethnicity(user_request),
            'age_range': detect_age_range(user_request)
        }
        
        # Era
        era = detect_value(user_request, ERA_KEYWORDS, 'modern')
        intent['scene'] = {
            'era': era
        }
        
        # Clothing - influenced by era
        clothing = detect_value(user_request, CLOTHING_KEYWORDS, None)
        if clothing is None:
            clothing = 'traditional_chinese' if era == 'ancient' else 'modern'
        
        # Hairstyle - influenced by clothing
        hairstyle = 'ancient_chinese' if clothing == 'traditional_chinese' else 'modern'
        
        # Makeup - influenced by era and culture
        makeup = detect_value(user_request, MAKEUP_KEYWORDS, None)
        if makeup is None:
            if era == 'ancient':
                makeup = 'traditional_chinese'
            else:
                makeup = 'natural'
        
        intent['styling'] = {
            'clothing': clothing,
            'hairstyle': hairstyle,
            'makeup': makeup
        }
        
        # Lighting
        lighting = detect_value(user_request, LIGHTING_KEYWORDS, 'natural')
        intent['lighting'] = {
            'lighting_type': lighting
        }
        
        # Director style
        director = detect_value(user_request, DIRECTOR_KEYWORDS, None)
        if director:
            intent['scene']['director_style'] = director
            # Override lighting for specific directors
            if director == 'zhang_yimou':
                intent['lighting']['lighting_type'] = 'cinematic'
        
        # Art style detection
        art_styles = {
            'anime': ['动漫', '二次元', 'anime'],
            'realistic': ['写实', '真实', 'realistic'],
            'cinematic': ['电影级', '电影', 'cinematic'],
            'illustration': ['插画', 'illustration']
        }
        art_style = detect_value(user_request, art_styles, 'realistic')
        intent['technical'] = {
            'art_style': art_style
        }
    
    elif domain == 'art':
        # Art-specific parsing
        art_types = {
            'ink_wash': ['水墨', '国画', 'ink wash'],
            'oil_painting': ['油画', 'oil painting'],
            'watercolor': ['水彩', 'watercolor'],
            'sketch': ['素描', 'sketch']
        }
        intent['art_type'] = detect_value(user_request, art_types, 'ink_wash')
        
        # Subject for art
        subject_types = {
            'landscape': ['山水', '风景', 'landscape'],
            'still_life': ['静物', 'still life'],
            'abstract': ['抽象', 'abstract']
        }
        intent['subject_type'] = detect_value(user_request, subject_types, 'landscape')
    
    elif domain == 'design':
        # Design-specific parsing
        design_types = {
            'bento_grid': ['Bento', 'bento', '网格'],
            'glassmorphism': ['玻璃态', 'glassmorphism', 'glass'],
            'poster': ['海报', 'poster'],
            'ui': ['UI', 'ui', '界面']
        }
        intent['design_type'] = detect_value(user_request, design_types, 'poster')
    
    elif domain == 'product':
        # Product-specific parsing
        product_types = {
            'luxury': ['奢华', '高端', 'luxury'],
            'commercial': ['商业', 'commercial'],
            'minimal': ['极简', 'minimal']
        }
        intent['product_style'] = detect_value(user_request, product_types, 'commercial')
    
    return intent


def format_intent_json(intent: Dict) -> str:
    """Format intent as pretty JSON string."""
    return json.dumps(intent, ensure_ascii=False, indent=2)
