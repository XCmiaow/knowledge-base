# R1 核心文献核验表 v0

> 状态说明：本表是基于本地深读笔记与 `r2_scoping_database_v2.csv` 的 R1 骨架核验 v0，不等同于 PDF 全文逐图核验。下一轮只需要回全文确认低温原位测试、循环/时长和器件运行细节。

## 结论

首批真正适合作为 cellulose core R1 的文献应以纤维素、CMC、CNF、CNC 或 regenerated cellulose 明确参与网络/功能构建为准。

前一版候选队列中有少数淀粉或纯 PAA 体系，适合当 comparator，不应放进 cellulose core R1 主案例。

## 12 篇核心骨架

| # | DOI | 体系角色 | 策略 | 关键低温/功能证据 | 初判等级 | 下一步核验 |
|---:|---|---|---|---|---|---|
| 1 | `10.1016/j.ijbiomac.2024.131129` | cellulose-based eutectogel | DES 溶纤 + PAAm 聚合 + 离子导电 | `-80 °C` 抗冻；20 °C 电导 `1.64 S/m`；GF `5.4`；透明、自愈、多刺激传感 | E3? | 回正文确认传感/电导是否在 `-80 °C` 原位测试 |
| 2 | `10.1016/j.carbpol.2024.122939` | natural cellulose reinforced eutectogel | cotton cellulose nanofiber + DES + 多功能表皮电极 | 温区 `-40 to 80 °C`；电导 `1.22 S/m`；黏附 `1562.2 kPa`；自愈约 `80%` | E3? | 回正文确认宽温区间下的器件信号是否原位稳定 |
| 3 | `10.1016/j.carbpol.2024.121932` | CNC@PANI conductive hydrogel | CNC 导电增强 + 自愈/黏附/保湿 | `-60 to 80 °C`；GF `1.68`；响应 `96 ms`；`>10,000` cycles motion detection under harsh temperature | E4 | 核验循环是否覆盖低温原位、是否有室温基线 |
| 4 | `10.1016/j.carbpol.2025.123253` | CNF-reinforced zwitterionic poly(ionic liquid) organohydrogel | glycerol/water + ZILs + Fe3+ + CNF | `-20 to 50 °C` 传感稳定；电导 `2.99 mS/cm`；GF `4.86`；自恢复约 `88%` | E3 | 核验低温循环、信号漂移和抗干燥时长 |
| 5 | `10.1002/app.58040` | CMC/PVA/PANI conductive hydrogel | 双网络 + PANI 导电 + 抗冻 | 室温电导 `2 S/m`；`-12 °C` 电导 `0.86 S/m`，伸长率 `>300%` | E3 | 核验传感测试是否在 `-12 °C` 原位进行 |
| 6 | `10.1016/j.ijbiomac.2025.147477` | CMC-Na/PVA composite hydrogel | EG/H2O + LiCl + clove oil | `-50 °C` 保持柔性和导电；电导 `6.94 S/m`；抗菌；人体运动监测 | E3 | 核验 `-50 °C` 是否有传感原位输出和循环 |
| 7 | `10.1016/j.carbpol.2024.122271` | zwitterionic CNF hydrogel | non-freezable water + Zn coordination | `-40 °C` 下韧性 `10.8 MJ/m3`、自愈 `98.9%/30 min`、电导 `2.9 S/m` | E3 | 核验是否有冻融循环和器件运行 |
| 8 | `10.1021/acsami.2c21617` | CMC/PAA/Fe3+/LiCl hydrogel | IPN + LiCl + Fe3+ + SLS-Fe 快速制备 | 超级电容 `-23 °C` 比电容 `83.16 F/g`，为 25 °C 的 `68%`；传感 GF `6.19` | E4 | 核验传感与储能两类器件的循环/倍率条件 |
| 9 | `10.1016/j.ijbiomac.2023.126550` | cellulose/PAA composite hydrogel | AlCl3/ZnCl2 溶纤/催化 + 双网络 | `-45 °C`；电导 `2.70 S/m`；重量保持率 `90%` | E3 | 核验低温压缩/传感是否原位，是否有长期稳定 |
| 10 | `10.1016/j.ijbiomac.2025.149374` | CMC/phytic acid hydrogel sensor | CMC + PA + 多动态交联 + 抗菌 | `-20 °C` 保持柔性和导电；电导 `1.45 S/m`；GF `2.13`；呼吸监测 | E3 | 核验呼吸监测是否低温原位，确认生物应用边界 |
| 11 | `10.1016/j.ijbiomac.2024.131115` | cellulose-reinforced eutectogel | DES 保留 + photopolymerization + Al3+/H-bond crosslinks | 自黏附 `52.1 kPa`；自愈；离子导电；低温窗口摘要层面不明确 | E1/E2 | 回正文确认是否有明确低温功能数据；若无，作为 reporting-gap 案例 |
| 12 | `10.1016/j.jcis.2024.05.102` | cellulose/PAM solid-state electrolyte | AlCl3/ZnCl2 室温溶纤 + AM 原位聚合 | `-45 °C` 抗冻；电导 `1.99 S/m`；超级电容面积比电容 `203.80 mF/cm2` | E3? | 核验超级电容是否在低温下测试，若只有材料抗冻则降级 |

## Comparator 文献

这些文献可以用于机制对照或设计策略解释，但不放进 cellulose core R1 主案例。

| DOI | 原因 | 用法 |
|---|---|---|
| `10.1016/j.ijbiomac.2022.06.011` | starch-based hydrogel，不是 cellulose core | 可作天然多糖 + Salt/DES/DN 策略对照 |
| `10.1016/j.ijbiomac.2023.129068` | starch/PAM organohydrogel，不是 cellulose core | 可作 glycerol organohydrogel 传感对照 |
| `10.3390/ma14206165` | hydrophobic associated PAA hydrogel，不是 cellulose core | 可作 glycerol anti-freezing/self-healing 机制参照 |

## E0-E4 案例表 v0

| 等级 | 当前案例 | 证据状态 |
|---|---|---|
| E0 Claim only | 暂不从核心 12 篇中选 | 后续从 C 类或摘要缺数据文献中补 |
| E1 Structural survival | `10.1016/j.ijbiomac.2024.131115` | 有 DES/eutectogel 体系与力学/黏附证据，但摘要层面低温功能不明确 |
| E2 Post-thaw recovery | 暂缺稳定代表 | 下一轮从自愈/冻融文献中找“解冻后恢复”案例 |
| E3 In-situ low-T function | `10.1016/j.carbpol.2024.122271`; `10.1016/j.ijbiomac.2023.126550`; `10.1016/j.ijbiomac.2025.147477` | 有低温下导电、力学或传感指标，但器件运行/循环强度需回正文确认 |
| E4 Operational validation | `10.1016/j.carbpol.2024.121932`; `10.1021/acsami.2c21617` | 有循环或器件级低温性能保持，是短线稿最重要的高等级案例 |

## 下一步

1. 优先回全文核验 #1、#2、#3、#8。
2. 每篇只抽取：tested temperature、in-situ function、room-temperature baseline、cycle/duration、trade-off。
3. 若不能确认低温原位功能，不删除文献，而是降级到 E1/E2/reporting-gap 案例。
