# 高中英语 · 知识点汇总

> **状态**：内容完成（v1.2）。28 张单元卡（E-1.1～E-7.4）；词汇 1560 条（去重 1440）；7 篇故事全部完成，**词形覆盖 1560/1560（其中 1442 个出现原形，118 个仅以屈折/派生形出现）**。

按上海教育出版社 2022 版《英语》必修第一至第三册、选择性必修第一至第四册编排，28 个单元。体例沿用物理、数学卷：每单元一张卡片，含 30 秒自评、用法与陷阱、三道梯度例题、限时挑战与过关线。

## 文档

| 文件 | 内容 |
|---|---|
| [`00-体例与符号规范.md`](00-体例与符号规范.md) | 编号、14 段卡片结构、词汇标注、5 勾规则、故事与覆盖口径 |
| [`00a-怎么用这本书.md`](00a-怎么用这本书.md) | 卡片怎么读、5 勾怎么打、故事怎么读、一周安排 |
| [`教材对照表.md`](教材对照表.md) | 七册 28 单元的话题 / 语法 / 写作 / 词数对照 |
| [`PROGRESS.md`](PROGRESS.md) | 制作总账、已知限制、可选后续 |
| [`CHANGELOG.md`](CHANGELOG.md) | 版本与 git 提交对应 |
| [`data/故事覆盖报告.md`](data/故事覆盖报告.md) | 逐册覆盖与仅屈折词清单（自动生成） |

## 词汇默写本（本书特色）

- **一行一个词**：左边英文 + 词性，中间 5 个方框，最右边中文 + 词性。
- **5 个勾 = 5 次间隔复习**：D0 / D+1 / D+3 / D+7 / D+15，双向都默对才打勾；哪次没过，回到 D0 重来。
- **盖住右边英译中，盖住左边中译英**；书末附可剪的遮挡条。
- **每册一篇英文故事**：把本册约 200 个目标词串成 4 章故事（每章对应一个 Unit），词根加粗（如 `**kidnap**ped`），先读故事再默词表。
- 每册单元词表 + 全书去重总表（按字母），总表标注首现册.单元。
- **不含音标**：原书音标为特殊字体，电子提取即乱码，与其放错不如不放。

## 进度

| 册 | 单元 | 词条 | 卡片 | 故事（词形覆盖） |
|---|---|---|---|---|
| 必修一 | 4 | 195 | ✅ 4/4 | ✅ The Lantern in the Dorm（195/195） |
| 必修二 | 4 | 198 | ✅ 4/4 | ✅ The Risk Report（198/198） |
| 必修三 | 4 | 208 | ✅ 4/4 | ✅ The Fourth Estate Club（208/208） |
| 选必一 | 4 | 263 | ✅ 4/4 | ✅ The Chocolate Theory（263/263） |
| 选必二 | 4 | 243 | ✅ 4/4 | ✅ The Letter in the Mailbox（243/243） |
| 选必三 | 4 | 237 | ✅ 4/4 | ✅ The Island Curriculum（237/237） |
| 选必四 | 4 | 216 | ✅ 4/4 | ✅ The Signal and the Story（216/216） |
| **合计** | **28** | **1560（去重 1440）** | **28** | **7/7** |

## 下载

已发布在 [v1.2 发布页](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/tag/v1.2)：

| 格式 | 文件 | 用途 |
|---|---|---|
| PDF（手册） | [high-english-handbook.pdf](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.2/high-english-handbook.pdf) | 28 张单元卡，86 页 |
| PDF（词汇默写本） | [high-english-vocab-workbook.pdf](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.2/high-english-vocab-workbook.pdf) | 词表 + 5 勾 + 7 篇故事，111 页 |
| HTML | [high-english-graph.html](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.2/high-english-graph.html) | 卡片 + 交互词汇打勾 |
| Excel | [high-english-points.xlsx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.2/high-english-points.xlsx) | 单元 / 必背词 / 词汇总表 / 故事 |
| Word | [high-english-handbook.docx](https://github.com/mojozhang/shanghai-secondary-knowledge-points/releases/download/v1.2/high-english-handbook.docx) | 二次编辑 |

> 版本与提交的对应关系见 [`CHANGELOG.md`](CHANGELOG.md)：v1.2 = `6ba2ce9`。

## 构建

```bash
bash build/make.sh                      # 8 步重建全部产物
python3 build/story_check.py            # 词形覆盖（缺失即非零退出）
python3 build/story_check.py --strict   # 原形覆盖（仅屈折也算未覆盖）
```

产物：
- `输出/上海高中英语知识图谱手册.pdf`（单元卡片）
- `输出/上海高中英语知识图谱.html`（卡片 + 交互词汇打勾 + 打印版）
- `输出/上海高中英语-词汇默写本.pdf`（单元词表 + 总表 + 故事）
- `输出/上海高中英语知识图谱手册.docx`、`输出/上海高中英语-考点词汇清单.xlsx`

## 数据

- `data/词汇库.json`：从 7 册课本 Vocabulary 附录解析，含单词、词性、中文/英文释义、册、单元、标星；不含音标。
- `data/故事.json`：每册故事（4 章），目标词词根用 `**词**` 标注。
- `data/考点库.json`：28 张卡片的解析结果，由 `build/parse.py` 生成，勿手改。
- `build/story_check.py`：双口径覆盖校验，并生成 `data/故事覆盖报告.md`。
