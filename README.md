# 上海初高中知识点汇总

> 按教材逐节编排的**上海初高中知识图谱**：先做物理（高中 166 考点 + 初中 43 考点），再扩展到语文、数学、英语、化学、生物。
>
> 每个考点配 3 道自评题 + 3 道梯度例题，支持「先测后学、会了就跳过」。

---

## 一、直接下载

> 点击即下载，不需要登录。全部文件挂在 **[v1.0 发布页](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/tag/v1.0)**，支持断点续传。

### 高中 · 物理（166 考点 / 229 页）

| 格式 | 下载 | 大小 | 用途 |
|---|---|---|---|
| **PDF** | [high-physics-handbook.pdf](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/high-physics-handbook.pdf) | 14.5 MB | 打印，A4 双面约 115 张 |
| **HTML** | [high-physics-graph.html](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/high-physics-graph.html) | 3.7 MB | 浏览器打开，可搜索、点关系图 |
| **Excel** | [high-physics-points.xlsx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/high-physics-points.xlsx) | 90 KB | 6 个表：考点/例题/公式/关系 |
| **Word** | [high-physics-handbook.docx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/high-physics-handbook.docx) | 3.3 MB | 需要二次编辑时用 |

### 初中 · 物理（43 考点 / 51 页）

| 格式 | 下载 | 大小 | 用途 |
|---|---|---|---|
| **PDF** | [junior-physics-handbook.pdf](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/junior-physics-handbook.pdf) | 2.8 MB | 打印，A4 双面约 26 张 |
| **HTML** | [junior-physics-graph.html](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/junior-physics-graph.html) | 2.4 MB | 浏览器打开，可搜索 |
| **Excel** | [junior-physics-points.xlsx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/junior-physics-points.xlsx) | 27 KB | 考点与公式清单 |
| **Word** | [junior-physics-handbook.docx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.0/junior-physics-handbook.docx) | 81 KB | 需要二次编辑时用 |

> 文件名是英文的，下载后可自行改名；发布页上每个文件都标了中文名称。

### 其他学科：发布计划（预计）

> 下面 12 项是**计划**，不是承诺。每完成一科会在本仓库新建对应目录并在这里更新链接。

| 批次 | 学段 | 学科 | 状态 | 预计 |
|---|---|---|---|---|
| — | 高中 | **物理** | ✅ 已发布 | 2026-10 |
| — | 初中 | **物理** | ✅ 已发布 | 2026-10 |
| 第 2 批 | 高中 | 数学 | 计划中 | 视进度 |
| 第 2 批 | 初中 | 数学 | 计划中 | 视进度 |
| 第 3 批 | 高中 | 化学 | 计划中 | 视进度 |
| 第 3 批 | 初中 | 化学 | 计划中 | 视进度 |
| 第 4 批 | 高中 | 生物 | 计划中 | 视进度 |
| 第 4 批 | 初中 | 生物 | 计划中 | 视进度 |
| 第 5 批 | 高中 | 语文 | 计划中 | 视进度 |
| 第 5 批 | 初中 | 语文 | 计划中 | 视进度 |
| 第 6 批 | 高中 | 英语 | 计划中 | 视进度 |
| 第 6 批 | 初中 | 英语 | 计划中 | 视进度 |

**为什么这个顺序：**

1. **数学**排第二——它是物理之外需求最大、也最依赖"题型 + 变式"结构的学科；
2. **化学、生物**排在理科之后——与物理共享"实验 + 计算 + 概念辨析"的骨架，改造成本低；
3. **语文、英语**放最后——这两科的核心是语料和阅读，卡片体例要做较大调整（从"公式推导"转向"文本分析 + 积累"），需要单独设计；
4. 每批**同时推进初高中**，避免只做高中、初中断档。

**完成一科大概要多久：** 物理高中卷（166 考点）花了约 20 轮迭代；初中卷（43 考点）一次成型。其余学科体量介于两者之间，具体看内容难度。

---

## 二、目录结构

```
上海初高中知识点汇总/
├── README.md                    本文件
├── LICENSE                      非商业使用许可
│
├── 初中/
│   ├── 物理/                    ✅ 已发布：43 考点 / 129 例题
│   │   ├── 01~09-*.md          9 个单元知识卡
│   │   ├── 教材对照表.md        四册章节目录
│   │   ├── README.md            初中物理单独说明
│   │   ├── build/              构建脚本
│   │   └── 输出/                PDF / HTML / Excel / Word
│   └── 语文/ 数学/ 英语/ 化学/ 生物/    规划中（占位）
│
└── 高中/
    ├── 物理/                    ✅ 已发布：166 考点 / 498 例题
    │   ├── 00-体例与符号规范.md
    │   ├── 00a-怎么用这本书.md
    │   ├── 03~24-*.md          20 个单元知识卡
    │   ├── 教材对照表.md
    │   ├── 教材覆盖对照.md      109 节逐节对应
    │   ├── 覆盖度报告.md
    │   ├── README.md
    │   ├── build/
    │   └── 输出/
    └── 语文/ 数学/ 英语/ 化学/ 生物/    规划中（占位）
```

---

## 三、规模

| | 初中物理 | 高中物理 | 合计 |
|---|---|---|---|
| 教材 | 四册 40 节 | 六册 109 节 | 149 节 |
| 单元 | 9 | 20 | 29 |
| 考点 | 43 | 166 | **209** |
| 例题 | 129 | 498 | **627** |
| 公式 | 59 | 184 | 243 |
| 手册页数 | 51 | 229 | **280** |

---

## 四、怎么用

**打印**：下载对应 PDF，双面打印（初中约 26 张、高中约 115 张）。

**电脑查**：下载 HTML 用浏览器打开——
- 顶部搜索框查考点、公式；
- `#c=C-8` 深链直达某个考点；
- 「图谱」页看考点间的前置/派生关系。

**给孩子做**：先做单元入口自评，按得分决定学多少；错题隔天重做、三天后换数字。

---

## 五、自己构建

每个学科目录独立，进去执行：

```bash
cd 高中/物理 && bash build/make.sh
cd 初中/物理 && bash build/make.sh
```

依赖：`python3`、`python-docx`、`openpyxl`、`markdown`、`matplotlib`、Google Chrome。

---

## 六、内容标准

- **按教材顺序**：一个考点对应教材的一节或几节，不按"知识模块"重排；
- **三级分流**：章入口 10 题 → 考点 3 题 → 按得分决定跳过/精学；
- **例题梯度**：基础 → 常考 → 综合，每题带"陷阱"和"变式"；
- **公式统一排版**：源文件写纯文本，构建时转 LaTeX，PDF 与 HTML 完全一致。

---

## 七、声明

本项目**仅限个人学习与教学参考使用，禁止任何形式的商业用途**。

- 下载、打印给孩子或学生使用：允许
- 教师备课、课堂讲义（不收费）：允许
- 转载须注明出处并保留本声明
- 售卖、打包付费课程、引流变现、商业出版：**禁止**

完整条款见 [LICENSE](LICENSE)。

---

## 八、更新

物理两卷会持续修订（勘误、补例题、考频校准）。新增学科按"语文 → 数学 → 英语 → 化学 → 生物"推进，节奏看 Issues 里的呼声。
