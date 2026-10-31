# 制作进度（供续作使用）

> **状态：已完结（v1.2）**。28 张单元卡、词汇默写本、7 篇故事、HTML/Excel/Word 全部完成并发布。
> 版本与提交对应见 [`CHANGELOG.md`](CHANGELOG.md)；体例见 [`00-体例与符号规范.md`](00-体例与符号规范.md)。

## 一、总账

| 项目 | 数字 | 核对方式 |
|---|---|---|
| 册 / 单元 | 7 册 / 28 单元 | `ls 0*.md`、`data/词汇库.json` 的 `id` 去重 |
| 词条 | 1560（去重 1440，标星 352） | `python3 -c "import sys;sys.path.insert(0,'build');import vocab;print(len(vocab.load()), len(vocab.master()))"` |
| 单元卡 | 28 张 | `grep -c '^## E-' 0*.md` |
| 故事 | 7 篇 × 4 章 | `data/故事.json` |
| 故事覆盖 | 词形 1560/1560；原形 1442/1560 | `python3 build/story_check.py` |
| 产物 | 6 个（2 PDF / HTML / Word / Excel / 打印版） | `输出/` |

## 二、已完成清单

- [x] 7 册课本 PDF → 文本，解析 Vocabulary 附录：1560 词条 / 1440 去重 / 28 单元
- [x] `data/词汇库.json`（word / pos / cn / en / star / book / book_no / unit / id；**不含音标**）
- [x] `build/vocab.py`（按单元分组、全书去重、统计）
- [x] `build/parse.py` → `data/考点库.json`（28 单元卡片解析结果）
- [x] `build/gen_html.py` / `gen_print.py` / `gen_pdf.py` / `gen_docx.py` / `gen_xlsx.py`
- [x] `build/gen_vocab_book.py`：词汇默写本（封面/说明/目录/故事/单元词表/总表/错词表/遮挡条）
- [x] `build/make.sh`：8 步一条命令重建（构建 → 故事校验 → Chrome 打印 PDF）
- [x] 28 张单元卡 `01..07-*.md`：E-1.1 ～ E-7.4 全部完成
- [x] 7 篇故事（每册 4 章，一章对应一个 Unit）
- [x] `build/story_check.py`：词形/原形双口径校验，输出 `data/故事覆盖报告.md`
- [x] `00-体例与符号规范.md`、`00a-怎么用这本书.md`（v1 体例沉淀）
- [x] `教材对照表.md`、`README.md`、`CHANGELOG.md`
- [x] 视觉校验：默写本方框/故事排版、手册目录/表格、Word 转 PDF 抽查
- [x] 根 README 下载表与发布状态；GitHub Release v1.2（5 个资产）

## 三、已知限制（不影响使用，续作时别再当 bug 查）

1. **音标不收录**：原书音标为特殊字体，提取即乱码，已从词库删除 `ipa` 字段；需要音标须人工校对。
2. **118 个词只以屈折形出现**：如 `**kidnap**ped`、`**shout**ed`，词根已加粗，认词不受影响；按 `--strict` 口径不计原形覆盖。逐条清单见 `data/故事覆盖报告.md`。
3. **词汇默写本 8.8 MB**：主要是内嵌字体与故事页；如需减小可改用系统字体子集。
4. 词表释义来自教材附录，个别词条含教材特有的用法说明（括号保留），不是词典全义。

## 四、可选后续（按价值排序）

- [ ] 若要"原形全覆盖"，按 `data/故事覆盖报告.md` 的 118 个词逐句改写故事（改完跑 `python3 build/story_check.py --strict` 必须为 0 退出）
- [ ] 音标人工校对版词表（需要词典数据源）
- [ ] 听说文本：朗读稿、快速应答模板、话题表达框架（听力/口语 10 分）
- [ ] 初中英语（7–9 年级）按同一体例复制

## 五、构建与校验

```bash
bash build/make.sh                      # 8 步重建全部产物
python3 build/story_check.py            # 词形覆盖，缺失即非零退出
python3 build/story_check.py --strict   # 原形覆盖，仅屈折也算未覆盖
```

## 六、单元卡模板（英文版）

```
## E-x.y 话题

*册 Unit N ｜ Ⅱ · 考频 ｜ 话题 ｜ 语法 ｜ 本单元 N 词*

**⚡ 先猜**：一句中式英语，判断对错

### 30 秒概述
### 30 秒自评（3 题 + 答案）
### 🔑 核心词汇（10）
### 🧩 短语与搭配（8）
### 📐 语法：……
### ✍️ 写作：……
### 📖 阅读技能：……
### 例题 1 · L1 词汇 / 例题 2 · L2 语法 / 例题 3 · L3 翻译
（每题：解析 / 💥 陷阱 / 变式）
### ⏱️ 限时挑战（60 秒）
### ✅ 接下来做什么 + 过关线
### 🧠 本单元必背 10 词
```
