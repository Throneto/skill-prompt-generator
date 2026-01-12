# MCP Server for Skill Prompt Generator

基于 MCP (Model Context Protocol) 的智能 AI 图像提示词生成服务。

## 快速开始

### 1. 安装依赖

```bash
cd /data/skill-promptgenerator
python3 -m venv .venv
source .venv/bin/activate
pip install mcp pydantic
```

### 2. 启动服务器

```bash
./start_mcp.sh
# 或者
source .venv/bin/activate && python -m mcp_server.server
```

## 工具列表

| 工具名 | 功能 | 参数 |
|--------|------|------|
| `parse_user_intent` | 解析用户自然语言为结构化Intent | user_request, domain |
| `query_prompt_elements` | 查询元素库 | domain, category, keywords, limit |
| `check_element_consistency` | 检查元素一致性 | elements_json, intent_json |
| `compose_final_prompt` | 组合最终提示词 | elements_json, mode, subject_desc |
| `get_library_stats` | 获取元素库统计 | domain |

## 编排 Prompts

| Prompt 名 | 用途 |
|-----------|------|
| `portrait_prompt_generator` | 人像摄影提示词 |
| `cinematic_portrait_generator` | 电影级人像（支持导演风格）|
| `art_prompt_generator` | 艺术风格提示词 |
| `ink_wash_generator` | 中国水墨画 |
| `design_prompt_generator` | 平面设计提示词 |
| `bento_grid_generator` | Bento Grid 布局 |
| `glassmorphism_generator` | 玻璃态 UI |

## 使用示例

在 Antigravity/Claude 中：

```
请使用 portrait_prompt_generator 为我生成：电影级的亚洲女性，张艺谋风格
```

AI 会按照 SOP 依次调用工具完成提示词生成。
