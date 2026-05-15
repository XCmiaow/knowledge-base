# 纤维素基宽温域水凝胶综述执行方案 v7 Deep Review

> 结论先行：v6 的战略方向是对的，但必须把文章从“大综述框架”压实为“critical scoping review + reporting framework”。短线稿的核心卖点不是全面总结所有抗冻水凝胶，而是用结构化数据证明领域存在 claims-evidence gap，并提出功能保持证据框架。

---

## 0. v7 修订原则

### 一句话定位

**From anti-freezing claims to functional retention evidence: a critical scoping review of cellulose-based wide-temperature gels.**

### v6 的保留项

| 模块 | 判断 | 处理 |
|---|---|---|
| “不冻结不等于能工作” | 核心贡献成立 | 保留为全文主线 |
| E0-E4 证据阶梯 | 很强，适合作为框架产出 | 保留并前置 |
| DFR 指标 | 有原创性，但不能过度量化 | 保留为建议性框架 |
| Cellulose 首投 | 方向合理 | 需要让题目、摘要、图表都突出纤维素贡献 |
| 长线升级大综述 | 有价值 | 从短线稿中拆出去，作为后续路线 |

### v6 的必须修正项

| 风险 | v6 问题 | v7 修正 |
|---|---|---|
| 数据口径混乱 | `R2=111/R3=140` 与当前 `174/156/171` 不一致 | 拆分为 discovery pool、structured scoping set、primary analysis set、full-text exemplar set |
| 证据过度解释 | 容易把“摘要未报告”写成“全文没有数据” | 全文统一写成 “at the abstract/record level, not consistently visible” |
| 文章太像大综述 | 机制、策略、应用都想展开 | 结果章和方法章前置，设计策略只做解释性讨论 |
| Cellulose 贡献证据不足 | “纤维素是主动调控因子”需要证明 | 用角色矩阵表达为假设框架，不当作已被所有文献证明的结论 |
| 期刊策略略粗 | Gels 速度快但品牌风险，CARPTA 与 carbohydrate scope 更强 | 推荐 `Cellulose -> CARPTA -> Gels`，若保研硬截止再切换速度路线 |

---

## 1. 深度评估

### 总体评分

| 维度 | 评分 | 评价 |
|---|---:|---|
| 选题价值 | 8.5/10 | “抗冻声明”和“低温功能保持证据”之间的落差是真问题，比普通材料罗列更有论文感 |
| 数据基础 | 7/10 | 已有 174 条结构化记录，足够支撑 scoping landscape，但不足以支撑 comprehensive review |
| 原创性 | 8/10 | E0-E4、DFR、reporting checklist 是真正可交付的原创框架 |
| 可投性 | 7/10 | Cellulose 可试，但必须突出 cellulose，而不是泛泛水凝胶 |
| 四周完成可行性 | 6.5/10 | 可完成首稿，但前提是本周冻结数据和图表，不能继续扩张范围 |
| 最大风险 | 高 | 口径不一致和 overclaim 会直接削弱可信度 |

### 战略判断

短线稿不要再追求 “Progress in Polymer Science / AFM style review”。那条路线需要 25-40 篇全文级精读、跨策略定量性能表和更系统的机理证据。现在最聪明的打法是把现有数据变成一篇有方法、有图、有框架的 critical scoping review。

短线稿的审稿人要被说服三件事。

1. 这个领域确实大量声称 wide-temperature / anti-freezing。
2. 这些声明在摘要和题录层面经常缺少功能保持证据。
3. 纤维素基体系需要一个更清楚的证据等级和最低报告标准。

---

## 2. 数据口径统一

### v7 采用的唯一主数据源

主数据源：`r2_scoping_database_v2.csv`。

派生统计：`scoping_results.json`。

旧版 `r2_scoping_database.csv` 缺少 `has_cellulose`、`arch_layer`、`solvent_layer`、`network_layer` 等字段，只作为历史版本保留，不再用于正文统计。

### 四层语料定义

