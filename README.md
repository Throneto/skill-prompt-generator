# Antigravity Skills Collection

**智能 AI 多模态生成系统** — 基于 Universal Elements Library（1140+ 元素）与 NanoBanana 引擎，提供专业级图像提示词与高质量 PPT/视频生成解决方案。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

---

## 🎯 项目定位

这是一个**双模式智能提示词生成系统**，支持：

| 模式 | 平台 | 使用场景 |
|------|------|----------|
| **Claude Skills** | Claude Code | 本地开发，直接对话生成 |
| **MCP Server** | Antigravity / 任意 MCP 客户端 | 标准化服务，工作流集成 |

核心特性：
- 🧠 **语义理解**：区分主体/风格/氛围，智能推断合理属性
- 📦 **1140+ 元素库**：7 大领域（人像/艺术/设计/产品/视频/室内/通用）
- 🎨 **12 个专业 Skills**：每个领域独立专家
- 🔧 **5 个原子工具 + 7 个编排 Prompts**：MCP 标准协议
- 🍌 **NanoBanana PPT Skills**：支持智能转场与交互式播放的 AI PPT 生成引擎

---

## 📁 项目结构

```

Antigravity-Skills-Collection/
├── .claude/                          # Claude Skills 系统配置
│   ├── claude.md                     # 项目核心规则与 Prompt
│   ├── SKILL_ROUTING_GUIDE.md        # Skill 智能路由指南
│   └── skills/                       # 12 个专业领域 Skills 定义
│
├── mcp_server/                       # MCP 服务器核心代码
│   ├── server.py                     # MCP 服务入口
│   ├── tools/                        # Atomic Tools (原子工具)
│   │   ├── intent_parser.py          # 意图解析工具
│   │   ├── element_query.py          # 元素查询工具
│   │   ├── consistency_checker.py    # 一致性检查工具
│   │   ├── prompt_composer.py        # 提示词组合工具
│   │   └── ppt_skill.py              # PPT 生成 Skill (集成 NanoBanana)
│   ├── prompts/                      # Orchestration Prompts (编排提示词)
│   └── external/                     # 外部依赖仓库 (Git Submodules/Clones)
│       └── NanoBanana-PPT-Skills/    # PPT 生成核心逻辑库
│
├── skill_library/                    # 通用 Skill 核心库 (Python Package)
│   ├── __init__.py                   # 包导出定义
│   ├── intelligent_generator.py      # 智能生成引擎主体
│   ├── framework_loader.py           # YAML 框架加载器
│   ├── element_db.py                 # SQLite 数据库操作接口
│   └── constants.py                  # 系统常量定义
│
├── scripts/                          # 运维与测试脚本
│   ├── start_mcp.sh                  # MCP 服务启动脚本
│   ├── run_portrait_gen.py           # 人像生成测试
│   ├── debug_elements.py             # 元素库调试工具
│   └── patch_db.py                   # 数据库维护脚本
│
├── extracted_results/                # 数据存储
│   └── elements.db                   # Universal Elements Library 数据库
│
├── knowledge_base/                   # 知识库与文档
│   └── how_to_control_color.md       # 颜色控制指南等参考文档
│
├── prompt_framework.yaml             # 核心生成框架配置文件
├── requirements.txt                  # 项目依赖列表
└── README.md                         # 项目说明文档
```

### 📂 核心目录说明

- **`mcp_server/`**: 包含 MCP 服务器的所有实现代码。`tools/` 存放具体的工具实现，`prompts/` 存放 Prompt 模板。`external/` 目录专门用于存放拉取的**外部开源仓库**（如 PPT 生成库），保持核心代码与外部依赖分离。
- **`skill_library/`**: 封装了核心业务逻辑的 Python 包，供 MCP Server 和其他脚本调用，实现逻辑复用。
- **`scripts/`**: 存放用于开发、测试、调试和维护的辅助脚本。
- **`.claude/`**: 专为 Claude Desktop/Code 设计的配置文件夹，定义了 AI 如何使用这些工具。

---

## 🚀 快速开始

### 前置要求

- **Python 3.8+**
- **Git**（可选）

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/Throneto/Antigravity-Skills-Collection.git
cd Antigravity-Skills-Collection

# 2. 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
pip install mcp pydantic  # MCP 服务器额外依赖
```

### 配置 (Configuration)

本项目需要配置 API Key 才能使用完整功能（特别是 PPT 生成）。

1. 复制配置模板：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API Key：
   ```env
   # NanoBanana PPT 生成需要 Gemini API Key
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## 💡 使用方式

### 方式一：MCP Server（推荐 for Antigravity）


#### 启动服务器

```bash
./scripts/start_mcp.sh
# 或
source .venv/bin/activate && python -m mcp_server.server
```

#### 可用工具（Atomic Tools）

