# 职业教育教学能力比赛专家系统

基于 opencode 的三Agent辩论式专家系统，为职业教育教学能力比赛提供备赛指导。

## 架构

```
用户提问
  ↓
┌─────────────────────────────────┐
│  jingsai-coach (主Agent/实战教练)  │
│  生成建议 → 派发审校 → 综合输出    │
└──────────┬──────────┬───────────┘
           │          │
     ┌─────▼──┐  ┌───▼───────┐
     │ reviewer│  │   judge   │
     │(政策审查)│  │(评委视角)  │
     └─────┬──┘  └───┬───────┘
           │          │
           ▼          ▼
     主Agent综合反馈 → 最终输出
```

- **jingsai-coach**：进取型思维，生成实操建议并直接修改文档
- **jingsai-reviewer**：防御型思维，核查政策合规性和事实准确性
- **jingsai-judge**：挑刺型思维，模拟评委视角找扣分风险

## 快速部署

### 前置条件

- Python 3.8+
- [opencode](https://opencode.ai) CLI
- 一个LLM Provider的API Key（支持Anthropic/OpenAI/智谱等）

### 步骤

```bash
# 1. 克隆仓库
git clone <repo-url> jingsai-expert-system
cd jingsai-expert-system

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 配置Provider
# 编辑 opencode.json，填入你的provider配置
# 或者使用全局 ~/.config/opencode/opencode.json 中的provider

# 4.（可选）放入知识原子
# 将264个知识原子.md文件放入 knowledge-base/ 的三个子目录
# 如果没有知识原子，系统仍可运行（但建议质量会降低）

# 5. 启动opencode
opencode
```

### 配置Provider

编辑 `opencode.json` 中的 `provider` 和 `model` 字段：

```json
{
  "provider": {
    "anthropic": {
      "options": { "apiKey": "your-key" }
    }
  },
  "model": "anthropic/claude-sonnet-4-6"
}
```

支持的provider格式：`<provider>/<model-id>`

## 支持的场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 文档指导+修改 | .docx 文件 | 指导建议 + 直接修改文档 |
| PPT指导+修改 | .pptx 文件 | 指导建议 + 直接修改幻灯片 |
| 架构图绘制 | 图片/文本描述 | SVG/PNG架构图 |
| 知识问答 | 自然语言问题 | 基于知识库的回答（不足时联网搜索） |

## 知识库

`knowledge-base/` 目录包含264个知识原子（.md文件），分为三类：

| 目录 | 内容 | 数量 |
|------|------|------|
| `方法论/` | 教学设计方法、比赛策略、操作流程 | ~139 |
| `资源/` | 术语库、案例集、工具推荐 | ~43 |
| `标准/` | 评分标准、检查清单、规范要求 | ~82 |

每个原子遵循统一格式：YAML元数据 + 问题段 + 核心内容段 + 参考段。

## 工具脚本

位于 `.opencode/skills/jingsai-tools/scripts/`：

| 脚本 | 功能 | 用法 |
|------|------|------|
| `docx_read.py` | 读取.docx为JSON | `python docx_read.py file.docx` |
| `docx_edit.py` | 修改.docx内容 | `python docx_edit.py file.docx --action replace --target "旧" --replacement "新"` |
| `pptx_read.py` | 读取.pptx为JSON | `python pptx_read.py file.pptx` |
| `pptx_edit.py` | 修改.pptx内容 | `python pptx_edit.py file.pptx --slide 3 --action replace --target "旧" --replacement "新"` |
| `knowledge_search.py` | 搜索知识库 | `python knowledge_search.py "课程重构" --category 方法论 --limit 10` |
| `svg_architecture.py` | 生成架构图SVG | `python svg_architecture.py --description "描述" --output out.svg` |

## 项目结构

```
jingsai-expert-system/
├── opencode.json                    # 项目配置
├── requirements.txt                 # Python依赖
├── AGENTS.md                        # Agent使用说明
├── README.md                        # 本文件
├── .opencode/
│   └── agent/
│       ├── jingsai-coach.md         # 主Agent：实战教练
│       ├── jingsai-reviewer.md      # 审校Agent：政策审查
│       └── jingsai-judge.md         # 审校Agent：评委模拟
│   └── skills/
│       └── jingsai-tools/
│           ├── SKILL.md             # Skill描述和使用指南
│           └── scripts/             # Python工具脚本
├── knowledge-base/                  # 知识原子库
│   ├── 方法论/
│   ├── 资源/
│   └── 标准/
└── docs/
    ├── 专家认知模式分析.md            # 专家思维分析报告
    └── SystemPrompt源文件.md         # System Prompt原始版本
```

## 自定义

### 更换模型

编辑各agent的 `.md` 文件头部 `model` 字段，或直接在 `opencode.json` 的 `agent` 部分覆盖。

### 增减知识原子

直接在 `knowledge-base/` 对应目录中增删 .md 文件即可。文件名格式：`序号_主题.md`。

### 添加新Agent

在 `.opencode/agent/` 中新建 `.md` 文件，按现有格式编写即可。

## 许可

本项目仅供教学研究使用。