| 层级 | 名称 | 当前数量 | 用途 | 正文表述边界 |
|---|---|---:|---|---|
| D0 | Discovery pool | 约 314 条 | 说明检索和积累规模 | 只能写 “candidate records / literature pool”，不做统计结论 |
| D1 | Structured scoping set | 174 条 | 摘要级和题录级编码 | 可做方法流程、敏感性说明 |
| D2 | Primary analysis set | 156 条 cellulose-relevant | 主要统计图和结果章 | 正文核心数据集 |
| D3 | Full-text exemplar set | 3 篇 | 解释性案例 | 只能用于 case illustration，不能代表全领域 |

### 必须废弃或降级的旧口径

`R2=111` 如果来自早期 MiMo 子集，就只能称为 pilot subset，不再作为正文统计母数。

`R3=140` 可以作为 discovery pool 的 “metadata-only records”，不能和 D1/D2 混在同一张统计图里。

正文中不要写 “we analyzed 254 papers”。更安全的写法是：

> We mapped a candidate pool of approximately 314 literature records and performed structured abstract-level coding on 174 records, among which 156 cellulose-relevant records formed the primary analysis set.

### 当前 D2 核心结果

| 结果 | D2 数值 | 可写成的论文结论 |
|---|---:|---|
| 声称宽温域/抗冻 | 130/156 = 83.3% | wide-temperature claims are widespread |
| 报告具体温度值 | 55/156 = 35.3% | specific temperature conditions are much less consistently visible |
| 报告零下温度 | 39/156 = 25.0% | subzero validation is visible in only a minority of records |
| 提及电导 | 75/156 = 48.1% | conductivity is frequently mentioned |
| 报告电导数值 | 22/156 = 14.1% | quantitative conductivity data are much less visible |
| 提及 GF/应变灵敏度 | 53/156 = 34.0% | sensing metrics appear often |
| 报告 GF 数值 | 10/156 = 6.4% | quantitative sensing metrics are sparse |
| 报告粘附数值 | 4/156 = 2.6% | adhesion is especially under-quantified |
| 任一非力学功能指标 | 39/156 = 25.0% | non-mechanical functional evidence is not consistently visible |
| 任一定量性能指标 | 69/156 = 44.2% | even broad quantitative reporting remains incomplete at record level |

### 结果解读边界

这些数字不能证明“文献全文没有数据”。它们只能证明“在摘要级记录中，功能保持证据没有稳定可见”。这个限制必须在 Methods、Results、Discussion 和 Conclusion 里重复保持一致。

---

## 3. 修订后的论文定位

### 推荐标题

**From Anti-Freezing Claims to Functional Retention: A Critical Scoping Review of Cellulose-Based Wide-Temperature Gels**

### 备选标题

| 标题 | 适合场景 | 风险 |
|---|---|---|
| Beyond Anti-Freezing: Evidence Visibility and Functional Retention Framework for Wide-Temperature Cellulose-Based Gels | 更强调框架贡献 | “Beyond” 略像观点文 |
| From Anti-Freezing Claims to Functional Retention: A Critical Scoping Review of Cellulose-Based Wide-Temperature Gels | 最稳，适合 Cellulose | 稍长但清楚 |
| Do Wide-Temperature Cellulose Gels Really Work? A Critical Scoping Review of Claims, Metrics, and Reporting Standards | 更有传播性 | 对传统期刊略显挑衅 |

推荐用第二个。它同时包含 claims、functional retention、critical scoping review、cellulose-based gels，审稿人一眼能看懂边界。

### 核心论点

1. **Claimed temperature windows are not equivalent to verified functional temperature windows.**
2. **Anti-freezing should be evaluated as functional retention, not only structural survival.**
3. **Cellulose-based gels need evidence-aware reporting because cellulose can alter water state, network mechanics, and interfacial behavior, while its exact role is often under-specified.**

第三条要比 v6 更谨慎。不要写 “cellulose is always an active regulator”。更稳的说法是 “cellulose can act as an active regulator, but the role is often insufficiently resolved in current reporting”。

