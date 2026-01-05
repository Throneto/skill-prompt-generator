# Skill Prompt Generator - 基于Skills的智能提示词生成系统

**一个 Claude Code Skills 项目**，通过12个专业领域Skills，基于Universal Elements Library（1140+元素）生成高质量AI图像提示词。

## 🎯 项目定位

**这不是一个普通的Python工具，而是一个完整的Skills系统：**

- 🎨 **Skills优先**：用户通过调用Skills生成提示词，不直接调用Python
- 🧠 **智能路由**：自动识别领域（人像/艺术/设计/产品/视频），调用对应专家
- 📦 **12个专业Skills**：每个领域有独立的专家Skill
- 💾 **统一数据源**：所有Skills共享Universal Elements Library（1140+元素）

## ✨ 核心特性

### 🎯 Skills系统（核心）
- **12个专业领域Skills**：intelligent-prompt-generator, art-master, design-master, product-master, video-master, universal-learner等
- **智能领域路由**：自动识别用户需求，调用对应专家
- **模块化架构**：每个Skill独立工作，协同配合

### 🧠 智能能力
- **语义理解**：区分主体/风格/氛围
- **常识推理**：自动推断合理属性（如人种→眼睛颜色）
- **一致性检查**：自动检测并修正逻辑冲突
- **框架驱动**：基于`prompt_framework.yaml`结构化生成

### 📦 双轨制系统
- **元素级生成**：从1140+个元素中智能选择组合
- **模板级生成**：完整设计系统模板（如Apple PPT模板）

### 📦 支持领域
- 📷 **portrait** - 人像摄影（502个元素）
- 🎨 **design** - 平面设计（80个元素）
- 🏠 **interior** - 室内设计
- 📦 **product** - 产品摄影
- 🎭 **art** - 艺术风格
- 🎬 **video** - 视频生成
- 📸 **common** - 通用摄影技术（205个元素）

## 📦 安装

### 前置要求

- **Claude Code** - 需要安装Claude Code CLI
- **Python 3.8+** - 用于运行底层引擎
- **Git** - 用于克隆项目（可选）

### 安装步骤

#### 方式1：克隆到本地（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/huangserva/skill-prompt-generator.git

# 2. 进入项目目录
cd skill-prompt-generator

# 3. 安装Python依赖
pip install -r requirements.txt
```

**重要**：克隆后，`.claude/skills/` 下的12个Skills会自动被Claude Code识别。

#### 方式2：下载ZIP

1. 访问 https://github.com/huangserva/skill-prompt-generator
2. 点击 "Code" → "Download ZIP"
3. 解压到任意目录
4. 在该目录下运行 `pip install -r requirements.txt`

### 验证安装

在Claude Code中测试：

```
# 测试人像生成skill
生成电影级的亚洲女性

# 测试设计skill
生成Bento Grid海报
```

如果Claude Code能正确调用Skills并生成提示词，说明安装成功。

---

## 🚀 快速开始

### 方式1：通过Skills使用（推荐）⭐

**这是主要使用方式** - 在Claude Code中直接调用Skills：

```
# 人像摄影
生成电影级的亚洲女性，张艺谋电影风格

# 平面设计
生成Bento Grid玻璃态海报

# 艺术绘画
生成中国水墨画山水

