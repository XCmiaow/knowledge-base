---
description: 会话上下文缓存——记录最近的知识库活动
updated: 2026-05-06
---

# hot.md

## 最近活动

- [2026-05-06] **服务器同步**：从服务器（`peach-lover.com`）完整同步 KB wiki（146 篇 arXiv 文献）+ Obsidian vault（227 篇深读笔记），总计 +373 篇。本地文献从 170 → 543 篇。
- [2026-05-06] **paper-ingest 打通**：完成 paper-ingest/paper-query 技能、全局配置、项目 hooks。批量处理 raw/水凝胶/ 中 53 个 JSON 文件。
- [2026-05-06] **服务器架构发现**：OpenClaw 服务器（peach-lover.com）含 KB wiki（146 篇）+ Obsidian vault（314 篇），通过 `accept_literature.py` cron 每日同步 + 飞书通知
- [2026-05-06] **literature-review 仓库**：发现 GitHub 上 617MB 的 `literature-review` 库，含 44 篇 PDF + 60 篇 MD 文献笔记（水凝胶方向）
- [2026-05-06] **全量文献总览**：服务器 KB 146 + Obsidian vault 314 + Zotero 396 + lit-review 44PDF/60MD，知识库基数充足
- [2026-04-30] 知识库初始建立，~82 篇文献笔记

## 当前状态

| 领域 | 文献 | 方向 |
|------|------|------|
| 水凝胶 | 402 篇 | 刺激响应、抗冻、药物递送、组织工程 |
| 有机磷化学 | 57 篇 | 手性膦催化剂、C-P键、不对称催化 |
| 化学信息学 | 51 篇 | ML分子建模、AI药物发现 |
| 化工设计竞赛 | 33 篇 | 苯乙烯清洁生产、乙苯脱氢 |

## 待办

- 有新 raw 文件时运行 `paper-ingest` 技能
- 每 10-15 篇新文献后调用 paper-lint 健康检查
- 好问答答案归档到 `wiki/问答/`

## 技能快速参考

- `paper-ingest`：raw/ → wiki/ 消化流水线
- `paper-query`：3 层渐进检索（Quick / Standard / Deep）