### 摘要骨架

> Cellulose-based gels are increasingly reported as wide-temperature or anti-freezing soft materials for sensors, energy devices, biomedical interfaces, and flexible electronics. However, claimed temperature tolerance does not necessarily demonstrate retained function under the claimed conditions. Here, we perform a critical scoping review of cellulose-relevant wide-temperature gel records and code the visibility of temperature conditions, subzero validation, and functional metrics. In the primary analysis set of 156 cellulose-relevant records, 83.3% claimed wide-temperature or anti-freezing behavior, whereas only 35.3% reported a specific temperature value and 25.0% visibly reported subzero validation. Quantitative functional metrics were even less consistently visible, including conductivity values in 14.1%, gauge-factor values in 6.4%, and adhesion values in 2.6% of records. We therefore propose an evidence ladder from claim-only anti-freezing to operational low-temperature validation, together with demonstrated functional retention metrics and a minimum reporting checklist. This review reframes anti-freezing cellulose gels from a materials survival problem into a functional-evidence problem.

---

## 4. 修订后的全文结构

### 建议结构

| 章节 | 标题 | 页数 | 功能 |
|---|---|---:|---|
| 1 | Introduction: from anti-freezing claims to functional evidence | 2 | 建立问题和贡献 |
| 2 | Scope, corpus construction, and coding framework | 2 | 解决可信度问题 |
| 3 | Evidence visibility landscape in cellulose-based wide-temperature gels | 4 | 文章核心结果 |
| 4 | Why cellulose matters, and why its role is hard to infer | 3 | 绑定 Cellulose 期刊 |
| 5 | Strategy-function coupling: salts, DES/IL, organohydrogels, and networks | 4 | 解释机制与设计启示 |
| 6 | Functional retention framework and reporting checklist | 3 | 输出原创框架 |
| 7 | Outlook and limitations | 1 | 降低 overclaim 风险 |

### 与 v6 的关键差异

v6 把 “thermal failure mechanisms” 放得太靠前，容易让稿子像传统综述。v7 把 “scoping results” 前置，让文章先证明问题，再解释机制。

v6 的 Design strategies 可以保留，但不能写成四个完整综述章节。短线稿只需要回答：每种策略如何影响 functional retention 的证据等级，以及目前摘要级报告里缺什么。

### 每章写作要点

#### 1. Introduction

不要从“水凝胶很重要”写太久。第一段就引出 wide-temperature claims 的增长，第二段指出 anti-freezing 与 functional retention 的差异，第三段说明 cellulose-based systems 的特殊性，第四段给出本文贡献。

#### 2. Methods

必须写得像一篇有方法的文章，而不是随笔式综述。最低要交代检索来源、纳入标准、排除标准、编码字段、AI/人工辅助流程、主分析集和敏感性分析。

#### 3. Results

这是短线稿的硬核。建议按四个结果组织：

1. Dataset composition and cellulose identity ambiguity。
2. Claims vs temperature reporting gap。
3. Functional metric visibility gap。
4. Strategy/application-dependent reporting patterns。

#### 4. Why cellulose matters

这章为 Cellulose 期刊服务。不要泛泛讲绿色材料，要讲纤维素可能参与三类机制：水状态调控、网络力学增强、界面相互作用。然后补一句：当前摘要层面常常不能区分 cellulose 是 active regulator、reinforcement filler 还是 green label。

#### 5. Strategy-function coupling

四类策略都用同一个模板。

| 模板问题 | 写法 |
|---|---|
| 解决什么热失效 | freezing, drying, brittleness, ion-transport collapse |
| 靠什么机制 | salt colligative effect, DES hydrogen-bond competition, solvent substitution, network reinforcement |
| cellulose 贡献在哪里 | water binding, nanofiber reinforcement, dissolution/regeneration, interface |
| 牺牲什么 | conductivity, mechanics, toxicity, corrosion, viscosity, dehydration |
| 到什么证据等级 | E0-E4 |