| 工具名 | 功能 | 参数 |
|--------|------|------|
| `parse_user_intent` | 解析自然语言为结构化 Intent | `user_request`, `domain` |
| `query_prompt_elements` | 查询元素库 | `domain`, `category`, `keywords`, `limit` |
| `check_element_consistency` | 检查元素一致性冲突 | `elements_json`, `intent_json` |
| `compose_final_prompt` | 组合最终提示词 | `elements_json`, `mode`, `subject_desc` |
| `get_library_stats` | 获取元素库统计 | `domain` |
| `generate_ppt` | 生成 PPT 演示文稿 | `description`, `pages`, `style`, `resolution` |

#### 编排 Prompts（Orchestration）

| Prompt | 用途 | 示例 |
|--------|------|------|
| `portrait_prompt_generator` | 人像摄影提示词 | 电影级亚洲女性 |
| `cinematic_portrait_generator` | 电影级人像（带导演风格）| 张艺谋风格人像 |
| `art_prompt_generator` | 艺术风格提示词 | 中国水墨山水 |
| `ink_wash_generator` | 中国水墨画专用 | 山水画、花鸟画 |
| `design_prompt_generator` | 平面设计提示词 | Bento Grid 布局 |
| `bento_grid_generator` | Bento Grid 专用 | 玻璃态海报 |
| `glassmorphism_generator` | 玻璃态 UI | 磨砂玻璃效果 |

#### 使用示例（在 Antigravity 中）

#### 使用示例（在 Antigravity 中）

您可以直接要求 AI 使用特定 Generator 生成内容：

```
# 1. 人像摄影 (Portrait)
请使用 portrait_prompt_generator 为我生成：侧脸微距人像，自然光

# 2. 电影级人像 (Cinematic)
请使用 cinematic_portrait_generator 为我生成：赛博朋克风格的女战士，霓虹灯光效，银翼杀手风格

# 3. 艺术绘画 (Art)
请使用 art_prompt_generator 为我生成：印象派风格的日落后的巴黎街道

# 4. 水墨画 (Ink Wash)
请使用 ink_wash_generator 为我生成：黄山云海，苍松翠柏，传统留白技法

# 5. 平面设计 (Design)
请使用 design_prompt_generator 为我生成：极简主义咖啡品牌海报

# 6. Bento Grid 布局 (Bento)
请使用 bento_grid_generator 为我生成：个人作品集网页布局，包含个人简介、项目展示和联系方式

# 7. 玻璃态设计 (Glassmorphism)
请使用 glassmorphism_generator 为我生成：带磨砂效果的信用卡 UI 组件

# 8. PPT 演示文稿 (NanoBanana)
请使用 generate_ppt 为我生成：一份关于生成式 AI 发展趋势的 PPT，共 5 页，科技感风格
```

AI 将按照 SOP 依次调用工具完成生成任务。

---

### 方式二：Claude Skills（for Claude Code）

在 Claude Code 中直接对话：

```
# 人像摄影
生成电影级的亚洲女性，张艺谋电影风格

# 平面设计
生成Bento Grid玻璃态海报

# 艺术绘画
生成中国水墨画山水
```

Claude Code 会自动识别领域并调用对应专家 Skill。

---

### 方式三：Python API（开发/调试）


```python
from skill_library.intelligent_generator import IntelligentGenerator

gen = IntelligentGenerator()

# 生成人像提示词
prompt = gen.generate_from_intent({
    'subject': {
        'gender': 'female',
        'ethnicity': 'East_Asian',
        'age_range': 'young_adult'
    },
    'styling': {
        'makeup': 'k_beauty'
    },
    'lighting': {
        'lighting_type': 'natural'
    }
})

print(prompt)
gen.close()
```

---

## 🎨 使用示例

### 示例 1：人像摄影

**输入**：
```
生成电影级的亚洲女性，张艺谋电影风格
```

**生成的提示词**：
```
Cinematic portrait of young East Asian woman, dramatic lighting with rim light
and chiaroscuro effect, Zhang Yimou's signature color palette with rich reds
and golds, 85mm lens, shallow depth of field, film grain texture...
```

### 示例 2：平面设计

**输入**：
```
生成Apple风格PPT模板
```

**输出**：完整模板系统，包括背景、布局、配色、字体、视觉效果

### 示例 3：艺术绘画

**输入**：
```
生成中国水墨画山水
```

**输出**：包含笔触、留白、泼墨等技法的专业提示词

### 示例 4：PPT 生成

**输入**：
```
生成一个关于 AI Agent 发展的 PPT，5页，玻璃态风格
```

**输出**：
- 生成 PPT 页面规划结构
- 调用 NanoBanana 引擎生成每一页的高清图片
- 返回包含图片路径和 HTML 预览器的 JSON 结果

---

## 📦 外部依赖管理

本项目采用**包含式集成**策略管理核心外部依赖。

