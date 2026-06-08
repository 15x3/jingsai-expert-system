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

---

## 部署教程

### 前置条件

| 条件 | 版本要求 | 检查方式 |
|------|---------|---------|
| Python | 3.8+ | `python --version` |
| pip | 最新 | `pip --version` |
| opencode CLI | 最新 | `opencode --version` |
| LLM API Key | 任选一家 | 见下方Provider配置 |

如果你还没有安装 opencode：
```bash
# 参考 https://opencode.ai 获取安装方式
```

### 第一步：获取代码

**方式A：从Git克隆（如果仓库已推送到远程）**
```bash
git https://github.com/15x3/jingsai-expert-system
cd jingsai-expert-system
```

**方式B：直接复制文件夹**
将整个 `jingsai-expert-system/` 文件夹复制到目标机器，然后进入该目录。

### 第二步：安装Python依赖

```bash
pip install -r requirements.txt
```

这会安装三个包：
- `python-docx` — 读写 .docx 文件
- `python-pptx` — 读写 .pptx 文件
- `lxml` — XML处理（上述包的依赖）

验证安装：
```bash
python -c "import docx; import pptx; print('依赖安装成功')"
```

### 第三步：配置LLM Provider

你需要在 `opencode.json` 中配置至少一个LLM Provider。根据你使用的AI服务商选择对应配置：

#### 智谱AI（GLM系列）
```json
{
  "provider": {
    "zhipuai-coding-plan": {
      "options": {
        "apiKey": "你的智谱API Key"
      }
    }
  },
  "model": "zhipuai-coding-plan/glm-4.6",
  "small_model": "zhipuai-coding-plan/glm-4.5-air"
}
```

#### Anthropic（Claude系列）
```json
{
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "你的Anthropic API Key"
      }
    }
  },
  "model": "anthropic/claude-sonnet-4-6"
}
```

#### OpenAI（GPT系列）
```json
{
  "provider": {
    "openai": {
      "options": {
        "apiKey": "你的OpenAI API Key"
      }
    }
  },
  "model": "openai/gpt-4o"
}
```

**配置方式**（二选一）：

1. **项目级**（推荐）：直接编辑仓库内的 `opencode.json`，将上方配置合并进去
2. **全局级**：编辑 `~/.config/opencode/opencode.json`（已存在则合并，不存在则新建）

> 如果你已有全局 `opencode.json` 且其中已配置了 provider，项目级 `opencode.json` 中的 provider 和 model 可以删掉，系统会自动使用全局配置。

### 第四步：启动

```bash
cd jingsai-expert-system
opencode
```

看到 opencode 的交互界面出现，说明启动成功。

### 第五步：验证

在 opencode 对话中输入：

```
请搜索知识库中关于"课程重构"的内容
```

如果Agent返回了知识原子的搜索结果，说明知识库加载正常。

再输入：

```
请读取这个文件的内容：docs/专家认知模式分析.md
```

如果Agent能读取并展示内容，说明文件系统访问正常。

---

## 使用方式

### 场景一：审查文档并给出建议

```
请帮我审查这份实施报告，指出问题并给出修改建议：
E:\备赛材料\实施报告.docx
```

Agent会：
1. 读取 .docx 文件内容
2. 检索知识库中相关的标准和方法论
3. 生成建议（高/中/低三档）
4. 派发给两个审校Agent交叉验证
5. 综合输出最终建议

### 场景二：直接修改文档

```
把实施报告中第三段的教学目标改成可评可测的写法，
参考知识库中"教学目标可评可测设定标准"的要求
```

Agent会调用 `docx_edit.py` 脚本直接修改文件，并输出联动提醒（告诉你还需同步修改哪些材料）。

### 场景三：审查PPT

```
请审查这份说课PPT：
E:\备赛材料\说课PPT.pptx
```

Agent会读取每一页幻灯片内容，对照知识库给出建议。

