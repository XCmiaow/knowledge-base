# 纤维素基宽温域水凝胶 — 最终方案 v6

> **策略：一主一副，先快后强。短线保研快速产出 critical scoping review，长线扩 R1 升级大综述。**

---

## 零、文献真实状态

```
R1  全文精读 (Codex)     3 篇   ← 仅用于说明性案例
R2  摘要级筛查 (MiMo)   111 篇   ← 领域图景、策略分布、摘要报告习惯
R3  仅题录 (无摘要)     140 篇   ← 仅文献池背景
```

**这意味着：** 不能写"comprehensive review"。可以写"critical scoping review + evidence framework proposal"。

---

## 一、短线文章：保研快速产出（4周）

### 基本信息

| 项目 | 内容 |
|------|------|
| **标题** | Beyond Anti-Freezing: A Critical Scoping Review of Functional Evidence in Wide-Temperature Cellulose-Based Gels |
| **类型** | Critical scoping review / framework paper |
| **字数** | 8,000-12,000 words |
| **图表** | 6-8 个 |
| **引用** | 80-120 篇 |
| **首投** | Cellulose（主题最契合） |
| **备投** | Gels（可行性更高）/ Carbohydrate Polymer Technologies and Applications |

### 核心论点（金句×3）

1. **Claimed temperature window ≠ verified functional temperature window.**
   声称的耐受温度窗口 ≠ 已验证的功能温度窗口。

2. **Anti-freezing is not function preservation.**
   不冻结 ≠ 还能导电、传感、自修复、粘附、作为器件运行。

3. **Cellulose is an active regulator of water state, network mechanics, and interfacial interactions — not merely a green label.**
   纤维素不是绿色标签，而是主动调控因子。

### 全文结构（7章，压缩版）

```
1. Introduction (2页)
   - 宽温域凝胶需求
   - 纤维素平台优势
   - 本文不是 comprehensive review，是 critical scoping review + framework

2. Methodology (2页) ★方法核心里程碑
   - R1/R2/R3 分层定义
   - 证据使用边界表
   - 本文不做什么（明确声明）

3. Thermal failure mechanisms (3页)
   - 四路级联失效模型（原创图1）
   - 证据阶梯图：从 anti-freezing claim 到 operational validation（原创图2）
   - "不冻结 ≠ 能工作" 的核心论证

4. Scoping landscape (3页) ★数据章
   - 基于R2=111篇的摘要级统计
   - 年份分布 / 策略分布 / 纤维素类型分布（图3-4）
   - 摘要报告维度覆盖率分析
   - 边界声明：分析的是摘要层面，不是全文级

5. Why cellulose? (3页)
   - 纤维素角色矩阵（表）
   - 纤维素特有贡献 vs 通用水凝胶机制
   - 隐藏代价

6. Design strategies (5页) — 每类按固定模板
   6.1 Salt-based
   6.2 DES/IL ★重点
   6.3 Organohydrogels + anti-drying
   6.4 Network engineering
   每个策略5问：什么失效/什么机制/纤维素贡献/牺牲什么/到什么证据等级

7. Framework and roadmap (3页)
   - DFR 指标（定量 + 定性）
   - E0-E4 证据阶梯
   - 最低报告 checklist（表）
   - 局限性声明

### 图表清单（8个）

编号 | 类型 | 内容 | 优先级
-----|------|------|-------
Fig 1 | 示意图 | 四路级联失效模型 | P0
Fig 2 | 阶梯图 | E0-E4 证据阶梯 | P0
Fig 3 | 统计图 | 策略分布 + 纤维素类型分布 | P0
Fig 4 | 覆盖率图 | 摘要报告维度覆盖率 | P0
Tab 1 | 方法表 | R1/R2/R3 证据使用边界 | P0
Tab 2 | 角色矩阵 | 纤维素5种角色/贡献/风险 | P0
Tab 3 | 策略对比 | 盐/DES/有机/网络：优势/代价/证据等级 | P1
Tab 4 | checklist | 最低报告标准 | P1

### E0-E4 证据阶梯（替代 F0-F4）

等级 | 名称 | 含义 | 常见证据
-----|------|------|---------
E0 | Claim only | 只声称抗冻/宽温域 | 无具体温度或功能数据
E1 | Structural survival | 结构存活 | DSC、弯曲照片、形貌
E2 | Post-thaw recovery | 回温功能恢复 | 解冻后电导/力学恢复
E3 | In-situ low-T function | 低温原位功能 | -T 下电导/GF/力学实测
E4 | Operational validation | 操作验证 | 循环+时长+器件+原位运行

### DFR = Demonstrated Functional Retention

**定量 DFR：**
- DFR_σ = σ_T / σ_RT × 100%
- DFR_GF = GF_T / GF_RT × 100%
- DFR_adhesion = A_T / A_RT × 100%

**定性 DFR：**
- DFR-0：只声称，无功能测试
- DFR-1：冷冻后结构保持，无功能
- DFR-2：冷冻后回温功能恢复
- DFR-3：低温原位功能可用
- DFR-4：低温原位功能 + 循环/长期稳定

### 最低报告 checklist

项目 | 必须报告
-----|---------
温度窗口 | claimed T 和 tested T 分开
功能测试 | 室温 + 低温原位
时间 | 低温暴露时长
循环 | 冻融循环次数
水/溶剂含量 | 初始和测试后
导电/传感 | σ, GF, 响应时间, 滞后，测试温度
力学 | 强度, 拉伸, 韧性, 测试温度
粘附/自修复 | 测试温度, 基底, 恢复率
器件 | 是否原位运行（非回温后运行）
安全性 | 盐/DES/有机溶剂泄漏/毒性/腐蚀性

### 必须避免的三句话

| ❌ 不写 | ✅ 改写 |
|---------|--------|
| "We analyzed 254 papers" | "We mapped 254 literature records at different evidence depths" |
| "The field does not report low-temperature functional data" | "At the abstract level, functional-retention metrics are not consistently visible" |
| "This review comprehensively summarizes" | "This critical scoping review maps the field and proposes a functional-evidence framework" |

### 4周执行时间表

```
Week 1: R2摘要表 + 4张图
  - 提取111篇R2的字段（DOI, year, journal, cellulose_type, strategy, 
    application, 摘要是否含温度/电导/力学/GF/自修复/粘附/抗干燥/可持续）
  - 生成：年份分布、策略分布、纤维素类型分布、摘要报告覆盖率