- **存放位置**：所有第三方开源仓库源码均拉取至 `mcp_server/external/` 目录。
- **目的**：确保 Skill 能够直接调用外部库的最新功能，同时保持项目自身结构清晰。
- **示例**：PPT Skill 依赖的 `NanoBanana-PPT-Skills` 位于 `mcp_server/external/NanoBanana-PPT-Skills/`。

---

## 📊 元素库统计

| 领域 | 元素数量 | 说明 |
|------|----------|------|
| **Portrait** | 502 | 人像专用（姿势、表情、妆容等）|
| **Common** | 205 | 通用摄影技术（光影、构图等）|
| **Design** | 80 | 平面设计（布局、配色、字体等）|
| **Art** | - | 艺术风格 |
| **Product** | - | 产品摄影 |
| **Video** | - | 视频生成 |
| **Interior** | - | 室内设计 |
| **总计** | **1140+** | 持续扩充中 |

---

## 🛠️ 核心功能

### 元素库系统
- 7 大领域分类
- 复用性评分（1-10）
- SQLite 数据库存储
- 支持关键词语义搜索

### 模板系统
- 完整设计系统模板
- 包含设计理念、使用指南
- 元素结构化组织
- 支持 PPT、UI、品牌 VI 等

### 智能生成
- 框架驱动（`prompt_framework.yaml`）
- 语义匹配和推理
- 一致性检查与冲突解决
- 常识推理（如人种→眼睛颜色）

### 学习系统
- 从新提示词中提取元素
- 自动领域分类
- 复用性评分
- 持续积累知识

### PPT 智能生成 (NanoBanana)
> **NanoBanana PPT Skills** 是基于 AI 的强大演示文稿生成工具，支持自动生成高质量 PPT 图片与视频，具备智能转场和交互式播放功能。
- **多模态生成**：支持高质量 PPT 图片与动态视频生成
- **智能交互**：内置智能转场特效与交互式播放体验
- **无缝集成**：作为 MCP Tool 直接调用，支持复杂排版与渲染

---

## 📝 开发指南

### 添加新元素


```python
from skill_library.element_db import ElementDB

db = ElementDB()
db.add_element({
    'element_id': 'portrait_expressions_010',
    'domain_id': 'portrait',
    'category_id': 'expressions',
    'name': 'serene_smile',
    'chinese_name': '宁静微笑',
    'ai_prompt_template': 'serene gentle smile...',
    'keywords': '["serene", "gentle", "peaceful"]',
    'reusability_score': 8.5
})
```

### 创建新模板

```python
template = {
    'template_id': 'template_xxx',
    'name': 'Template Name',
    'chinese_name': '模板中文名',
    'category': 'ppt_design',
    'element_ids': ['elem1', 'elem2'],
    'element_structure': {
        'backgrounds': ['elem1'],
        'layouts': ['elem2']
    },
    'design_philosophy': '设计理念...',
    'usage_scenarios': '使用场景...'
}
```

---

## 📐 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                     用户层（User Layer）                      │
├──────────────────────┬──────────────────────────────────────┤
│   Claude Code        │         Antigravity / MCP Client     │
│   (自然语言对话)      │         (工具调用)                    │
├──────────────────────┴──────────────────────────────────────┤
│                   接口层（Interface Layer）                   │
├──────────────────────┬──────────────────────────────────────┤
│   Skills (12个)       │         MCP Server                   │
│   .claude/skills/    │         mcp_server/                  │
│                      │         ├─ 5 Tools                   │
│                      │         └─ 7 Prompts                 │
├──────────────────────┴──────────────────────────────────────┤
│                   引擎层（Engine Layer）                      │
│   intelligent_generator.py | framework_loader.py | element_db.py │
├─────────────────────────────────────────────────────────────┤
│                   数据层（Data Layer）                        │
│              Universal Elements Library (1140+ 元素)          │
│                    extracted_results/elements.db             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 配置

### prompt_framework.yaml

定义人像提示词的完整框架：
- **7 大类**：subject, facial, styling, expression, lighting, scene, technical
- **字段映射**：字段到数据库的精确映射
- **依赖规则**：如 `era=ancient → makeup=traditional`
- **验证规则**：确保生成结果的一致性

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献方式
1. Fork 项目
2. 创建 Feature 分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -m 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建 Pull Request

---

## 📄 License

[MIT License](LICENSE)

---

## 🙏 致谢

- [Skill Prompt Generator](https://github.com/huangserva/skill-prompt-generator) - 基于 Skills 的智能提示词生成系统
- [NanoBanana PPT Skills](https://github.com/op7418/NanoBanana-PPT-Skills) - 基于 AI 自动生成高质量 PPT 图片和视频的强大工具，支持智能转场和交互式播放
- [Claude Code](https://claude.ai/) - Skills 系统支持
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议标准
- Universal Elements Library 架构设计
- 框架驱动生成理念

---

<p align="center">
  <sub>Built with ❤️ for AI Image Generation</sub>
</p>