### 场景四：生成架构图

```
帮我画一个课程重构的架构图，内容是：
- 顶部：政策依据（五要素联动、岗课赛证）
- 中间：重构逻辑（岗位→典型任务→能力图谱→模块化设计）
- 底部：三大模块（并列式，每个模块含项目名称和学时）
- 右侧：思政维度贯穿
```

Agent会生成SVG架构图并渲染为PNG。

### 场景五：知识问答

```
增值评价到底怎么设计？我们是一个中职专业课团队。
```

```
省赛和国赛的作品有什么区别？我们的作品该怎么定位？
```

```
视频拍摄时三机位怎么摆？
```

Agent会先搜索知识库，找到相关原子后基于专家思维回答。如果知识库中没有相关内容，会自动联网搜索补充。

### 场景六：让Agent同时处理文件+问题

```
请读取这份教案 E:\备赛材料\教案3.docx，
然后告诉我：
1. 学情分析够不够精准
2. 教学目标是否可评可测
3. 教学重难点是否与学情呼应
如果不达标，直接帮我修改
```

---

## 使用模式说明

### 模式A：在仓库目录内使用（默认）

```bash
cd jingsai-expert-system
opencode
```

所有agent、skill、知识库自动加载。你需要把待处理的文件放到仓库目录下，或使用文件的绝对路径。

### 模式B：在其他工作目录使用

如果你想在**自己的备赛工作目录**中使用专家系统：

**方法1：符号链接（Windows）**
```powershell
# 以管理员身份运行 PowerShell
# 将agent和skill链接到全局配置目录
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\agent\jingsai-coach.md" -Target "C:\path\to\jingsai-expert-system\.opencode\agent\jingsai-coach.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\agent\jingsai-reviewer.md" -Target "C:\path\to\jingsai-expert-system\.opencode\agent\jingsai-reviewer.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.config\opencode\agent\jingsai-judge.md" -Target "C:\path\to\jingsai-expert-system\.opencode\agent\jingsai-judge.md"
```

**方法2：复制文件到全局目录**
```powershell
# 创建全局agent目录（如果不存在）
New-Item -ItemType Directory -Path "$env:USERPROFILE\.config\opencode\agent" -Force

# 复制agent文件
Copy-Item "C:\path\to\jingsai-expert-system\.opencode\agent\*.md" "$env:USERPROFILE\.config\opencode\agent\"
```

然后在你的工作目录中创建一个 `opencode.json`，添加 skill 路径：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": [
      "C:/path/to/jingsai-expert-system/.opencode/skills"
    ]
  }
}
```

这样在任何目录运行 `opencode` 都能使用专家系统。

---

## 知识库

`knowledge-base/` 目录包含264个知识原子（.md文件），分为三类：

| 目录 | 内容 | 数量 |
|------|------|------|
| `方法论/` | 教学设计方法、比赛策略、操作流程 | ~139 |
| `资源/` | 术语库、案例集、工具推荐 | ~43 |
| `标准/` | 评分标准、检查清单、规范要求 | ~82 |

每个原子遵循统一格式：

```yaml
---
类型: 方法论
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

### 维护知识库

**新增原子**：在对应目录中新建 `.md` 文件，命名格式 `序号_主题.md`

**更新原子**：直接编辑对应的 `.md` 文件

**删除原子**：直接删除对应的 `.md` 文件

修改后无需重启 opencode，下次检索自动生效。

---

## 工具脚本

位于 `.opencode/skills/jingsai-tools/scripts/`：

