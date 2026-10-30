# 制作进度（供续作使用）

## 已完成
- [x] 7 册课本 PDF → 文本，解析 Vocabulary 附录：1560 词条 / 1440 去重 / 28 单元
- [x] `data/词汇库.json`（word / pos_all / cn / star / book_no / unit / id）
- [x] `build/vocab.py`（按单元、去重合并、统计）
- [x] `build/gen_vocab_book.py`：词汇默写本 HTML（封面/说明/目录/故事/单元词表/总表/错词表/遮挡条）
- [x] `build/make.sh`：生成 HTML → 检查故事覆盖 → Chrome 打印 PDF（94 页）
- [x] 第 1 册故事：The Lantern in the Dorm（4 章，1408 词，覆盖 195/195）
- [x] 第 2 册故事：The Risk Report（4 章，1349 词，覆盖 198/198）
- [x] 第 3 册故事：The Fourth Estate Club（4 章，966 词，覆盖 208/208）
- [x] 第 4 册故事：The Chocolate Theory（4 章，1185 词，覆盖 263/263）
- [x] 第 5 册故事：The Letter in the Mailbox（4 章，1158 词，覆盖 243/243）
- [x] `build/story_check.py`：故事覆盖率检查
- [x] `教材对照表.md`、`README.md`

## 待做（按顺序）
1. [~] 第 6–7 册故事（第 1–5 册已完成，用 story_check.py 验收 100%）
   - 词表：`python3 -c "import sys;sys.path.insert(0,'build');import vocab;print([r['word'] for r in vocab.by_unit()['E-2.1']])"`
   - 写完把章节追加到 `data/故事.json` 对应册的 chapters
2. [~] 28 张单元卡 `01..28-*.md`（模板见下）
   - [x] E-1.1 Our world、E-1.2 Places、E-1.3 Choices、E-1.4 My space（必修一完成）
   - [x] E-2.1 No limits、E-2.2 Roads to education、E-2.3 Progress?、E-2.4 Achievements（必修二完成）
   - [x] E-3.1 The media、E-3.2 The things around us、E-3.3 The way we are、E-3.4 Travellers' tales（必修三完成）
   - [x] E-4.1 Feeling good、E-4.2 Making a difference、E-4.3 Paying the price、E-4.4 The senses（选必一完成）
   - [x] E-5.1 Decisions、E-5.2 Digital humans、E-5.3 Creativity、E-5.4 Inspiration（选必二完成）
   - 剩余：选必三 E-6.1 起 8 张
3. [ ] `build/parse.py` 解析卡片 → `data/考点库.json`
4. [ ] `build/gen_html.py`：知识图谱 HTML（卡片 + 词汇交互打勾 + 图谱）
5. [ ] `build/gen_docx.py`、`build/gen_xlsx.py`、PDF
6. [ ] `00-体例与符号规范.md`、`00a-怎么用这本书.md`
7. [ ] 视觉校验（默写本方框/故事排版、手册公式与表格）
8. [ ] 根 README、GitHub Release v1.2 发布

## 单元卡模板（英文版，与物理/数学同骨架）

```
# Unit N 话题（册）

> 覆盖 E-x.y；本单元 N 词
*册 › Unit N ｜ Ⅱ · 考频 ｜ 话题 ｜ 语法*

**⚡ 先猜**：一句中式英语，判断对错

### 30 秒概述
### 30 秒自评（3 题 + 答案）
### 🔑 核心词汇（10 个：词条 + 搭配 + 例句）
### 🧩 短语与搭配（8 个）
### 📐 语法点（规则表 + 3 例句 + 2 陷阱 + 3 练习）
### ✍️ 写作（结构模板 + 5 句式）
### 📖 阅读技能（策略 + 1 例）
### 例题 1 · L1 词汇 / 例题 2 · L2 语法 / 例题 3 · L3 翻译
（每题：解析 / 💥 陷阱 / 变式）
### ⏱️ 限时挑战（60 秒）
### ✅ 接下来做什么 + 过关线
### 🧠 本单元必背 10 词（5 勾小表）
```
