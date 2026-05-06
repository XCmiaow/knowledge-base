# raw/ — 原始文献

> **只读目录**。存放 Obsidian Web Clipper 剪藏和 Zotero 导出的原始文献数据。
> 此目录下的文件永不修改，仅由 paper-ingest 技能读取并标记处理状态。

## 主题目录

| 目录 | 说明 | 来源 |
|------|------|------|
| `水凝胶/` | 水凝胶相关论文 | Web Clipper + Zotero |
| `有机磷化学/` | 有机磷/膦化学论文 | Web Clipper + Zotero |
| `化学信息学/` | AI/ML 化学论文 | Web Clipper + Zotero |
| `化工设计竞赛/` | 竞赛相关文献 | Web Clipper + Zotero |
| `其他/` | 未分类或跨主题 | Web Clipper |

## 工作流

1. 新剪藏 → `raw/<主题>/` (status: unprocessed)
2. 运行 `paper-ingest` → 读取 → 生成 wiki 页面
3. 标记 `status: processed`

## 格式

### JSON（Zotero 导出）
```json
{
  "doi": "10.xxxx/xxxxx",
  "title_en": "...",
  "title_zh": "...",
  "authors": [...],
  "journal": "...",
  "abstract": "...",
  "status": "unprocessed|processed"
}
```

### Markdown（Web Clipper 剪藏）
带 frontmatter 的 markdown 文件，`status: unprocessed|processed`