# 产品摄影
生成奢华手表产品摄影
```

Claude Code会自动：
1. 识别领域（人像/设计/艺术/产品）
2. 调用对应的专家Skill
3. 返回完美的提示词

### 方式2：直接调用Python引擎（开发/调试）

如果你想直接调用底层引擎：

```bash
# 安装依赖
pip install -r requirements.txt
```

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

**注意**：直接调用Python引擎主要用于开发和调试，日常使用建议通过Skills。

## 📖 项目结构

```
.
├── .claude/                       # ⭐ Skills系统（核心）
│   ├── CLAUDE.md                  # 项目规则和Skill路由指南
│   └── skills/                    # 12个专业领域Skills
│       ├── intelligent-prompt-generator/  # 人像提示词专家
│       ├── art-master/            # 艺术风格专家
│       ├── design-master/         # 平面设计专家
│       ├── product-master/        # 产品摄影专家
│       ├── video-master/          # 视频生成专家
│       ├── universal-learner/     # 学习系统
│       ├── prompt-analyzer/       # 提示词分析
│       ├── prompt-extractor/      # 元素提取
│       ├── prompt-generator/      # 通用生成器
│       ├── prompt-master/         # 主控调度
│       ├── prompt-xray/           # X-Ray分析
│       └── domain-classifier/     # 领域分类
│
├── intelligent_generator.py       # Python引擎：核心生成
├── framework_loader.py            # Python引擎：框架加载
├── element_db.py                  # Python引擎：数据库操作
├── prompt_framework.yaml          # 人像框架定义
│
├── extracted_results/
│   └── elements.db                # Universal Elements Library (1140+元素)
│
├── requirements.txt               # Python依赖
└── README.md                      # 项目文档
```

**架构说明**：
- **用户层**：通过Claude Code调用Skills
- **Skills层**：12个专业领域专家（.claude/skills/）
- **引擎层**：Python引擎支持Skills运行
- **数据层**：Universal Elements Library（1140+元素）

## 🎨 使用示例

### 示例1：人像摄影（intelligent-prompt-generator skill）

**用户请求**：
```
生成电影级的亚洲女性，张艺谋电影风格
```

**Skill自动处理**：
- 识别：人像摄影领域
- 调用：intelligent-prompt-generator skill
- 生成：电影级人像提示词，包含戏剧性光影

**输出提示词**：
```
Cinematic portrait of young East Asian woman, dramatic lighting with rim light
and chiaroscuro effect, Zhang Yimou's signature color palette with rich reds
and golds, 85mm lens, shallow depth of field, film grain texture...
```

### 示例2：平面设计（design-master skill）

**用户请求**：
```
生成Apple风格PPT模板
```

**Skill自动处理**：
- 识别：平面设计领域
- 调用：design-master skill
- 查询：Apple淡蓝商务PPT模板（12个元素完整系统）

**输出**：完整模板系统，包括背景、布局、配色、字体、视觉效果

### 示例3：艺术绘画（art-master skill）

**用户请求**：
```
生成中国水墨画山水
```

**Skill自动处理**：
- 识别：艺术绘画领域（无人物）
- 调用：art-master skill
- 生成：包含笔触、留白、泼墨等技法的提示词

### 示例4：产品摄影（product-master skill）

**用户请求**：
```
生成奢华手表产品摄影
```

**Skill自动处理**：
- 识别：产品摄影领域
- 调用：product-master skill
- 生成：商业级产品摄影提示词

## 🛠️ 核心功能

### 1. 元素库系统
- **1140+个可复用元素**
- 7大领域分类
- 复用性评分（1-10）
- SQLite数据库存储

### 2. 模板系统
- 完整设计系统保存
- 包含设计理念、使用指南
- 元素结构化组织
- 支持PPT、UI、品牌VI等

### 3. 智能生成
- 框架驱动（`prompt_framework.yaml`）
- 语义匹配和推理
- 一致性检查
- 自动冲突解决

### 4. 学习系统
- 从新提示词中提取元素
- 自动领域分类
- 复用性评分
- 持续积累知识

## 📊 数据库统计

- **总元素数**: 1140+
- **Portrait领域**: 502个（人像专用）
- **Design领域**: 80个（平面设计）
- **Common领域**: 205个（通用技术）
- **模板数**: 1个（Apple淡蓝商务PPT）

## 🔧 配置

### prompt_framework.yaml

定义人像提示词的完整框架：
- 7大类：subject, facial, styling, expression, lighting, scene, technical
- 字段到数据库的映射
- 依赖规则（如era=ancient → makeup=traditional）
- 验证规则

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
    'element_ids': ['elem1', 'elem2', ...],
    'element_structure': {
        'backgrounds': ['elem1'],
        'layouts': ['elem2']
    },
    'design_philosophy': '设计理念...',
    'usage_scenarios': '使用场景...'
}
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

MIT License

## 🙏 致谢

- 基于Claude Code Skills系统
- Universal Elements Library架构
- 框架驱动生成理念
