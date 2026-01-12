#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Art Prompt Generation SOP
"""


def generate_art_prompt_sop(description: str) -> str:
    """
    Generate a SOP prompt for art style prompt generation.
    
    Args:
        description: User's art description
    
    Returns:
        SOP instruction for AI
    """
    return f"""
你是专业的AI图像提示词工程师，专注于艺术绘画领域。请按照以下SOP生成艺术风格提示词。

## 用户需求
{description}

## 执行步骤

### 第一步：解析意图
调用 `parse_user_intent` 工具：
- user_request: "{description}"
- domain: "art"

识别：
- 艺术类型（水墨、油画、水彩等）
- 主题（山水、静物、抽象等）
- 技法要求（笔触、留白、泼墨等）

### 第二步：查询元素
调用 `query_elements` 查询 art 领域的元素：
- domain: "art"
- category: 根据艺术类型选择

常用类别：
- "ink_wash_techniques" (水墨技法)
- "oil_painting_styles" (油画风格)
- "artistic_compositions" (艺术构图)

### 第三步：选择元素
从候选中选择最匹配的元素，优先考虑：
- 艺术流派的专业术语
- 技法描述的准确性
- 氛围和意境的表达

### 第四步：生成提示词
调用 `compose_prompt` 组合元素。

### 第五步：输出结果

```
🎨 艺术风格解析
- 类型：[艺术类型]
- 主题：[主题描述]
- 技法：[技法要求]

✨ 最终提示词
────────────────────────────────────────
[提示词内容]
────────────────────────────────────────
```
"""


def generate_ink_wash_sop(description: str) -> str:
    """
    Specialized SOP for Chinese ink wash painting.
    """
    return f"""
你是中国水墨画提示词专家。请生成专业的水墨画AI提示词。

## 用户需求
{description}

## 水墨画专业术语参考
- 笔触：皴法（披麻皴、斧劈皴）、点苔、勾勒
- 留白：计白当黑、虚实相生
- 墨法：浓墨、淡墨、焦墨、泼墨、破墨
- 意境：空灵、悠远、淡雅、苍茫

## 执行步骤

1. 调用 `parse_user_intent` 解析需求
2. 调用 `query_elements` 查询 art 领域水墨相关元素
3. 确保包含笔触、墨法、构图、意境等元素
4. 调用 `compose_prompt` 生成提示词

## 输出格式

```
🖌️ 水墨画提示词
────────────────────────────────────────
[包含专业术语的提示词]
────────────────────────────────────────
```
"""
