# latex-templates

_Last updated: 2026-04-30 | 0 active memories, 0 total_

---

## 模板清单

| 目录 | 模板 | 核心文件 | 场景 |
|------|------|---------|------|
| `njfu-course-paper/` | NJFU 课程论文 | `NJFUReport.sty` + `main.tex` | **水课期末论文（默认）** |
| `elegantbook/` | ElegantBook v4.6 | `elegantbook.cls` | 中文教材/笔记/知识库 |
| `kaobook/` | kaobook | `kaobook.cls` + `kao.sty` | 英文学术专著/论文 |
| `colorist/` | colorist 系列 | `lebhart.cls` / `beaulivre.cls` | 彩色笔记/实验报告 |
| `elegant-notebook/` | Elegant Notebook | `elegant-notebook.tex` | 17配色×7字体 |
| `naelquin-templates/` | NaelQuin 6 件套 | penrose/salam/dirac/... | 通用文章到专著 |

---

## NJFU 课程论文写作工作流（默认水课模板）

### 1. 起步：从模板复制
```
cp -r E:\工作区\latex-templates\njfu-course-paper\  目标目录/
```
或直接在原模板 `main.tex` 上改。

### 2. 填封面字段
修改 `main.tex` 中以下内容：
- `\reportheader{...}` — 页眉
- `\reporttitle{...}` — 封面标题
- `\coursename{...}` / `\college{...}` / `\majorname{...}` / `\studentid{...}` / `\studentname{...}` / `\teachername{...}`
- `\reportdate{...}` — 日期
- `\cabstract{...}` / `\ckeywords{...}` — 中文摘要
- `\etitle{...}` / `\eabstract{...}` / `\ekeywords{...}` — 英文摘要

### 3. 写正文
标准结构：
- 引言（背景、问题、目的）
- 资料来源与研究框架（方法、数据来源）
- 结果与分析（核心内容）
- 讨论（解读、局限性、启示）
- 结论

### 4. 数据 → 三线表
**原则**：所有表格用 `booktabs` 三线表格式（`\toprule` / `\midrule` / `\bottomrule`），禁止竖线。

模板：
```latex
\begin{table}[htbp]
\centering
\caption{表格标题}
\label{tab:xxx}
\begin{tabular}{lcc}
\toprule
\textbf{指标} & \textbf{数值} & \textbf{来源} \\
\midrule
数据行1 & 100 & 文献\cite{ref1} \\
数据行2 & 200 & 文献\cite{ref2} \\
\bottomrule
\end{tabular}
\end{table}
```

**信息密度要求**：合并同类指标、对齐数值的小数位数、加粗关键列头。表格应自成一体——不看正文也能理解。

### 5. 数据 → SCI 风格图片
**原则**：用 Python（matplotlib/seaborn）生成 PDF 矢量图，符合科研规范。

规范：
- 字体：Times New Roman 或 Arial，字号 ≥8pt
- 分辨率：矢量 PDF 优先，位图 ≥300 dpi
- 配色：色盲友好（viridis / cividis / plasma）
- 坐标轴：标签有单位，刻度向内
- 图例：不放图内空间，放图外右上或下方
- 无 chartjunk：不必要的背景/阴影/3D 全去掉
- 尺寸：单栏 ~8cm 宽，通栏 ~16cm 宽，高宽比 0.6–0.75

Python 模板：
```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

fig, ax = plt.subplots(figsize=(6, 4))  # 单栏宽度
# ... plot ...
ax.set_xlabel('X Label (unit)')
ax.set_ylabel('Y Label (unit)')
ax.legend(frameon=False, fontsize=8)
fig.savefig('img/figure_name.pdf', format='pdf')
plt.close()
```

