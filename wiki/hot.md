---
description: 会话上下文缓存——记录最近的知识库活动
updated: 2026-05-07
---

# hot.md

## 最近活动

- [2026-05-09] **Codex Section 4 精读补完：2 篇 TENG/农业文献入库**：Codex (GPT-5.4) 精读综述 Section 4 剩余子方向。PVA/纤维素DN TENG(-40~50°C, 30天不干, Nano Energy 2024)、NaCMC/HEC超吸水凝胶(水分效率+25-45%, IJBMC 2025)。KB水凝胶页：317→319篇。Codex精读：84→87 篇。：Codex (GPT-5.4) 精读综述 Section 3 方向。覆盖面条预拉伸超强水凝胶(>50 MPa, -80°C, Carbohydr. Polym. 2024)、BmimCl/AM PDES离子凝胶(-20°C, 2.44 S/m, ACS APM 2023)、全纤维素44200%伸长水凝胶(Mater. Today 2024)、PLCNF/Fe³⁺/Zn²⁺宽温域传感(CEJ 2025)、CNC+DMSO/H₂O抗冻-70°C(Carbohydr. Polym. 2022)。KB水凝胶页：307→314 篇。Codex精读：76→81 篇。

- [2026-05-09] **Codex 检索补充：22 篇纤维素基凝胶入库**：Codex (GPT-5.4) 零上下文检索 3 个综述缺口。纤维素溶解/fabrication(8篇，含 Research 2024、Mater. Today Chem综述、Carbohydr. Polym.×2), 软体机器人/执行器(6篇，含 Soft Robotics 2025、Nano Lett. 2024、Biomacromolecules), 细菌纤维素创面敷料(8篇，含 Adv. Mater. 2025、Carbohydr. Polym.×2、IJBMC×3)。KB水凝胶页：285→307 篇。：针对半成品综述 *Wide-Temperature Tolerant Cellulose-Based Gels* 的 6 个薄弱方向补充。CNC/CNF抗冻凝胶(3)、DES纤维素共晶凝胶(2)、纤维素TENG(2)、冷冻保存(2)、ML辅助设计(2)、水状态表征(3)。KB水凝胶页：271→285 篇。
- [2026-05-09] **深度扩充：17 篇高影响力水凝胶论文入库**：Web检索+Crossref富化，覆盖5薄弱方向。自修复/粘附(Nature 2025, Nat. Mater.×2 2025, Nat. Commun.×2), 防冰/冷冻保存(Nat. Commun.×2, Adv. Mater.×3), 电子皮肤/生物电子(Nat. Commun.×3, Adv. Sci. 2026), 有机水凝胶/抗脱水(Adv. Healthc. Mater., Nanoscale, IJEM)。Nature 1篇, Nat. Mater. 2篇, Nat. Commun. 7篇, Adv. Mater. 3篇。KB水凝胶页：254→271 篇。
- [2026-05-09] **Batch Ingest: 15 篇 Eutectogel 文献入库**：通过 Codex + Crossref 批量处理 raw/水凝胶/ 中的 15 篇待处理 JSON。覆盖疏水共晶凝胶(CEJ)、纤维素增强(IJBMC)、交联共晶凝胶传感器(Nat. Commun. 2025)、两性离子双网络(JMCA)、MXene超级电容器(JMCC)、药物透皮(JMCB 2025)、DES凝胶(Green Chem. 2026)等方向。KB水凝胶页：239→254 篇。脚本: `scripts/batch_ingest.py`。