#### 6. Framework

把 E0-E4、DFR 和 minimum reporting checklist 组合成本文最终产物。框架要让读者觉得可以直接拿去评价下一篇论文。

---

## 5. 图表包重排

### P0 图表

| 编号 | 类型 | 内容 | 目的 |
|---|---|---|---|
| Fig 1 | corpus flow diagram | D0/D1/D2/D3 语料边界和纳入排除流程 | 先解决可信度 |
| Fig 2 | evidence funnel | 83.3% claims -> 35.3% temperature value -> 25.0% subzero -> 14.1% conductivity value -> 6.4% GF value | 一张图打出主结论 |
| Fig 3 | heatmap | strategy/application x metric visibility | 展示不是简单缺数据，而是有报告偏差 |
| Fig 4 | cellulose role map | cellulose as water-state regulator / network scaffold / ionic environment modulator / interface mediator / sustainability carrier | 绑定期刊主题 |
| Fig 5 | failure cascade | freezing -> structure -> ion transport -> mechanics -> interface -> device failure | 支撑“功能保持”概念 |
| Fig 6 | E0-E4 + DFR framework | 从 claim 到 operational validation | 原创框架产出 |

### P0 表格

| 编号 | 内容 | 目的 |
|---|---|---|
| Table 1 | D0/D1/D2/D3 语料定义和证据使用边界 | 防止 overclaim |
| Table 2 | coding codebook | 方法可复现 |
| Table 3 | minimum reporting checklist | 输出可引用工具 |

### P1 图表

| 编号 | 内容 | 使用条件 |
|---|---|---|
| Fig S1 | 年份分布 | 若年份字段清洗完成 |
| Fig S2 | cellulose type distribution | 若 `Unspecified` 的解释写清楚 |
| Table S1 | full coded database | 作为补充材料 |
| Table S2 | 3 篇 R1 说明性案例 | 不进入主统计 |

### 图表优先级判断

四周内先做 Fig 1、Fig 2、Fig 6 和 Table 1。没有这四个，文章没有骨架。Fig 3 和 Fig 4 是加分项。Fig 5 可以晚一点画，因为它是概念支持图，不是核心数据图。

---

## 6. 方法学补强

### 必须增加的 Methods 内容

1. **Search and corpus construction**：说明候选池来源、时间范围、关键词组合和去重规则。
2. **Eligibility criteria**：定义 cellulose-relevant、wide-temperature/anti-freezing、gel-based material。
3. **Evidence-depth classification**：定义 D0/D1/D2/D3。
4. **Coding schema**：列出 temperature、subzero、conductivity、GF、self-healing、adhesion、anti-drying、sustainability 等字段。
5. **Primary and sensitivity analysis**：主分析用 D2=156，敏感性可报告 D1=174。
6. **Limitations of abstract-level coding**：明确全文级数据缺失不等于全文没有数据。

### 建议加入的质量控制

| 检查 | 最小做法 |
|---|---|
| 重复记录 | DOI 去重，缺 DOI 用标题规范化去重 |
| cellulose 相关性 | 抽查 `has_cellulose=NO` 的 18 条，确保排除合理 |
| strategy 多标签 | 保留三层编码 `arch_layer/solvent_layer/network_layer`，不要只依赖单一 `strategy` |
| 数值抽取 | 对 reports/value 字段抽查 20 条原摘要 |
| R1 案例 | 3 篇全文案例只做 narrative check |

### Methods 可直接使用的短句

> Because the review was designed to map evidence visibility rather than extract all full-text performance values, absence of a metric in the coded record was interpreted as “not visible at the abstract/record level” rather than “not reported in the full text.”

这句话必须保留。它是防止审稿人攻击的护栏。

---

## 7. 期刊策略修订

### 首推路线