图片引用：
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{img/figure_name.pdf}
\caption{图片标题（描述 what/where/when，不写结论）}
\label{fig:xxx}
\end{figure}
```

### 6. 参考文献
用 `thebibliography` 手写格式，不需要 bib 文件：
```latex
\bibitem{key}
作者. 标题[J]. 期刊, 年份, 卷(期): 页码.
```

### 7. 编译
```bash
xelatex main.tex
xelatex main.tex  # 两次以更新目录和引用
```

### 8. 检查清单
- [ ] 封面字段全部替换
- [ ] 中英文摘要对齐（不是机翻）
- [ ] 表格全是三线表（`\toprule/\midrule/\bottomrule`），无竖线
- [ ] 图片是 PDF 矢量图，字体清晰可读
- [ ] 所有图表都有 `\label` 和 `\caption`
- [ ] 正文 `\autoref` / `\cite` 引用正确
- [ ] 参考文献格式统一
- [ ] 编译无报错

---

## 用户 LaTeX 风格规范（从 CUMCM+DMC2601501 学到的）

### 表格铁律
- **仅三线表**：`\toprule` / `\midrule` / `\bottomrule`，永远不用竖线
- **宽度控制**：`tabularx` + 自定义列类型 `C`/`L`/`R`
- **多层表头**：`\cmidrule(r){n-m}` 分组 + `\multicolumn` 合并
- **字体**：表内 `\small`，表头 `\textbf{}` 加粗
- **符号表**：双栏布局 `@{\qquad}` 分隔左右
- **标题位置**：表上方，宋体加粗小四

### 图片规范
- **格式**：PNG（位图）或 PDF（矢量），放 `figures/` 或 `img/`
- **宽度**：`0.6-1.0\linewidth`
- **定位**：`[htbp]` 优先，关键图 `[H]`
- **子图**：`subcaption`，`\cref{fig:xxx}a` 引用
- **Caption**：描述 what/where，不给结论

### 数学公式
- **间距压缩**：`\abovedisplayskip=0pt` / `\belowdisplayskip=0pt`
- **优化模型**：`empheq` + `flalign` + `\empheqlbrace`
- **cases**：`dcases`（自动 displaystyle）
- **自定义算子**：`\DeclareMathOperator{\arcsinh}{arcsinh}` / `\DeclareMathOperator*{\argmin}{arg\,min}`
- **单位**：`\mathrm{m/s}` 或 `\si{cm}`
- **加粗数学**：`\bm{}`

### 论文结构
```
结构化摘要（\textbf{针对问题X} 每段标题）
→ 问题重述 → 问题分析（\subsection* 不编号）
→ 模型假设（itemize + \textbf{假设X}）
→ 符号说明（三线表双栏）
→ 各问题：模型建立→模型求解→模型结论→小结
→ 模型评价 → 参考文献 → 附录（\lstinputlisting）
```

### 引用系统
- 正文：`\cite{key}` / `\cite{key1,key2}`
- 智能引用：`\cref{tab:xxx}` / `\cref{fig:xxx}` / `\cref{eq:xxx}`
- 文献格式：`gbt7714-numerical`（国标顺序编码制）
- `.bib` 文件管理 + `\bibliographystyle{gbt7714-numerical}`

### 强调方式
- 关键数据/结论用 `\textbf{}` 加粗：**412.473838s**、**均大于5.26%**
- 代码内引用：`\texttt{main.py}`
- 术语首次出现：可加粗定义

### 代码展示
- Python/MATLAB 自定义 `\lstdefinestyle`
- 蓝关键字、绿注释、红字符串、灰行号
- 附录里 `\lstinputlisting[language=python]{code/xxx.py}`

### 排版参数
- 段首缩进 2em，行距 1.35-1.38
- 页边距 2.5cm 四周
- 正文字号小四（12pt），标题黑体，正文宋体

---

_For deeper context, use memory_search, memory_related, or memory_ask tools._

<!-- MEMORY:START -->
# latex-templates

_Last updated: 2026-04-30 | 0 active memories, 0 total_

_For deeper context, use memory_search, memory_related, or memory_ask tools._
<!-- MEMORY:END -->
