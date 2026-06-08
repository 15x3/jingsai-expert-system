---
name: jingsai-tools
description: 职业教育教学能力比赛专家系统的工具集。Use ONLY when the user asks about 教学能力比赛, 备赛, 实施报告, 教案, 课程重构, 视频拍摄, 现场答辩, or when handling .docx/.pptx/架构图 related to 教学比赛.
---

# 教学能力比赛工具集

## 知识库位置

知识原子存放在 `knowledge-base/` 目录下，三个子目录：
- `knowledge-base/方法论/` — 方法论类原子（约139个）
- `knowledge-base/资源/` — 资源类原子（约43个）
- `knowledge-base/标准/` — 标准类原子（约82个）

每个原子是一个独立的 .md 文件，格式：
```yaml
---
类型: 方法论/资源/标准
主题: xxx
标签: #tag1, #tag2
适用场景: xxx
置信度: 高/中/低
原始来源: 第X天X午_演讲记录
---
## 问题
...
## 核心内容
...
## 参考
...
```

## 工具脚本

所有脚本位于 `scripts/` 目录，通过 bash 调用。

### 1. 读取 .docx 文件

```bash
python scripts/docx_read.py "path/to/file.docx"
```

输出：纯文本内容（保留段落结构）。

### 2. 修改 .docx 文件

```bash
python scripts/docx_edit.py "path/to/file.docx" --action replace --target "旧文本" --replacement "新文本"
python scripts/docx_edit.py "path/to/file.docx" --action insert --after "某段落末尾文本" --text "要插入的内容"
python scripts/docx_edit.py "path/to/file.docx" --action format --target "某段文本" --style "标题1"
```

操作说明：
- `replace`：替换指定文本（全文搜索，支持部分匹配）
- `insert`：在指定段落后插入新段落
- `format`：修改指定段落的样式（标题1/标题2/正文等）
- 每次修改会自动创建 .bak 备份

### 3. 读取 .pptx 文件

```bash
python scripts/pptx_read.py "path/to/file.pptx"
```

输出：每页幻灯片的文本内容，标注页码和布局类型。

### 4. 修改 .pptx 文件

```bash
python scripts/pptx_edit.py "path/to/file.pptx" --slide 3 --action replace --target "旧文本" --replacement "新文本"
python scripts/pptx_edit.py "path/to/file.pptx" --slide 1 --action add-text --text "新内容" --position "{\"left\": 100, \"top\": 200, \"width\": 400, \"height\": 50}"
```

### 5. 生成架构图

```bash
python scripts/svg_architecture.py --description "描述架构内容" --output "output.svg"
```

或直接在回复中生成 SVG 代码，然后用 `godot_generate_2d_asset` 或写入 .html 文件。

架构图设计原则（来自知识库）：
- 要素完整（政策依据、重构逻辑、模块关系、思政维度缺一不可）
- 关联明显（用箭头、加号、位置排布表达关系）
- 不过于复杂（"多等于没有"——图的作用是简化信息）
- 依据放最上面（重要性放在哪里说明你怎么定义信息）

### 6. 搜索知识库

```bash
python scripts/knowledge_search.py "搜索关键词"
python scripts/knowledge_search.py "课程重构" --category 方法论
python scripts/knowledge_search.py "思政" --limit 10
```

参数：
- 第一个参数：搜索关键词
- `--category`：限定类别（方法论/资源/标准），可选
- `--limit`：返回条数上限，默认5

输出：匹配的知识原子文件路径 + 相关度评分 + 摘要。

如果知识库中没有找到相关内容，agent应使用 websearch 工具联网搜索。

## 检索策略

根据用户问题类型，优先搜索不同子目录：

| 问题类型 | 优先搜索 | 典型关键词 |
|----------|----------|-----------|
| "怎么做"类（方法流程） | 方法论/ | 重构、设计、拍摄、撰写、答辩 |
| "用什么"类（工具资源） | 资源/ | 术语、案例、模板、工具 |
| "对不对"类（标准规范） | 标准/ | 评分、扣分、规范、要求、检查 |
| 混合型 | 全部三个目录 | — |

## 审校工作流

主agent生成建议后，必须通过 task 工具并行派发审校：

```
task(subagent_type="general", prompt="请审查以下备赛指导建议的政策合规性：\n[建议内容]")

task(subagent_type="general", prompt="请从评委角度审查以下备赛指导建议：\n[建议内容]")
```

注意：审校agent需要通过 opencode.json 中的 agent 配置引用。
