---
type: literature
source_type: arxiv
arxiv_id: 2604.28179v1
topic: hydrogel
date: 2026-05-12
rating: ★☆☆☆☆
_audit: pending
_audit_codex: FULLTEXT
_fulltext_attempt: html
tags: [hydrogel, arxiv, irrelevant-hit]
---

# Stop Holding Your Breath: CT-Informed Gaussian Splatting for Dynamic Bronchoscopy

## 基本信息

| 属性 | 值 |
|------|-----|
| **arXiv** | [2604.28179v1](https://arxiv.org/abs/2604.28179v1) |
| **分类** | Computer Vision and Pattern Recognition (cs.CV) |
| **作者** | Beltran, Andrea Dunn; Rho, Daniel; Mehta, Aarav; Xiong, Xinqi; Estépar, Raúl San José; Alterovitz, Ron; Niethammer, Marc; Sengupta, Roni |
| **年份** | 2026 |
| **全文** | [HTML](https://arxiv.org/html/2604.28179v1) / [PDF](https://arxiv.org/pdf/2604.28179v1) |
| **检索来源** | arXiv:cellulose hydrogel freeze tole |
| **原始保存日期** | 2026-05-02 |

## 摘要

Bronchoscopic navigation relies on registering endoscopic video to a preoperative CT scan, but respiratory motion deforms the airway by 5-20 mm, creating CT-to-body divergence that limits localization accuracy. In practice, this is mitigated through breath-hold protocols, which attempt to match the intraoperative anatomy to a static CT, but are difficult to reproduce and disrupt clinical workflow. We propose to eliminate the need for breath-hold protocols by leveraging patient-specific respiratory modeling. Paired inhale-exhale CT scans, already acquired for planning, implicitly define the patient-specific deformation space of the breathing airway. By registering these scans, we reduce respiratory motion to a single scalar breathing phase per frame, constraining all reconstructions to anatomically observed configurations. We embed this representation within a mesh-anchored Gaussian splatting framework, where a lightweight estimator infers breathing phase directly from endoscopic RGB, enabling continuous, deformation-aware reconstruction throughout the respiratory cycle without breath-holds or external sensing. To enable quantitative evaluation, we introduce RESPIRE, a physically grounded bronchoscopy simulation pipeline with per-frame ground truth for geometry, pose, breathing phase, and deformation. Experiments on RESPIRE show that our approach achieves geometrically faithful reconstruction, over 20x faster training, and 1.22 mm target localization accuracy (within the 3mm clinically relevant tolerances) outperforming unconstrained single-CT baselines. Please check out our website for additional visuals: this https URL

## HTML 全文结构

- 1 Introduction
- 2 Related Works
- 3 Methods
- 4 RESPIRE Framework
- 5 Experiments
- 5.1 Results
- 6 Conclusion

## Codex 精读（v2，基于 arXiv HTML 全文）

### 核心判断
- 已获取 arXiv HTML 全文，这篇属于 算法/计算论文，当前主题判定主要依据标题、摘要与章节结构喵~「Title」「Abstract」
- 摘要与正文目录表明这篇论文讨论的是“Stop Holding Your Breath: CT-Informed Gaussian Splatting for Dynamic Bronchoscopy”对应的问题域，属于 Computer Vision and Pattern Recognition (cs.CV)，不是纤维素/水凝胶/抗冻凝胶材料研究喵~「Title」「Abstract」「1 Introduction」「2 Related Works」「3 Methods」「4 RESPIRE Framework」
- 正文结构集中在 1 Introduction / 2 Related Works / 3 Methods / 4 RESPIRE Framework / 5 Experiments，没有出现 cellulose、hydrogel、gel electrolyte、anti-freezing 等材料关键词喵~「1 Introduction」「2 Related Works」「3 Methods」「4 RESPIRE Framework」

### 可追溯数据
- Bronchoscopic navigation relies on registering endoscopic video to a preoperative CT scan, but respiratory motion deforms the airway by 5-20 mm, creating CT-to-body divergence that limits localization accuracy. 喵~「Abstract」
- Experiments on RESPIRE show that our approach achieves geometrically faithful reconstruction, over 20x faster training, and 1.22 mm target localization accuracy (within the 3mm clinically relevant tolerances) outperforming unconstrained single-CT baselines. 喵~「Abstract」

### 与综述关联
- 对《Wide-Temperature Tolerant Cellulose-Based Gels》而言，这是一条检索误召回；建议保留为排除样本，不进入正文证据链或数据矩阵喵~「Title」「Abstract」
- 如果后续要优化检索式，优先收紧材料词与低温性能词组合，而不是继续沿用当前这条噪声结果喵~「Title」「Abstract」

### 不足与后续
- 本次升级目标是“全文获取 + 主题判定 + v2 覆盖”；由于该文与综述主题不符，没有继续逐节抽取全部实验/结果细节喵~「Abstract」「1 Introduction」「2 Related Works」「3 Methods」「4 RESPIRE Framework」

### 置信度 | 5/5 |
已获取 arXiv HTML 全文，相关性判断可追溯到标题、摘要与正文结构，足以稳定标记为 FULLTEXT 喵~

## 原文核查表

- [x] 已核对 arXiv 标题与摘要
- [x] 已核对 HTML 正文章节结构
- [x] 综述相关性判断可追溯到原文位置
