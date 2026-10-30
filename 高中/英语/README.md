# 高中英语 · 知识点汇总

> **状态**：内容完成。28 张单元卡（E-1.1～E-7.4）全部完成；词汇数据 1560 条；7 篇故事全部完成，逐词覆盖 1560/1560。

按上海教育出版社 2022 版《英语》必修第一至第三册、选择性必修第一至第四册编排，28 个单元。体例沿用物理、数学卷：每单元一张卡片，含 30 秒自评、用法与陷阱、三道梯度例题、限时挑战与过关线。

## 词汇默写本（本书特色）

- **一行一个词**：左边英文 + 词性，中间 5 个方框，最右边中文 + 词性。
- **5 个勾 = 5 次间隔复习**：D0 / D+1 / D+3 / D+7 / D+15，双向都默对才打勾；哪次没过，回到 D0 重来。
- **盖住右边英译中，盖住左边中译英**；书末附可剪的遮挡条。
- **每册一篇英文故事**：把本册约 200 个目标词串成 4 章故事（每章对应一个 Unit），目标词加粗，先读故事再默词表。
- 每册单元词表 + 全书去重总表（按字母），总表标注首现册.单元。

## 进度

| 册 | 单元 | 词条 | 卡片 | 故事 |
|---|---|---|---|---|
| 必修一 | 4 | 195 | ✅ 4/4 | ✅ The Lantern in the Dorm（195/195 词） |
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

## 构建

```bash
bash build/make.sh
```

产物：
- `输出/上海高中英语知识图谱手册.pdf`（单元卡片）
- `输出/上海高中英语知识图谱.html`（卡片 + 交互词汇打勾 + 打印版）
- `输出/上海高中英语-词汇默写本.pdf`（单元词表 + 总表 + 故事）
- `输出/上海高中英语知识图谱手册.docx`、`输出/上海高中英语-考点词汇清单.xlsx`

## 数据

- `data/词汇库.json`：从 7 册课本 Vocabulary 附录解析，含单词、词性、中文释义、册、单元、标星。
- `data/故事.json`：每册故事（4 章），目标词用 `**词**` 标注。
- `build/story_check.py`：检查每篇故事对本册词表的覆盖率，当前第 1 册 195/195。
