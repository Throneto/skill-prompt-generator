#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())


from mcp_server.tools.intent_parser import parse_intent
from skill_library.intelligent_generator import IntelligentGenerator

def main():
    user_request = "电影级的亚洲女性，张艺谋风格"
    print(f"用户需求: {user_request}\n")
    
    # 1. Parse Intent
    intent = parse_intent(user_request, domain_hint='portrait')
    print("📋 意图解析")
    print(f"- 主体: {intent.get('subject', {}).get('gender', 'unknown')} {intent.get('subject', {}).get('ethnicity', 'unknown')} {intent.get('subject', {}).get('age_range', 'unknown')}")
    print(f"- 风格: {intent.get('styling', {}).get('clothing', 'unknown')} + {intent.get('styling', {}).get('makeup', 'unknown')}")
    print(f"- 光影: {intent.get('lighting', {}).get('lighting_type', 'natural')}")
    print(f"- 时代: {intent.get('scene', {}).get('era', 'unknown')}")
    director = intent.get('scene', {}).get('director_style')
    if director:
        print(f"- 导演: {director}")
    print("")

    # Adapter for IntelligentGenerator
    # IntelligentGenerator expects a flatter structure than what intent_parser returns
    adapted_intent = intent.copy()
    
    # Flatten styling
    if 'styling' in intent:
        adapted_intent['clothing'] = intent['styling'].get('clothing', 'modern')
        adapted_intent['hairstyle'] = intent['styling'].get('hairstyle', 'modern')
        
    # Flatten scene/atmosphere
    if 'scene' in intent:
        adapted_intent['era'] = intent['scene'].get('era', 'modern')
        if 'director_style' in intent['scene']:
            if 'atmosphere' not in adapted_intent: adapted_intent['atmosphere'] = {}
            adapted_intent['atmosphere']['director_style'] = intent['scene']['director_style']
            
    # Flatten technical/visual_style
    if 'technical' in intent:
        if 'visual_style' not in adapted_intent: adapted_intent['visual_style'] = {}
        adapted_intent['visual_style']['art_style'] = intent['technical'].get('art_style')

    # Flatten lighting
    if 'lighting' in intent and isinstance(intent['lighting'], dict):
        adapted_intent['lighting'] = intent['lighting'].get('lighting_type', 'natural')

    # 2. Select Elements
    gen = IntelligentGenerator()
    elements = gen.select_elements_by_intent(adapted_intent)
    
    print("🎨 选用元素")
    print("| 类别 | 元素名 | 中文名 |")
    print("|---|---|---|")
    for elem in elements:
        print(f"| {elem['category']} | {elem['name']} | {elem['chinese_name']} |")
    print("")

    # 3. Check Consistency
    issues = gen.check_consistency(elements)
    print("✅ 一致性检查")
    if issues:
        print(f"发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"- {issue['description']} ({issue['suggestion']})")
        
        # Resolve conflicts
        fixed_elements, fixes = gen.resolve_conflicts(elements, issues)
        print("已自动修正:")
        for fix in fixes:
            print(fix)
        elements = fixed_elements
    else:
        print("无冲突")
    print("")

    # 4. Compose Prompt
    prompt = gen.compose_prompt(elements, mode='auto')
    
    print("✨ 最终提示词")
    print("────────────────────────────────────────")
    print(prompt)
    print("────────────────────────────────────────")

    gen.close()

if __name__ == "__main__":
    main()
