---
type: literature
source_type: arxiv
arxiv_id: 2604.28169v1
topic: hydrogel
date: 2026-05-12
rating: ★☆☆☆☆
_audit: pending
_audit_codex: FULLTEXT
_fulltext_attempt: html
tags: [hydrogel, arxiv, irrelevant-hit]
---

# PhyCo: Learning Controllable Physical Priors for Generative Motion

## 基本信息

| 属性 | 值 |
|------|-----|
| **arXiv** | [2604.28169v1](https://arxiv.org/abs/2604.28169v1) |
| **分类** | Computer Vision and Pattern Recognition (cs.CV) |
| **作者** | Narayanan, Sriram; Jiang, Ziyu; Narasimhan, Srinivasa; Chandraker, Manmohan |
| **年份** | 2026 |
| **全文** | [HTML](https://arxiv.org/html/2604.28169v1) / [PDF](https://arxiv.org/pdf/2604.28169v1) |
| **检索来源** | arXiv:self-healing hydrogel cryoprot |
| **原始保存日期** | 2026-05-02 |

## 摘要

Modern video diffusion models excel at appearance synthesis but still struggle with physical consistency: objects drift, collisions lack realistic rebound, and material responses seldom match their underlying properties. We present PhyCo, a framework that introduces continuous, interpretable, and physically grounded control into video generation. Our approach integrates three key components: (i) a large-scale dataset of over 100K photorealistic simulation videos where friction, restitution, deformation, and force are systematically varied across diverse scenarios; (ii) physics-supervised fine-tuning of a pretrained diffusion model using a ControlNet conditioned on pixel-aligned physical property maps; and (iii) VLM-guided reward optimization, where a fine-tuned vision-language model evaluates generated videos with targeted physics queries and provides differentiable feedback. This combination enables a generative model to produce physically consistent and controllable outputs through variations in physical attributes-without any simulator or geometry reconstruction at inference. On the Physics-IQ benchmark, PhyCo significantly improves physical realism over strong baselines, and human studies confirm clearer and more faithful control over physical attributes. Our results demonstrate a scalable path toward physically consistent, controllable generative video models that generalize beyond synthetic training environments.

## HTML 全文结构

- 1 Introduction
- 2 Related Work
- 3 Method
- 3.1 Physically Grounded Simulations
- 3.2 Physics Supervised Fine-tuning
- 3.3 VLM Reward Optimization
- 4 Experimental Results
- 5 Conclusion

## Codex 精读（v2，基于 arXiv HTML 全文）

### 核心判断
- 已获取 arXiv HTML 全文，这篇属于 算法/计算论文，当前主题判定主要依据标题、摘要与章节结构喵~「Title」「Abstract」
- 摘要与正文目录表明这篇论文讨论的是“PhyCo: Learning Controllable Physical Priors for Generative Motion”对应的问题域，属于 Computer Vision and Pattern Recognition (cs.CV)，不是纤维素/水凝胶/抗冻凝胶材料研究喵~「Title」「Abstract」「1 Introduction」「2 Related Work」「3 Method」「3.1 Physically Grounded Simulations」
- 正文结构集中在 1 Introduction / 2 Related Work / 3 Method / 3.1 Physically Grounded Simulations / 3.2 Physics Supervised Fine-tuning，没有出现 cellulose、hydrogel、gel electrolyte、anti-freezing 等材料关键词喵~「1 Introduction」「2 Related Work」「3 Method」「3.1 Physically Grounded Simulations」

### 可追溯数据
- Our approach integrates three key components: (i) a large-scale dataset of over 100K photorealistic simulation videos where friction, restitution, deformation, and force are systematically varied across diverse scenarios; (ii) physics-supervised fine-tuning of a pretrained diffusion model using a ControlNet conditioned on pixel-aligned physical property maps; and (iii) VLM-guided reward optimization, where a fine-tuned vision-language model evaluates generated videos with targeted physics queries and provides differentiable feedback. 喵~「Abstract」

### 与综述关联
- 对《Wide-Temperature Tolerant Cellulose-Based Gels》而言，这是一条检索误召回；建议保留为排除样本，不进入正文证据链或数据矩阵喵~「Title」「Abstract」
- 如果后续要优化检索式，优先收紧材料词与低温性能词组合，而不是继续沿用当前这条噪声结果喵~「Title」「Abstract」

### 不足与后续
- 本次升级目标是“全文获取 + 主题判定 + v2 覆盖”；由于该文与综述主题不符，没有继续逐节抽取全部实验/结果细节喵~「Abstract」「1 Introduction」「2 Related Work」「3 Method」「3.1 Physically Grounded Simulations」

### 置信度 | 5/5 |
已获取 arXiv HTML 全文，相关性判断可追溯到标题、摘要与正文结构，足以稳定标记为 FULLTEXT 喵~

## 原文核查表

- [x] 已核对 arXiv 标题与摘要
- [x] 已核对 HTML 正文章节结构
- [x] 综述相关性判断可追溯到原文位置
