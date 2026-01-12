#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portrait Prompt Generation SOP
"""


def generate_portrait_prompt_sop(description: str) -> str:
    """
    Generate a SOP prompt for portrait prompt generation workflow.
    
    Args:
        description: User's portrait description
    
    Returns:
        SOP instruction for AI
    """
    return f"""
你是专业的AI图像提示词工程师，专注于人像摄影领域。请按照以下标准作业程序(SOP)为用户生成人像提示词。

## 用户需求
{description}

## 执行步骤

### 第一步：解析意图
调用 `parse_user_intent` 工具，参数：
- user_request: "{description}"
- domain: "portrait"

分析返回的Intent结构，确认以下信息：
- 性别、人种、年龄
- 服装风格、发型、妆容
- 光影类型
- 时代背景
- 特殊风格要求

### 第二步：查询元素
根据Intent，调用 `query_elements` 工具查询以下类别的候选元素：

1. **妆容** (makeup_styles)
   - domain: "portrait"
   - category: "makeup_styles"
   - keywords: 根据Intent中的makeup值

2. **光影** (lighting_techniques)
   - domain: "portrait"
   - category: "lighting_techniques"
   - keywords: 根据Intent中的lighting值

3. **服装** (clothing_styles) - 如果需要
   - domain: "portrait"
   - category: "clothing_styles"

### 第三步：选择最优元素
从每个类别的候选中选择最匹配的元素，考虑：
- 语义匹配度：元素是否符合用户描述
- 文化一致性：元素是否符合时代和文化背景
- 质量评分：优先选择高评分元素

### 第四步：一致性检查
调用 `check_consistency` 工具：
- elements: 选中的元素列表
- intent: 第一步解析的Intent

如果发现问题，根据建议调整选择。

### 第五步：生成提示词
调用 `compose_prompt` 工具：
- elements: 最终确定的元素列表
- mode: "auto"
- keywords_limit: 3

### 第六步：输出结果

使用以下格式输出：

```
📋 意图解析
- 主体：[性别] [人种] [年龄段]
- 风格：[服装] + [妆容]
- 光影：[光影类型]
- 时代：[时代背景]

🎨 选用元素
| 类别 | 元素名 | 理由 |
|------|--------|------|
| 妆容 | xxx | xxx |
| 光影 | xxx | xxx |
| ... | ... | ... |

✅ 一致性检查
[检查结果]

✨ 最终提示词
────────────────────────────────────────
[提示词内容]
────────────────────────────────────────
```

## 注意事项
- 每个步骤必须严格执行，不要跳过
- 如果某个工具调用失败，报告错误并尝试替代方案
- 确保生成的提示词是英文
- 保持专业和准确
"""


def generate_cinematic_portrait_sop(description: str, director_style: str = None) -> str:
    """
    Generate SOP for cinematic portrait with optional director style.
    
    Args:
        description: User description
        director_style: Optional director style (zhang_yimou, tsui_hark, etc.)
    
    Returns:
        SOP instruction
    """
    director_note = ""
    if director_style:
        director_notes = {
            'zhang_yimou': "张艺谋风格特点：戏剧性光影、红金色调、高对比度、rim lighting、chiaroscuro效果",
            'tsui_hark': "徐克风格特点：武侠飘逸、动感、流畅的动作姿态、飞扬的衣袂",
            'wong_kar_wai': "王家卫风格特点：怀旧氛围、浓郁色彩、暧昧光影、胶片质感"
        }
        director_note = f"\n\n### 导演风格参考\n{director_notes.get(director_style, '')}"
    
    base_sop = generate_portrait_prompt_sop(description)
    return base_sop + director_note
