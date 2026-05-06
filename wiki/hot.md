---
description: 会话上下文缓存——记录最近的知识库活动
updated: 2026-05-06
---

# hot.md

## 最近活动

- [2026-05-06] **paper-ingest 打通**：完成 paper-ingest/paper-query 技能、全局配置、项目 hooks。批量处理 raw/水凝胶/ 中 53 个 JSON 文件（均已有 wiki 页面，仅标记 processed）。重建 4 个主题 README 索引，更新总览/SUMMARY 计数。
- [2026-04-30] 知识库初始建立，~82 篇文献笔记

## 当前状态

| 领域 | 文献 | 方向 |
|------|------|------|
| 水凝胶 | 58 篇 | 刺激响应、抗冻、药物递送、组织工程 |
| 有机磷化学 | 9 篇 | 手性膦催化剂、C-P键、不对称催化 |
| 化学信息学 | 13 篇 | ML分子建模、AI药物发现 |
| 化工设计竞赛 | 4 篇 | 苯乙烯清洁生产、乙苯脱氢 |

## 待办

- 有新 raw 文件时运行 `paper-ingest` 技能
- 每 10-15 篇新文献后调用 paper-lint 健康检查
- 好问答答案归档到 `wiki/问答/`

## 技能快速参考

- `paper-ingest`：raw/ → wiki/ 消化流水线
- `paper-query`：3 层渐进检索（Quick / Standard / Deep）