| 轮次 | 期刊 | 推荐程度 | 适配条件 | 主要风险 |
---|---|---:|---|---|
| 1 | Cellulose | 高 | 标题、摘要、Fig 4 都必须突出 cellulose contribution | 若写成泛水凝胶综述，容易被认为偏离 scope |
| 2 | Carbohydrate Polymer Technologies and Applications | 高 | title 和 abstract 明确 cellulose/carbohydrate 是中心成分 | APC 较高，且必须突出 carbohydrate component |
| 3 | Gels | 中高 | 如果保研时间压力大，或稿件更偏 gel application | MDPI 品牌评价因导师和学院而异 |

### 期刊定位依据

Cellulose 官方 scope 明确欢迎 cellulose 的 physics、chemistry、biochemistry、materials science，并列出 sensors、materials、biological/medical、energy 等应用，同时对 Review 的定义是 “critical evaluation” 而不是罗列文献。因此 Cellulose 是最适合的首投，但稿件必须以 cellulose 为中心。

Carbohydrate Polymer Technologies and Applications 要求 title 和 abstract 显式出现核心 carbohydrate-containing molecule，并强调 carbohydrate component 对性质或应用的贡献。因此它适合作为强备投，但题目必须保留 cellulose-based。

Gels 明确接收 review papers，范围包含 hydrogels、organogels、ionic gels 和 practical applications。它速度与范围友好，但投稿前要和导师确认 MDPI 接受度。

### 两条投稿路线

#### 路线 A：稳健保研路线

Cellulose -> Carbohydrate Polymer Technologies and Applications -> Gels。

适合目标是“简历质量优先，兼顾可行性”。

#### 路线 B：速度优先路线

Gels special issue / regular review -> Carbohydrate Polymer Technologies and Applications。

适合目标是“必须尽快拿到接收或至少外审记录”。这条路线要提前确认 APC 和导师态度。

### 不建议短线首投

Progress in Polymer Science、Advanced Functional Materials、Carbohydrate Polymers 暂不适合短线首投。原因不是选题不够好，而是当前 R1 全文级证据不足，短线稿更像 scoping/framework paper，不是 150-200 篇全文级综合大综述。

---

## 8. 四周执行计划 v7

### Week 0.5：数据冻结和口径修复

目标：不再扩张文献池，冻结 D1/D2 数据。

验证：

- `r2_scoping_database_v2.csv` 行数为 174。
- D2 主分析集为 `has_cellulose=YES` 的 156 条。
- `scoping_results.json` 与 CSV 重新核对一致。
- 旧口径 `R2=111` 不再进入正文主统计。

交付：

- Table 1：语料层级和证据边界。
- Table 2：coding codebook。
- Fig 1：corpus flow。

### Week 1：核心结果图

目标：把主结论图画出来。

验证：

- Fig 2 能单独说明 claims-evidence gap。
- Fig 3 能说明 reporting visibility 与 strategy/application 相关。
- 所有图注都写明 “primary analysis set, n=156”。

交付：

- Fig 2 evidence funnel。
- Fig 3 heatmap。
- Results 章 bullet outline。

### Week 2：Methods + Results 初稿

目标：先写最像论文的部分。

验证：

- Methods 能回答“你怎么选文献、怎么编码、这些数字从哪来”。
- Results 不出现 “full text lacks data” 这类过度推断。
- 每个百分比都能回到 CSV 或 JSON。

交付：

- Section 2 完整草稿。
- Section 3 完整草稿。

### Week 3：Discussion + Framework

目标：把数据结果解释成领域贡献。

验证：

- Discussion 不变成普通综述。
- 每个 strategy 都围绕 evidence level 和 functional retention 写。
- E0-E4 和 DFR 能形成一张可引用的 framework 图。

交付：

- Section 4-6 草稿。
- Fig 4、Fig 5、Fig 6。
- Table 3 checklist。

### Week 4：语言、投稿包和一致性检查

目标：形成可给导师看的完整稿。

验证：

- 摘要、引言、结论的贡献表述一致。
- 全文没有混用 D0/D1/D2/D3 数字。
- 不出现 comprehensive review、meta-analysis、first-ever 等高风险词。

