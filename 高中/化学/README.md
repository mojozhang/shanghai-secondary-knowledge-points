# 高中化学 · 知识点汇总

> **状态**：内容完成（v1.3）。**5 册 / 19 章 / 60 节**，拆成 **19 个单元、130 个考点、390 道例题、311 条方程式**。
> 教材依据：上海科学技术出版社（沪科版）《化学》必修第一、二册（2021 版），选择性必修第一册《化学反应原理》、第二册《物质结构与性质》、第三册《有机化学基础》（2023 版）。

按物理、数学卷的同一套骨架编排：一个教材章一张卡片，章内按考点拆；每个考点 3 道自评 + 3 道梯度例题 + 易错边界 + 过关线，支持「先测后学、会了就跳过」。化学特有的部分是**方程式速查**与**三查（元素/电荷/条件）**。

## 文档

| 文件 | 内容 |
|---|---|
| [`00-体例与符号规范.md`](00-体例与符号规范.md) | 编号、方程式与单位约定、10 段卡片结构、三级分流、错因码 |
| [`00a-怎么用这本书.md`](00a-怎么用这本书.md) | 卡片怎么读、三查怎么查、一周安排、错因码 |
| [`教材对照表.md`](教材对照表.md) | 5 册 19 章 60 节的教材页码与单元编号对照 |
| [`PROGRESS.md`](PROGRESS.md) | 制作进度、已知限制、复现方式 |
| [`CHANGELOG.md`](CHANGELOG.md) | 版本与 git 提交对应 |

## 覆盖与进度

| 册 | 模块 | 单元 | 考点 | 例题 | 方程式 |
|---|---|---|---|---|---|
| 必修第一册 | A | A-1 化学研究的天地 | 8 | 24 | 16 |
| | | A-2 海洋中的卤素资源 | 7 | 21 | 20 |
| | | A-3 硫、氮及其循环 | 7 | 21 | 20 |
| | | A-4 原子结构和化学键 | 8 | 24 | 15 |
| 必修第二册 | B | B-5 金属及其化合物 | 7 | 21 | 22 |
| | | B-6 化学反应速率和化学平衡 | 6 | 18 | 15 |
| | | B-7 常见的有机化合物 | 7 | 21 | 20 |
| 选必一 化学反应原理 | C | C-1 化学反应的热效应 | 6 | 18 | 16 |
| | | C-2 化学反应的方向、限度和速率 | 7 | 21 | 12 |
| | | C-3 水溶液中的离子反应与平衡 | 8 | 24 | 16 |
| | | C-4 氧化还原反应和电化学 | 8 | 24 | 20 |
| 选必二 物质结构与性质 | D | D-1 原子结构与性质 | 6 | 18 | 11 |
| | | D-2 分子结构与性质 | 7 | 21 | 12 |
| | | D-3 晶体结构与性质 | 6 | 18 | 10 |
| 选必三 有机化学基础 | E | E-1 认识有机化学 | 6 | 18 | 10 |
| | | E-2 烃和卤代烃 | 7 | 21 | 20 |
| | | E-3 烃的含氧衍生物 | 7 | 21 | 22 |
| | | E-4 生物大分子与合成高分子 | 6 | 18 | 16 |
| | | E-5 有机化合物的合成与研究 | 6 | 18 | 18 |
| **合计** | — | **19 单元** | **130** | **390** | **311** |

## 下载

已发布在 [v1.3 发布页](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/tag/v1.3)：

| 格式 | 文件 | 规模 |
|---|---|---|
| PDF（手册） | [high-chem-handbook.pdf](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.3/high-chem-handbook.pdf) | 271 页，5.7 MB |
| HTML | [high-chem-graph.html](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.3/high-chem-graph.html) | 单文件，可搜索、看关系图 |
| Excel | [high-chem-points.xlsx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.3/high-chem-points.xlsx) | 考点 / 例题 / 方程式 / 关系 / 关卡 |
| Word | [high-chem-handbook.docx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.3/high-chem-handbook.docx) | 二次编辑用 |

## 目录结构

```
高中/化学/
├── 00-体例与符号规范.md
├── 00a-怎么用这本书.md
├── 教材对照表.md
├── PROGRESS.md / CHANGELOG.md
├── 01~19-*.md              19 个单元知识卡（130 考点）
├── data/考点库.json         由 parse.py 生成的结构化数据
├── build/                  构建脚本（parse / gen_html / gen_docx / gen_xlsx / gen_pdf / check_cards）
└── 输出/                    PDF / HTML / Excel / Word
```

## 构建

```bash
bash build/make.sh   # 校验 → 解析 → Excel → Word → HTML → PDF → qpdf 压缩
```

产物：

- `输出/上海高中化学知识图谱手册.pdf`（Chrome 打印，271 页）
- `输出/上海高中化学知识图谱.html`（搜索、关系图、深链 `#c=C-3.2`）
- `输出/上海高中化学-考点方程式清单.xlsx`（考点总表 / 例题索引 / 方程式表 / 关系 / 关卡）
- `输出/上海高中化学知识图谱手册.docx`

依赖：Python 3（标准库 + python-docx / openpyxl）、Google Chrome、qpdf（可选，压缩 PDF）。

## 数据与约定

- `data/考点库.json`：19 个单元、130 个考点、390 道例题、311 条方程式、关系边与关卡表，由 `build/parse.py` 从 Markdown 自动解析，**勿手改**。
- 化学式与离子：Unicode 上下标（H₂SO₄、SO₄²⁻、Fe³⁺）；反应 `→`、可逆 `⇌`、气体 `↑`、沉淀 `↓`；条件写在箭头右侧括号内：`2KClO₃ →(MnO₂, Δ) 2KCl + 3O₂↑`。
- 数值：N_A = 6.02 × 10²³ mol⁻¹；V_m = 22.4 L·mol⁻¹（标准状况）；K_w = 1.0 × 10⁻¹⁴（25 ℃）。
- 本卷不含图片；装置与流程用文字描述 + 表格表达。

## 许可

与非商业使用许可一致，见仓库根目录 [LICENSE](../../LICENSE)。