Week 2: Ch2+Ch3+Ch4
  - 方法论（R1/R2/R3 + 证据边界表）
  - 热失效机制（四路级联失效模型 + E0-E4阶梯）
  - Scoping图景（Week 1的4张图 + 文字分析）

Week 3: Ch5+Ch6
  - Why cellulose（角色矩阵）
  - Design strategies（盐/DES/有机/网络，每类5问模板）

Week 4: Ch7 + 全稿修缮
  - Framework（DFR + checklist + 路线图）
  - 画 Fig 1, Fig 2 终稿
  - Abstract + Graphical Abstract + Cover Letter
  - 语言降噪 + 全文一致性检查
```

---

## 二、长线升级路线：未来大综述

### 触发条件
R1 从 3 篇扩到 ≥25 篇（每类策略 4-8 篇全文级案例）

### 升级目标
- **期刊：** Carbohydrate Polymers / Advanced Functional Materials
- **类型：** Comprehensive critical review
- **篇幅：** 15,000-20,000 words，12-15 图表，150-200 引用
- **时间：** 短线上线后 2-4 个月

### 升级内容
| 短线版本 | 升级为大综述 |
|---------|------------|
| R1=3，说明性案例 | R1≥25，代表性样本 |
| 摘要层面报告习惯 | 全文级功能数据库 |
| 定性策略对比 | 定量 Pareto 分析 |
| E0-E4 + DFR 框架 | + 全文级策略间横向性能对比表 |

---

## 三、投稿策略

| 轮次 | 期刊 | ISSN | 类型 | 理由 |
|------|------|------|------|------|
| 首投 | **Cellulose** | 1572-882X | 细分顶刊 | 主题最契合，综述形式合理 |
| 二投 | **Gels** | 2310-2861 | MDPI开放获取 | 范围匹配，速度快 |
| 三投 | **Carbohydr. Polym. Technol. Appl.** | 2666-8939 | 新刊 | 保底 |
| 升级 | **Carbohydrate Polymers** | 0144-8617 | 领域顶刊 | R1扩后投稿 |

---

*版本 v6 Final | 一主一副双线策略 | 保研快速 + 长期升级*
