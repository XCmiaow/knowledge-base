---
type: literature
source_type: arxiv
arxiv_id: 2604.28180v1
topic: hydrogel
date: 2026-05-12
rating: ★☆☆☆☆
_audit: pending
_audit_codex: FULLTEXT
_fulltext_attempt: html
tags: [hydrogel, arxiv, irrelevant-hit]
---

# An adaptive wavelet-based PINN for problems with localized high-magnitude source

## 基本信息

| 属性 | 值 |
|------|-----|
| **arXiv** | [2604.28180v1](https://arxiv.org/abs/2604.28180v1) |
| **分类** | Machine Learning (cs.LG) |
| **作者** | Pandey, Himanshu; Behera, Ratikanta |
| **年份** | 2026 |
| **全文** | [HTML](https://arxiv.org/html/2604.28180v1) / [PDF](https://arxiv.org/pdf/2604.28180v1) |
| **检索来源** | arXiv:ionic conductive hydrogel low  |
| **原始保存日期** | 2026-05-02 |

## 摘要

In recent years, physics-informed neural networks (PINNs) have gained significant attention for solving differential equations, although they suffer from two fundamental limitations, namely, spectral bias inherent in neural networks and loss imbalance arising from multiscale phenomena. This paper proposes an adaptive wavelet-based PINN (AW-PINN) to address the extreme loss imbalance characteristic of problems with localized high-magnitude source terms. Such problems frequently arise in various physical applications, such as thermal processing, electro-magnetics, impact mechanics, and fluid dynamics involving localized forcing. The proposed framework dynamically adjusts the wavelet basis function based on residual and supervised loss. This adaptive nature makes AW-PINN handle problems with high-scale features effectively without being memory-intensive. Additionally, AW-PINN does not rely on automatic differentiation to obtain derivatives involved in the loss function, which accelerates the training process. The method operates in two stages, an initial short pre-training phase with fixed bases to select physically relevant wavelet families, followed by an adaptive refinement that adapts scales and translations without populating high-resolution bases across entire domains. Theoretically, we show that under certain assumptions, AW-PINN admits a Gaussian process limit and derive its associated NTK structure. We evaluate AW-PINN on several challenging PDEs featuring localized high-magnitude source terms with extreme loss imbalances having ratios up to $10^{10}:1$. Across these PDEs, including transient heat conduction, highly localized Poisson problems, oscillatory flow equations, and Maxwell equations with a point charge source, AW-PINN consistently outperforms existing methods in its class.

## HTML 全文结构

- 1 Introduction
- 2 Related Works
- 2.1 PINN framework for problems with multi-magnitude loss terms
- 2.2 Wavelet-based PINN
- 2.3 Neural Tangent Kernel theory for PINN
- 3 Adaptive Wavelet-based PINN
- 4 Results
- 4.1 Heat conduction problem with extreme heat source

## Codex 精读（v2，基于 arXiv HTML 全文）

### 核心判断
- 已获取 arXiv HTML 全文，这篇属于 算法/计算论文，当前主题判定主要依据标题、摘要与章节结构喵~「Title」「Abstract」
- 摘要与正文目录表明这篇论文讨论的是“An adaptive wavelet-based PINN for problems with localized high-magnitude source”对应的问题域，属于 Machine Learning (cs.LG)，不是纤维素/水凝胶/抗冻凝胶材料研究喵~「Title」「Abstract」「1 Introduction」「2 Related Works」「2.1 PINN framework for problems with multi-magnitude loss terms」「2.2 Wavelet-based PINN」
- 正文结构集中在 1 Introduction / 2 Related Works / 2.1 PINN framework for problems with multi-magnitude loss terms / 2.2 Wavelet-based PINN / 2.3 Neural Tangent Kernel theory for PINN，没有出现 cellulose、hydrogel、gel electrolyte、anti-freezing 等材料关键词喵~「1 Introduction」「2 Related Works」「2.1 PINN framework for problems with multi-magnitude loss terms」「2.2 Wavelet-based PINN」

### 可追溯数据
- We evaluate AW-PINN on several challenging PDEs featuring localized high-magnitude source terms with extreme loss imbalances having ratios up to $10^{10}:1$. 喵~「Abstract」

### 与综述关联
- 对《Wide-Temperature Tolerant Cellulose-Based Gels》而言，这是一条检索误召回；建议保留为排除样本，不进入正文证据链或数据矩阵喵~「Title」「Abstract」
- 如果后续要优化检索式，优先收紧材料词与低温性能词组合，而不是继续沿用当前这条噪声结果喵~「Title」「Abstract」

### 不足与后续
- 本次升级目标是“全文获取 + 主题判定 + v2 覆盖”；由于该文与综述主题不符，没有继续逐节抽取全部实验/结果细节喵~「Abstract」「1 Introduction」「2 Related Works」「2.1 PINN framework for problems with multi-magnitude loss terms」「2.2 Wavelet-based PINN」

### 置信度 | 5/5 |
已获取 arXiv HTML 全文，相关性判断可追溯到标题、摘要与正文结构，足以稳定标记为 FULLTEXT 喵~

## 原文核查表

- [x] 已核对 arXiv 标题与摘要
- [x] 已核对 HTML 正文章节结构
- [x] 综述相关性判断可追溯到原文位置