- [2026-05-07] **Deep Read v2 批量：65篇新增精读 + 11篇补入库**：批量处理全部 round 2 剩余文献，覆盖有机水凝胶(15)、Eutectogels(9)、传感器/能源(9)、抗脱水/纤维素(12)、综述(6)、其他(13) 及 11篇补入库。47篇 MiMo 精读成功，28篇无摘要标记。累计精读 76 篇（含 v1）。脚本: `Desktop/deepread_v2.py`。
- [2026-05-07] **v1→v2 升级：11篇精读笔记统一格式**：将第一轮 deep round 的 11 篇 v1 精读笔记全部升级到 v2 格式（原文依据「」+ [推断]标记 + 原文核查表）。至此全部 76 篇精读笔记格式统一。
- [2026-05-07] **Deep Round 2：4 agent 并行搜索 122 篇 + Zotero +91 篇 + KB +105 篇**：4 agent 覆盖①纤维素溶解/改性(6子方向) ②有机水凝胶+Eutectogels(6子方向) ③宽温域应用(6子方向) ④综述+竞争分析。Zotero 602→693 (+91 去重后)，KB 水凝胶 490→595 (+105 笔记)。BibTeX: `Desktop/literature_bib/deep_round2/master_round2.bib`。含 Zheng CSR 2025 竞争分析差异化建议。
- [2026-05-07] **文献扩充：自动检索7大方向+41篇入KB**：全自动完成文献搜索→DOI收集→BibTeX抓取→KB笔记生成。覆盖有机水凝胶(7)、纤维素溶解(3)、Eutectogels(7)、姚建峰组早期(7)、抗脱水(5)、防冰/冷冻保存(3)、传感器应用(5)、剩余导入失败(4)。BibTeX文件存桌面`literature_bib/`。Zotero已升级9.0.2需管理员权限修复。KB水凝胶页：402→443篇。
- [2026-05-07] **cc-deploy v3 打包**：升级一键部署包，新增 29 个学术技能（cnki-/lit-/obsidian/paper-ingest/paper-query/zotero）、deepseek-tui 自动安装配置、替换为猫娘 persona CLAUDE.md，技能总数 62→91
- [2026-05-07] **远程部署尝试**：尝试通过 WinRM 部署新电脑（192.168.3.15），因网络隔离（100.79.x.x → 192.168.x.x）失败，改用本地跑部署包方案
- [2026-05-07] **代码推送中断**：cc-deploy commit 因 LF→CRLF warning 被中断，待重新提交推送
- [2026-05-07] **深度文献扩充+48篇高引论文**：3 agent并行检索（顶级期刊近3年、纤维素溶解基础、抗冻奠基性文献）+ 直接搜索 landmark 论著。覆盖 Nat. Commun.(6)、Science(2)/Sci. Adv.(2)、Adv. Mater.(3)、AFM(3)、Angew. Chem.(3)、CSR(1)、JACS Au(1)、Nat. Mater.(1)、Nature(1)、Prog. Polym. Sci.(1) 等。包含 Gong/Suo DN凝胶、Isogai TEMPO-CNF、Abbott DES、张俐娜NaOH/尿素、刘明杰有机水凝胶等里程碑文献。全部导入 Zotero + KB笔记25篇。Zotero: 541→589，KB: 443→490
- [2026-05-06] **服务器同步**：从服务器（`peach-lover.com`）完整同步 KB wiki（146 篇 arXiv 文献）+ Obsidian vault（227 篇深读笔记），总计 +373 篇。本地文献从 170 → 543 篇。
- [2026-05-06] **paper-ingest 打通**：完成 paper-ingest/paper-query 技能、全局配置、项目 hooks。批量处理 raw/水凝胶/ 中 53 个 JSON 文件。
- [2026-05-06] **服务器架构发现**：OpenClaw 服务器（peach-lover.com）含 KB wiki（146 篇）+ Obsidian vault（314 篇），通过 `accept_literature.py` cron 每日同步 + 飞书通知
- [2026-05-06] **literature-review 仓库**：发现 GitHub 上 617MB 的 `literature-review` 库，含 44 篇 PDF + 60 篇 MD 文献笔记（水凝胶方向）
- [2026-05-06] **全量文献总览**：服务器 KB 146 + Obsidian vault 314 + Zotero 396 + lit-review 44PDF/60MD，知识库基数充足
- [2026-04-30] 知识库初始建立，~82 篇文献笔记

## 当前状态

| 领域 | 文献（.md笔记） | 方向 |
|------|------|------|
| 水凝胶 | 319 篇（87篇精读） | 抗冻、抗脱水、Eutectogels、自修复粘附、防冰/冷冻保存、电子皮肤、纤维素、传感器/能源、执行器/软体机器人、创面敷料 |
| 有机磷化学 | 57 篇 | 手性膦催化剂、C-P键、不对称催化 |
| 化学信息学 | 51 篇 | ML分子建模、AI药物发现 |
| 化工设计竞赛 | 33 篇 | 苯乙烯清洁生产、乙苯脱氢 |

### 精读质量

全部 76 篇精读笔记采用 v2 格式：
- **原文依据**「摘要原句引用」— 每个结论可追溯
- **[推断]** — 推测与事实严格分离
- **原文核查表** — 断言 ↔ 原文支持 ↔ 可信度评级
- 批次含 29 篇无摘要占位（待手动补充）

### 精读脚本

`Desktop/deepread_v2.py` — 全自动精读 pipeline：
1. Semantic Scholar → Crossref 获取摘要
2. MiMo-V2.5-Pro 精读（含原文依据 prompt）
3. 自动验证断言可追溯性
4. 写入 KB wiki 笔记

后续使用：编辑 PAPERS 列表 → `python deepread_v2.py`

### 待处理的 28 篇无摘要论文

已尝试 Semantic Scholar + Crossref 均无摘要，可通过 DOI 内容协商、CORE API 或直读 PDF 补充。 |

## 待办

- 有新 raw 文件时运行 `paper-ingest` 技能
- 每 10-15 篇新文献后调用 paper-lint 健康检查
- 好问答答案归档到 `wiki/问答/`

## 技能快速参考

- `paper-ingest`：raw/ → wiki/ 消化流水线
- `paper-query`：3 层渐进检索（Quick / Standard / Deep）