| 脚本 | 功能 | 用法示例 |
|------|------|---------|
| `docx_read.py` | 读取.docx为JSON | `python docx_read.py file.docx` |
| `docx_edit.py` | 修改.docx内容 | `python docx_edit.py file.docx --action replace --target "旧文本" --replacement "新文本"` |
| `pptx_read.py` | 读取.pptx为JSON | `python pptx_read.py file.pptx` |
| `pptx_edit.py` | 修改.pptx内容 | `python pptx_edit.py file.pptx --slide 3 --action replace --target "旧文本" --replacement "新文本"` |
| `knowledge_search.py` | 搜索知识库 | `python knowledge_search.py "课程重构" --category 方法论 --limit 10` |
| `svg_architecture.py` | 生成架构图SVG | `python svg_architecture.py --description "描述" --output out.svg` |

这些脚本由Agent自动调用，一般不需要手动执行。

---

## 项目结构

```
jingsai-expert-system/
├── opencode.json                    # 项目配置（agent注册+model+skill路径）
├── requirements.txt                 # Python依赖
├── AGENTS.md                        # Agent使用说明（opencode自动读取）
├── README.md                        # 本文件
├── .gitignore
├── .opencode/
│   ├── agent/
│   │   ├── jingsai-coach.md         # 主Agent：实战教练
│   │   ├── jingsai-reviewer.md      # 审校Agent：政策审查
│   │   └── jingsai-judge.md         # 审校Agent：评委模拟
│   └── skills/
│       └── jingsai-tools/
│           ├── SKILL.md             # Skill描述和使用指南
│           └── scripts/             # Python工具脚本（6个）
├── knowledge-base/                  # 知识原子库（264个.md文件）
│   ├── 方法论/                      # 139个方法论原子
│   ├── 资源/                        # 43个资源原子
│   └── 标准/                        # 82个标准原子
└── docs/                            # 参考文档
    ├── 专家认知模式分析.md            # 专家思维分析报告
    ├── SystemPrompt源文件.md         # System Prompt原始版本
    └── 五整天培训_知识萃取总结.md     # 完整知识萃取总结
```

---

## 自定义

### 更换模型

编辑各agent的 `.md` 文件头部的 `model` 字段，或在 `opencode.json` 的 `agent` 部分覆盖：

```json
{
  "agent": {
    "jingsai-coach": {
      "model": "anthropic/claude-sonnet-4-6"
    },
    "jingsai-reviewer": {
      "model": "anthropic/claude-sonnet-4-6"
    },
    "jingsai-judge": {
      "model": "anthropic/claude-sonnet-4-6"
    }
  }
}
```

> 审校Agent建议使用与主Agent相同或更强的模型，以保证审查质量。

### 调整审校严格程度

编辑 `.opencode/agent/jingsai-reviewer.md` 和 `jingsai-judge.md` 中的审查维度和检查清单。

### 添加新知识来源

将新的知识原子 `.md` 文件放入 `knowledge-base/` 对应目录即可。格式参考现有文件。

### 添加新Agent

在 `.opencode/agent/` 中新建 `.md` 文件，按现有格式编写。opencode会自动发现。

---

## 常见问题

### Q: 启动opencode后Agent没有被识别？
确认你在 `jingsai-expert-system/` 目录下启动。opencode 从当前目录向上查找 `opencode.json`。

### Q: Agent无法读取我电脑上的文件？
使用文件的绝对路径（如 `E:\备赛材料\教案.docx`），不要使用相对路径。

### Q: Agent修改文档后文件损坏了怎么办？
每次修改前脚本会自动创建 `.bak` 备份文件。找到原文件旁边的 `.bak` 文件恢复即可。

### Q: 想在多台电脑上使用？
每台电脑执行同样的步骤：安装Python → 安装依赖 → 配置Provider → 启动opencode。知识库和Agent配置都在仓库中，git clone即可获取。

### Q: Agent的回答不够准确怎么办？
1. 检查知识库中是否有相关原子（`knowledge-base/` 目录）
2. 尝试把问题拆得更具体（不要问"怎么备赛"，问"中职电子信息专业的实施报告教学目标怎么写"）
3. 如果是模型能力问题，考虑升级到更强的模型

---

## 许可

本项目仅供教学研究使用。
