import sys
import json
import os
import re

def search_knowledge(keyword, category=None, limit=5):
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))), "knowledge-base")
    if not os.path.isdir(base):
        return {"error": f"knowledge-base not found at {base}", "results": []}

    categories = [category] if category else ["方法论", "资源", "标准"]
    results = []

    keyword_lower = keyword.lower()
    keywords = [k.strip() for k in keyword_lower.split()]

    for cat in categories:
        cat_path = os.path.join(base, cat)
        if not os.path.isdir(cat_path):
            continue
        for fname in sorted(os.listdir(cat_path)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(cat_path, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                continue

            content_lower = content.lower()
            score = 0
            for kw in keywords:
                score += content_lower.count(kw)

            title = ""
            tags = ""
            scenario = ""
            confidence = ""
            for line in content.split("\n"):
                line_stripped = line.strip()
                if line_stripped.startswith("主题:"):
                    title = line_stripped[3:].strip()
                elif line_stripped.startswith("标签:"):
                    tags = line_stripped[3:].strip()
                elif line_stripped.startswith("适用场景:"):
                    scenario = line_stripped[5:].strip()
                elif line_stripped.startswith("置信度:"):
                    confidence = line_stripped[4:].strip()
                elif line_stripped == "---":
                    break

            if score > 0:
                results.append({
                    "file": f"{cat}/{fname}",
                    "score": score,
                    "title": title,
                    "tags": tags,
                    "scenario": scenario,
                    "confidence": confidence,
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"keyword": keyword, "total_matches": len(results), "results": results[:limit]}

def main():
    if len(sys.argv) < 2:
        print("Usage: python knowledge_search.py <keyword> [--category 方法论|资源|标准] [--limit N]", file=sys.stderr)
        sys.exit(1)

    keyword = sys.argv[1]
    args = sys.argv[2:]

    parsed = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                parsed[key] = args[i + 1]
                i += 2
            else:
                parsed[key] = True
                i += 1
        else:
            i += 1

    category = parsed.get("category", None)
    limit = int(parsed.get("limit", 5))

    result = search_knowledge(keyword, category, limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