交付：

- 完整 manuscript draft。
- Graphical abstract 草图。
- Cover letter。
- Supplementary table。

---

## 9. Go / No-Go 标准

### 可以继续写短线稿的条件

| 条件 | 标准 |
---|---|
| 数据冻结 | D2=156 能稳定复现 |
| 图表成立 | Fig 2 的 claims-evidence gap 足够清楚 |
| 方法可信 | coding schema 能解释每个字段 |
| Cellulose 主题明确 | 至少一章和一张图专门讨论 cellulose role |
| 语言克制 | 全文只声称 abstract/record-level visibility |

### 暂停并补数据的条件

| 信号 | 处理 |
|---|---|
| 156 条里大量不是 cellulose-based gels | 重筛 primary set |
| 年份字段缺失太多 | 年份图降级到补充或删除 |
| strategy 多标签混乱 | 用三层编码替代主策略分布 |
| R1 只有 3 篇且案例不足以支撑策略讨论 | 策略章进一步缩短，只保留解释性段落 |
| 导师强烈要求一区大综述 | 切换到长线 R1 扩展路线 |

---

## 10. 立刻要做的五件事

1. 冻结 `r2_scoping_database_v2.csv` 为 master database。
2. 写 `Methods`，不要先写 Introduction。
3. 生成 Fig 1、Fig 2、Table 1、Table 2。
4. 把所有 “R2=111” 改成 “early pilot subset”，正文不用。
5. 给导师展示一页 summary：研究问题、D2=156、主发现、E0-E4 框架、目标期刊。

---

## 11. 禁用表达和替代表达

| 禁用 | 替代 |
|---|---|
| This comprehensive review summarizes... | This critical scoping review maps... |
| We analyzed 254 papers... | We mapped a candidate pool and coded 174 structured records... |
| The field lacks low-temperature data... | Low-temperature functional metrics were not consistently visible at the abstract/record level... |
| Cellulose is always an active regulator... | Cellulose can act as a regulator, but its exact role is often under-specified... |
| This is the first review... | This review reframes anti-freezing gels through functional evidence visibility... |
| DES is the best strategy... | DES appears promising where solvent reconstruction, ion transport, and cellulose processing are coupled... |

---

## 12. 最终 v7 方案

### 短线稿

| 项目 | 内容 |
|---|---|
| 类型 | Critical scoping review / reporting framework |
| 推荐标题 | From Anti-Freezing Claims to Functional Retention: A Critical Scoping Review of Cellulose-Based Wide-Temperature Gels |
| 主数据集 | D2 primary analysis set, n=156 cellulose-relevant records |
| 支撑数据 | D1 structured scoping set, n=174 |
| 案例数据 | D3 full-text exemplar set, n=3 |
| 目标字数 | 8,000-10,000 words |
| 图表 | 6 figures + 3 tables |
| 首投 | Cellulose |
| 备投 | Carbohydrate Polymer Technologies and Applications, Gels |
| 核心贡献 | claims-evidence gap + E0-E4 evidence ladder + DFR/reporting checklist |

### 长线稿

短线稿投出后，再启动 R1 扩展。目标是每类策略至少 4-8 篇全文级案例，总 R1 达到 25-40 篇。那时再升级为 comprehensive critical review，目标 Carbohydrate Polymers 或 Advanced Functional Materials。

### 版本判断

v7 比 v6 少了一点野心，但更像能真实投稿的文章。它把“我读了很多文献”改成“我发现了一个可证明的报告和证据问题”，这才是短线最强的打法。

---

## 参考核查

- Cellulose scope and review definition: https://link.springer.com/journal/10570/aims-and-scope
- Gels aims and accepted article types: https://www.mdpi.com/journal/gels/about
- Carbohydrate Polymer Technologies and Applications scope: https://www.sciencedirect.com/journal/carbohydrate-polymer-technologies-and-applications

核查日期：2026-05-14。
