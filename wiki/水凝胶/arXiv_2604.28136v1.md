---
type: literature
source_type: arxiv
arxiv_id: 2604.28136v1
topic: hydrogel
date: 2026-05-12
rating: ★☆☆☆☆
_audit: pending
_audit_codex: FULLTEXT
_fulltext_attempt: html
tags: [hydrogel, arxiv, irrelevant-hit]
---

# Beyond Pixel Fidelity: Minimizing Perceptual Distortion and Color Bias in Night Photography Rendering

## 基本信息

| 属性 | 值 |
|------|-----|
| **arXiv** | [2604.28136v1](https://arxiv.org/abs/2604.28136v1) |
| **分类** | Computer Vision and Pattern Recognition (cs.CV) |
| **作者** | Kınlı, Furkan |
| **年份** | 2026 |
| **全文** | [HTML](https://arxiv.org/html/2604.28136v1) / [PDF](https://arxiv.org/pdf/2604.28136v1) |
| **检索来源** | arXiv:cellulose-based anti-freezing  |
| **原始保存日期** | 2026-05-02 |

## 摘要

Night Photography Rendering (NPR) poses a significant challenge due to the extreme contrast between dark and illuminated areas in scenes, stemming from concurrent capture of severely dark regions alongside intense point light sources. Existing methods, which are mainly tailored for fidelity metrics, reveal considerable perceptual gaps and often detract from visual quality. We introduce pHVI-ISPNet, a novel RAW-to-RGB framework built on the robust HVI color space. Our network integrates four distinct key refinements: RAW-domain feature processing and Wavelet-based feature propagation to mitigate high-frequency detail loss; sample-based dynamic loss coefficients to ensure stable learning across varying exposure levels; and loss term based on feature distributions to maintain rigorous color constancy. Evaluations on the dataset introduced in the NTIRE 2025 challenge on NPR confirm our approach achieves competitive fidelity while establishing new state-of-the-art results in both CIE2000 color difference and LPIPS. This validates our perceptually-driven design for high-quality nighttime imaging.

## HTML 全文结构

- 1 Introduction
- 2 Related Works
- 3 Methodology
- 3.1 Base Architecture: CIDNet
- 3.2 RAW-Domain Feature Processing
- 3.3 Wavelet-based Feature Propagation
- 3.4 Loss Functions
- 4 Experiments

## Codex 精读（v2，基于 arXiv HTML 全文）

### 核心判断
- 已获取 arXiv HTML 全文，这篇属于 算法/计算论文，当前主题判定主要依据标题、摘要与章节结构喵~「Title」「Abstract」
- 摘要与正文目录表明这篇论文讨论的是“Beyond Pixel Fidelity: Minimizing Perceptual Distortion and Color Bias in Night Photography Rendering”对应的问题域，属于 Computer Vision and Pattern Recognition (cs.CV)，不是纤维素/水凝胶/抗冻凝胶材料研究喵~「Title」「Abstract」「1 Introduction」「2 Related Works」「3 Methodology」「3.1 Base Architecture: CIDNet」
- 正文结构集中在 1 Introduction / 2 Related Works / 3 Methodology / 3.1 Base Architecture: CIDNet / 3.2 RAW-Domain Feature Processing，没有出现 cellulose、hydrogel、gel electrolyte、anti-freezing 等材料关键词喵~「1 Introduction」「2 Related Works」「3 Methodology」「3.1 Base Architecture: CIDNet」

### 可追溯数据
- Evaluations on the dataset introduced in the NTIRE 2025 challenge on NPR confirm our approach achieves competitive fidelity while establishing new state-of-the-art results in both CIE2000 color difference and LPIPS. 喵~「Abstract」

### 与综述关联
- 对《Wide-Temperature Tolerant Cellulose-Based Gels》而言，这是一条检索误召回；建议保留为排除样本，不进入正文证据链或数据矩阵喵~「Title」「Abstract」
- 如果后续要优化检索式，优先收紧材料词与低温性能词组合，而不是继续沿用当前这条噪声结果喵~「Title」「Abstract」

### 不足与后续
- 本次升级目标是“全文获取 + 主题判定 + v2 覆盖”；由于该文与综述主题不符，没有继续逐节抽取全部实验/结果细节喵~「Abstract」「1 Introduction」「2 Related Works」「3 Methodology」「3.1 Base Architecture: CIDNet」

### 置信度 | 5/5 |
已获取 arXiv HTML 全文，相关性判断可追溯到标题、摘要与正文结构，足以稳定标记为 FULLTEXT 喵~

## 原文核查表

- [x] 已核对 arXiv 标题与摘要
- [x] 已核对 HTML 正文章节结构
- [x] 综述相关性判断可追溯到原文位置
