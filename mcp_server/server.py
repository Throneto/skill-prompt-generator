#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for Skill Prompt Generator

A Model Context Protocol server that provides atomic tools and prompts
for intelligent AI image prompt generation.

Usage:
    python -m mcp_server.server
    
    Or with uvx:
    uvx mcp run python -m mcp_server.server
"""

import sys
import os
import json
from typing import Optional

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from mcp.server.fastmcp import FastMCP

# Import tools
from mcp_server.tools.intent_parser import parse_intent, format_intent_json
from mcp_server.tools.element_query import (
    query_elements, 
    query_by_field, 
    get_domain_stats,
    format_elements_json,
    format_stats_json
)
from mcp_server.tools.consistency_checker import check_consistency, format_report, format_report_json
from mcp_server.tools.prompt_composer import compose_prompt, format_prompt_output
from mcp_server.tools.ppt_skill import generate_ppt

# Import prompts
from mcp_server.prompts.portrait import generate_portrait_prompt_sop, generate_cinematic_portrait_sop
from mcp_server.prompts.art import generate_art_prompt_sop, generate_ink_wash_sop
from mcp_server.prompts.design import generate_design_prompt_sop, generate_bento_grid_sop, generate_glassmorphism_sop


# Initialize MCP Server
mcp = FastMCP(
    name="SkillPromptGenerator",
    instructions="智能AI图像提示词生成器 - 基于1140+元素的专业提示词生成系统"
)


# ============================================================
# Atomic Tools
# ============================================================

@mcp.tool()
def parse_user_intent(user_request: str, domain: str = "auto") -> str:
    """
    解析用户的自然语言描述，提取结构化的生成意图。
    
    这是工作流的第一步，用于理解用户需求。
    
    Args:
        user_request: 用户的描述，如"电影级的亚洲女性，张艺谋风格"
        domain: 领域提示 (portrait/art/design/product/video/auto)
    
    Returns:
        JSON格式的Intent结构，包含主体、风格、光影等信息
    
    Example:
        parse_user_intent("生成电影级的亚洲女性，张艺谋风格")
    """
    intent = parse_intent(user_request, domain)
    return format_intent_json(intent)


@mcp.tool()
def query_prompt_elements(
    domain: str,
    category: str,
    keywords: str = "",
    limit: int = 10
) -> str:
    """
    从Universal Elements Library（1140+元素）查询匹配的元素。
    
    这是工作流的第二步，用于获取候选元素。
    
    Args:
        domain: 领域 (portrait/art/design/product/video/common)
        category: 类别 (makeup_styles/lighting_techniques/clothing_styles等)
        keywords: 搜索关键词，用逗号分隔，如"traditional,chinese"
        limit: 返回数量限制，默认10
    
    Returns:
        JSON格式的候选元素列表，每个元素包含ID、名称、模板、评分等
    
    Example:
        query_prompt_elements("portrait", "makeup_styles", "traditional,chinese", 5)
    """
    kw_list = [k.strip() for k in keywords.split(',')] if keywords else None
    elements = query_elements(domain, category, kw_list, limit)
    return format_elements_json(elements)


@mcp.tool()
def check_element_consistency(elements_json: str, intent_json: str) -> str:
    """
    检查元素组合的一致性，识别冲突并提供修正建议。
    
    这是工作流的第三步，用于验证选择的元素是否协调。
    
    Args:
        elements_json: 已选择的元素列表，JSON格式
        intent_json: 用户意图结构，JSON格式（来自parse_user_intent）
    
    Returns:
        一致性报告，包含问题数量、严重程度、具体问题和修正建议
    
    Example:
        check_element_consistency('[{"element_id":"..."}]', '{"subject":{"ethnicity":"East_Asian"}}')
    """
    try:
        elements = json.loads(elements_json)
        intent = json.loads(intent_json)
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {e}"
    
    report = check_consistency(elements, intent)
    return format_report(report)


@mcp.tool()
def compose_final_prompt(
    elements_json: str,
    mode: str = "auto",
    subject_desc: str = ""
) -> str:
    """
    将选中的元素组合成完整的AI图像提示词。
    
    这是工作流的最后一步，生成可直接使用的提示词。
    
    Args:
        elements_json: 元素列表，JSON格式
        mode: 组合模式 (simple/auto/detailed)，默认auto
        subject_desc: 可选的主体描述覆盖，如"A young woman"
    
    Returns:
        完整的英文AI图像提示词
    
    Example:
        compose_final_prompt('[{"template":"cinematic lighting..."}]', "auto")
    """
    try:
        elements = json.loads(elements_json)
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {e}"
    
    prompt = compose_prompt(elements, mode=mode, subject_desc=subject_desc)
    return format_prompt_output(prompt, len(elements))


@mcp.tool()
def get_library_stats(domain: str = "") -> str:
    """
    获取元素库的统计信息，帮助了解可用资源。
    
    辅助工具，用于了解各领域的元素数量和分布。
    
    Args:
        domain: 特定领域（留空返回全部统计）
    
    Returns:
        JSON格式的统计信息，包含总元素数和各领域分布
    
    Example:
        get_library_stats("portrait")
    """
    stats = get_domain_stats(domain if domain else None)
    return format_stats_json(stats)


@mcp.tool()
def nanobanana_ppt_generator(
    description: str, 
    pages: int = 5, 
    style: str = "gradient-glass", 
    resolution: str = "2K"
) -> str:
    """
    Generate professional PPT images using Nano Banana Pro.
    
    Automatically plans the slide structure based on the description/content,
    then generates high-quality images using Gemini and predefined styles.
    
    Args:
        description: The topic or content of the presentation.
        pages: Number of slides (default: 5).
        style: Visual style ('gradient-glass' or 'vector-illustration').
        resolution: Image resolution ('2K' or '4K').
        
    Returns:
        JSON string containing the output directory and slide details.
    """
    return generate_ppt(description, pages, style, resolution)


# ============================================================
# Orchestration Prompts
# ============================================================

@mcp.prompt()
def portrait_prompt_generator(description: str) -> str:
    """
    人像摄影提示词生成工作流。
    
    按照标准SOP生成专业的人像摄影AI提示词。
    包含意图解析、元素查询、一致性检查、提示词组合等完整流程。
    
    Args:
        description: 人像描述，如"电影级的亚洲女性，张艺谋风格"
    """
    return generate_portrait_prompt_sop(description)


@mcp.prompt()
def cinematic_portrait_generator(description: str, director: str = "") -> str:
    """
    电影级人像提示词生成工作流（支持导演风格）。
    
    专为电影级人像设计，支持张艺谋、徐克、王家卫等导演风格。
    
    Args:
        description: 人像描述
        director: 导演风格 (zhang_yimou/tsui_hark/wong_kar_wai)
    """
    return generate_cinematic_portrait_sop(description, director if director else None)


@mcp.prompt()
def art_prompt_generator(description: str) -> str:
    """
    艺术风格提示词生成工作流。
    
    按照标准SOP生成艺术绘画类AI提示词。
    支持水墨画、油画、水彩等多种艺术形式。
    
    Args:
        description: 艺术作品描述，如"中国水墨画山水"
    """
    return generate_art_prompt_sop(description)


@mcp.prompt()
def ink_wash_generator(description: str) -> str:
    """
    中国水墨画提示词生成工作流。
    
    专为中国水墨画设计，包含专业术语（笔触、墨法、留白等）。
    
    Args:
        description: 水墨画描述
    """
    return generate_ink_wash_sop(description)


@mcp.prompt()
def design_prompt_generator(description: str) -> str:
    """
    平面设计提示词生成工作流。
    
    按照标准SOP生成设计类AI提示词。
    支持海报、UI、Bento Grid等多种设计形式。
    
    Args:
        description: 设计描述，如"Bento Grid玻璃态海报"
    """
    return generate_design_prompt_sop(description)


@mcp.prompt()
def bento_grid_generator(description: str) -> str:
    """
    Bento Grid设计提示词生成工作流。
    
    专为Bento Grid布局设计。
    
    Args:
        description: Bento Grid设计描述
    """
    return generate_bento_grid_sop(description)


@mcp.prompt()
def glassmorphism_generator(description: str) -> str:
    """
    玻璃态（Glassmorphism）设计提示词生成工作流。
    
    专为玻璃态UI设计。
    
    Args:
        description: 玻璃态设计描述
    """
    return generate_glassmorphism_sop(description)


# ============================================================
# Resources (Optional - Database access)
# ============================================================

@mcp.resource("elements://stats")
def resource_stats() -> str:
    """获取元素库统计信息"""
    stats = get_domain_stats()
    return format_stats_json(stats)


# ============================================================
# Entry Point
# ============================================================

def main():
    """Run the MCP server."""
    print("Starting Skill Prompt Generator MCP Server...")
    print(f"Project root: {PROJECT_ROOT}")
    print("Tools: parse_user_intent, query_prompt_elements, check_element_consistency, compose_final_prompt, get_library_stats")
    print("Prompts: portrait_prompt_generator, art_prompt_generator, design_prompt_generator, ...")
    mcp.run()


if __name__ == "__main__":
    main()
