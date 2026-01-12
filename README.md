# Skill Prompt Generator

**智能 AI 图像提示词生成系统** — 基于 Universal Elements Library（1140+ 元素）的专业级提示词生成解决方案。

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

---

## 📁 项目结构

```
skill-prompt-generator/
├── .claude/                          # Claude Skills 系统
│   ├── claude.md                     # 项目规则
│   ├── SKILL_ROUTING_GUIDE.md        # Skill 路由指南
│   └── skills/                       # 12 个专业领域 Skills
│       ├── intelligent-prompt-generator/  # 人像提示词专家
│       ├── art-master/               # 艺术风格专家
│       ├── design-master/            # 平面设计专家
│       ├── product-master/           # 产品摄影专家
│       ├── video-master/             # 视频生成专家
│       └── ...                       # 其他 Skills
│
├── mcp_server/                       # MCP 服务器
│   ├── server.py                     # 主服务入口
│   ├── tools/                        # 5 个原子工具
│   │   ├── intent_parser.py          # 意图解析
│   │   ├── element_query.py          # 元素查询
│   │   ├── consistency_checker.py    # 一致性检查
│   │   └── prompt_composer.py        # 提示词组合
│   ├── prompts/                      # 编排 Prompts
│   │   ├── portrait.py               # 人像摄影工作流
│   │   ├── art.py                    # 艺术风格工作流
│   │   └── design.py                 # 平面设计工作流
│   └── README.md                     # MCP 服务器文档
│
├── intelligent_generator.py          # Python 核心引擎
├── framework_loader.py               # 框架加载器
├── element_db.py                     # 数据库操作
├── prompt_framework.yaml             # 人像框架定义
│
├── extracted_results/
│   └── elements.db                   # SQLite 元素库 (1140+ 元素)
│
├── knowledge_base/                   # 知识库
├── start_mcp.sh                      # MCP 启动脚本
├── requirements.txt                  # Python 依赖
└── README.md                         # 本文档
```

---

## 🚀 快速开始

### 前置要求

- **Python 3.8+**
- **Git**（可选）

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/huangserva/skill-prompt-generator.git
cd skill-prompt-generator

# 2. 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
pip install mcp pydantic  # MCP 服务器额外依赖
```

---

## 💡 使用方式

### 方式一：MCP Server（推荐 for Antigravity）

#### 启动服务器

```bash
./start_mcp.sh
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

```
请使用 portrait_prompt_generator 为我生成：电影级的亚洲女性，张艺谋风格
```

AI 将按照 SOP 依次调用工具完成提示词生成。

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
from intelligent_generator import IntelligentGenerator

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

---

## 📝 开发指南

### 添加新元素

```python
from element_db import ElementDatabase

db = ElementDatabase()
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

- [Claude Code](https://claude.ai/) - Skills 系统支持
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议标准
- Universal Elements Library 架构设计
- 框架驱动生成理念

---

<p align="center">
  <sub>Built with ❤️ for AI Image Generation</sub>
</p>
