"""
根据文本描述生成教学能力比赛架构图的SVG。

输出一个美观的、符合教学比赛评审审美的SVG架构图。

设计原则（来自知识库）：
- 要素完整（政策依据、重构逻辑、模块关系、思政维度缺一不可）
- 关联明显（用箭头、加号、位置排布表达关系）
- 不过于复杂（图的作用是简化信息）
- 依据放最上面（重要性位置=定义优先级）
- 配色统一（与视频、课件、着装同色系）
"""
import sys
import json
import os
import argparse

def generate_svg(description, output_path, width=1200, height=800):
    svg_template = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" 
     font-family="Microsoft YaHei, SimHei, sans-serif">
  <defs>
    <style>
      .title {{ font-size: 24px; font-weight: bold; fill: #1a1a2e; text-anchor: middle; }}
      .subtitle {{ font-size: 16px; fill: #16213e; text-anchor: middle; }}
      .box {{ rx: 8; ry: 8; stroke-width: 2; }}
      .box-primary {{ fill: #e8f4f8; stroke: #0f3460; }}
      .box-secondary {{ fill: #fff3e0; stroke: #e65100; }}
      .box-highlight {{ fill: #e8f5e9; stroke: #2e7d32; }}
      .box-policy {{ fill: #fce4ec; stroke: #c62828; }}
      .label {{ font-size: 14px; fill: #1a1a2e; text-anchor: middle; }}
      .label-small {{ font-size: 12px; fill: #555; text-anchor: middle; }}
      .arrow {{ stroke: #0f3460; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }}
      .arrow-dashed {{ stroke: #999; stroke-width: 1.5; fill: none; stroke-dasharray: 6,3; marker-end: url(#arrowhead-gray); }}
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#0f3460"/>
    </marker>
    <marker id="arrowhead-gray" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#999"/>
    </marker>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#fafafa"/>
  
  <!-- Title -->
  <text x="{title_x}" y="40" class="title">{title}</text>
  <line x1="{line_start}" y1="55" x2="{line_end}" y2="55" stroke="#0f3460" stroke-width="2"/>
  
  <!-- PLACEHOLDER: Agent should replace the content below based on description -->
  <text x="{title_x}" y="{height}/2" class="subtitle" fill="#999">
    [此SVG为模板骨架，需根据具体描述填充内容]
  </text>
  <text x="{title_x}" y="{height}/2 + 30" class="subtitle" fill="#999">
    描述: {desc_escaped}
  </text>
</svg>'''

    title = "教学架构图"
    for line in description.split("\n"):
        if "标题" in line or "title" in line.lower():
            parts = line.split("：", 1)
            if len(parts) > 1:
                title = parts[1].strip()
                break
            parts = line.split(":", 1)
            if len(parts) > 1:
                title = parts[1].strip()
                break

    desc_escaped = description.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    title_x = width // 2
    line_start = width // 2 - 200
    line_end = width // 2 + 200

    svg = svg_template.format(
        width=width, height=height, title=title,
        title_x=title_x, line_start=line_start, line_end=line_end,
        desc_escaped=desc_escaped
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    return {"status": "ok", "output": output_path, "note": "Template SVG generated. Agent should customize based on description."}

def main():
    parser = argparse.ArgumentParser(description="Generate architecture SVG")
    parser.add_argument("--description", required=True, help="Architecture description")
    parser.add_argument("--output", default="output.svg", help="Output SVG path")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=800)
    args = parser.parse_args()

    result = generate_svg(args.description, args.output, args.width, args.height)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
