# 高质量 Query 评估筛选指南

> **适用对象**：需要从外部交付数据（协作方 / 供应商 / 众包）中筛选高质量 query 构建 eval set 的 AI PM
> **更新时间**：2026-08
> **定位**：本文是 `LLM_evaluation_framework.md` §4 Step 3「自建 eval set 实测」的深化篇——那里讲"自建 eval 才是真相"，本文回答：**当数据不是自己攒的，而是别人交付的一批 query + 多模型回答时，怎么筛出能用的部分。**

---

## 1. 引言：筛选 = 两道独立闸门

**把筛 query 当成筛考题：好题必须同时满足两个独立条件——题目本身出得好（query 质量），以及能拉开考生的分数（回答区分性）。** 两个维度分开打分，分别设闸门，最后合并决策。只用其中一个维度会产生系统性偏差：只看 query 质量会留下一堆"人人都答对"的天花板题；只看区分性会把歧义题、坏题误当成"难题"留下来。

本文以一个真实数据画像为运行示例：**协作方交付 1500–2000 条 query，覆盖 10+ 种语言、10+ 个细分领域，每条 query 附带多个模型的回答。**

附带的多模型回答是这类交付数据的独有优势：**相当于一次免费的 pilot run**。正常流程里，要判断一条 query 能否拉开模型差距，得自己调用各模型拿回答；现在这一步已经有人替你跑完，区分性可以直接量化计算。

最终产出不是一份名单，而是三样东西：

| 产出 | 内容 | 用途 |
|---|---|---|
| **核心 eval set** | 高质量 + 高区分的 query | 模型对比、选型、迭代验证 |
| **锚点回归集** | 高质量但模型全对的题（少量保留） | 基准线、监测能力回退 |
| **淘汰台账** | 每条被淘汰 query 的原因标签与统计 | 反馈协作方、指导下批交付 |

---

## 2. 总流程：五阶段 pipeline

| 阶段 | 动作 | 手段 | 典型淘汰比例 | 人工介入 |
|---|---|---|---|---|
| **Stage 0** 规则清洗 | 去重、剔残缺、打标签 | 脚本 + embedding | 20–40% | 无 |
| **Stage 1** 歧义剔除 | 按 7 条清单剔除歧义/残缺题 | LLM 检测 + 清单 | 10–20% | 边界 case 裁决 |
| **Stage 2** 质量打分 | 7 判据逐条 yes/no，0–7 计分 | LLM annotator | 视阈值 | 抽检校准 |
| **Stage 3** 区分性分桶 | judge 独立打分 → spread 分桶 | 强模型 judge | 视分桶 | 全低分桶裁决 |
| **Stage 4** 覆盖配比 | 语言 × 领域矩阵检查、定稿 | 统计 + 人工 | — | 配比决策 |

三点量级说明：

- **2k 条不需要 Arena-Hard 式的聚类抽样**。Arena-Hard 的 BERTopic 聚类是为 20 万条设计的入口漏斗；2k 条量级 LLM 逐条打分完全可行，只保留轻量 embedding 去重即可。
- **顺序不可颠倒**：Stage 0/1 便宜，Stage 2/3 要花 judge 调用费。先用便宜手段砍掉三到五成，再对剩余部分精评。
- **每一步都记录淘汰原因标签**，不要静默丢弃——淘汰台账既是给协作方的反馈，也是自查筛选逻辑是否失控的依据（某个环节淘汰率异常高，先怀疑规则再怀疑数据）。

---

## 3. Stage 0：规则清洗（不花 judge 费用）

全部可脚本化，目标是把明显不可用的数据在花钱之前清掉。

| 检查项 | 口径 | 处置 |
|---|---|---|
| **近重复去重** | 先按语言分桶（跨语言不比），桶内 embedding 余弦相似度 ≥0.92 判重复；0.85–0.92 灰区人工扫一眼 | 每组重复保留 1 条（选表述最完整的） |
| **模板化伪多样性** | 同一句式换名词批量生成（"帮我写一篇关于 X 的文章"× 50） | 只打 `template_id` 标签放行，**不在此阶段定夺去留**；超大组（>10 条）粗剪至 10 条以控制 judge 成本，终选见 §7.4 |
| **截断/残缺** | 以半句结尾、明显被切断的粘贴文本 | 剔除 |
| **乱码/编码错误** | 非正常字符占比 >10% | 剔除 |
| **超短** | 去除标点后 <5 个词（或 <10 个汉字）且无明确任务 | 剔除 |
| **语言不符** | 语言检测结果与协作方标注不一致 | 修正标签，不剔除 |
| **PII** | 含真实姓名+联系方式、证件号、账号密码 | 脱敏后保留，脱敏会破坏语义则剔除 |

**近重复"早剪"、模板组"晚剪"，区别对待是有意的**：近重复（余弦 ≥0.92）的条目连模型回答都几乎一样，质量分和 spread 必然趋同，早剪省 judge 费用且无信息损失；模板组不同——实例间主题各异（X 换了 50 个话题），质量和区分性真有差别，此时还没有 Stage 2/3 的信号，早剪等于瞎选。原则是**早标记、晚定夺**：粗剪只在组太大时为控制成本执行，剪的标准也只是"主题差异最大、表述最完整"，真正的择优留到 Stage 4（§7.4）。

**产出**：清洗后的 query 表，每条带 `language`、`domain` 初始标签（协作方标注 + 自动检测双列，不一致的标记待复核）。

---

## 4. Stage 1：歧义与残缺剔除

**有歧义的 query 不入选。** 判定不靠感觉，按下面 7 条清单逐条检查，命中任意一条即剔除并记录类型标签：

| # | 歧义类型 | 判例 | 判定口径 |
|---|---|---|---|
| 1 | **指代不明** | "这个方案帮我改一下"、"他说的对吗" | 代词/名词在 query 内找不到指代对象 |
| 2 | **引用不可见材料** | "根据以上内容总结"、"翻译这张图" | 提到附件/图片/上文，但数据里没有 |
| 3 | **多轮残片** | 明显是对话中间一轮，脱离前文无法理解 | 单独阅读无法还原任务 |
| 4 | **任务动词不明** | "看看这段代码"、"处理一下这个投诉" | 无法确定期望产出是解释、修改还是评价 |
| 5 | **关键约束缺失** | "写一份自我介绍"（无场景/长度/身份） | 缺约束导致任何回答都"对"，无法比较 |
| 6 | **多重解释互斥** | "苹果最新的产品怎么样" | 不同理解导向完全不同且矛盾的答案 |
| 7 | **前提错误/自相矛盾** | "为什么 Python 比 C 快" | 纠正前提与顺着答会产生无法同框比较的回答 |

### 4.1 两个操作化检测（不逐条人肉读）

- **改写一致性测试**：让 LLM 独立跑两次"把这条 query 改写成完整明确的版本"。两次改写的**意图**不一致 → 歧义，剔除。适合批量跑在全量数据上。
- **理解方向分歧检测**：直接利用已有的多模型回答——如果各模型对任务的**理解方向**不同（A 在解释代码、B 在改代码），而不是完成质量不同 → 强歧义信号，进人工裁决队列。这比只看 query 本身更灵敏，是这批数据白送的检测器。

两个检测是**召回手段**，最终裁决仍对照 7 条清单：检测标红但清单一条不中的，保留。

### 4.2 时效性处理（三条规则，不搞一刀切）

1. **能钉住时点的，改写后保留**："最近的销量" → "2025 年 Q3 的销量"，改写后按普通题处理。
2. **钉不住且答案会漂移的，剔除**：剔除理由记为"维护成本"，不是题本身不好。
3. **被评产品带联网/RAG 的，时效题单独建子集另评**，不混入主集。

---

## 5. Stage 2：query 质量打分（7 判据）

采用 Arena-Hard / BenchBuilder 的 7 判据，每条 query 由 LLM annotator 逐条判 yes/no，**满足几条得几分（0–7）**。不用"可判定性"这类抽象词——每条判据都能独立检查：

| # | 判据 | 中文口径（yes 的条件） |
|---|---|---|
| 1 | **Specificity** | 要求明确、具体的输出，不留模糊空间 |
| 2 | **Domain Knowledge** | 考察一个或多个特定领域的知识 |
| 3 | **Complexity** | 含多个组件、变量或层次，不是一步能答完 |
| 4 | **Problem-Solving** | 需要主动分析问题并系统性给出解法，而非复述事实 |
| 5 | **Creativity** | 需要创造性的思路或方案 |
| 6 | **Technical Accuracy** | 答案要求高技术准确度，错了能被明确指出 |
| 7 | **Real-world Application** | 对应真实使用场景，不是刁钻的智力游戏 |

### 5.1 阈值

- **≥5 分入选，作为起步阈值**。Arena-Hard 用 ≥6，但那是 20 万条里挑 500 条的奢侈打法；2k 条数据用 ≥6 可能筛得所剩无几。
- 先跑完打分看**分数分布**再定阈值：如果 ≥5 的存量不足以覆盖语言 × 领域矩阵（见 §7），降到 ≥4 并在交付说明里写明取舍；反之存量充裕可提高到 ≥6。
- **阈值对全体 query 统一**，不要按领域各设一套——领域间的量不平衡放到 Stage 4 用配比解决，不要用阈值解决。

### 5.2 多语言适配

- **Judge prompt 用英文，被评 query 保持原语言**（附录 A）。强模型跨语言评估英文指令最稳定。
- annotator 输出中带 `language` 字段，方便按语言统计分数分布——**如果某语言整体分数显著偏低，先怀疑 judge 在该语言上的能力衰减，再怀疑数据质量**。
- 小语种（judge 训练数据少的语言）的打分结果，人工抽检比例翻倍（见 §8.3）。

---

## 6. Stage 3：回答区分性评估

对通过 Stage 2 的 query，用 judge 给每条 query 下的**每个模型回答独立打分**，再按分数离散度分桶。

### 6.1 打分原则（三条铁律）

1. **独立**：judge 一次只看一个回答，不同时看多个——避免 Position Bias（见 §8.1）。
2. **双盲**：prompt 中不出现模型名——避免 Self-Preference Bias。
3. **按 rubric 逐条 PASS/FAIL，不凭整体印象**：这样分数差异才来自质量差距，而不是风格偏好（附录 B）。

Judge 选比候选模型更强的模型；生成方模型不做自己回答的唯一 judge。

### 6.2 分桶决策表

以 0–5 分制为例，对每条 query 计算 spread = max − min：

| 分数形态 | 判断 | 处置 |
|---|---|---|
| **spread ≥ 2** | 黄金题，真正区分模型能力 | 进核心 eval set |
| **全高分**（min ≥ 4） | 天花板题，太简单 | 抽 10–15% 进锚点回归集，其余淘汰（标"无区分"） |
| **全低分**（max ≤ 2） | 真硬题或坏题，二者必居其一 | **必须人工裁决**：所有模型都栽的原因是题目残缺 → 坏题淘汰；题目完好但确实难 → 硬题保留并标 `hard` |
| **spread = 1 中间态** | 弱区分 | 按覆盖配比需要取舍：稀缺格子（小语种 × 冷门领域）保留，充裕格子淘汰 |

### 6.3 开放题：换 Pairwise + Swap

纯开放题（无硬约束可写 rubric）绝对打分不可靠，改用相对比较：judge 一次看两个匿名回答选更好的，**交换顺序再跑一次**——两次结果一致才计入，不一致记平局。区分性指标相应变为：**胜负关系是否稳定且不对称**（某模型稳定胜出 → 有区分；平局为主 → 无区分）。

### 6.4 集合级验证

单条区分性都合格 ≠ 整套集合合格。定稿前做一次整体检验：**用最终集合给参评模型排一次名，对照团队的常识判断**（比如公认强的模型是否排在前面、差距是否明显）。排名反常识时优先排查 judge 偏差，其次排查集合构成。

> 这是 Arena-Hard "separability" 的简化版——原版定义为 bootstrap 95% 置信区间不重叠的模型对占比（Arena-Hard 500 题达到 87%，MT-Bench 仅 22%）。2k 量级不必跑 bootstrap，排名对照常识足够；如果这套集合将长期服役、频繁用于模型选型决策，再补置信区间计算。

---

## 7. Stage 4：覆盖度与配比

筛完之后必须回答：**留下的题在语言、领域、难度上是否还能代表这批数据要评的能力面？** 逐条质量再高，覆盖塌了整套集合就失效。

### 7.1 语言 × 领域矩阵

10+ 语言 × 10+ 领域 = 100+ 个格子，2k 条平均每格十几条，筛掉一半后极易出现空格。定稿前生成矩阵热力图检查：

- **空格子**：回到该格子被淘汰的 query 里，从"弱区分"档回捞质量最高的 1–2 条补位，并标注 `backfill`。
- **实在无题可捞的格子**：在交付说明中明确声明该格子无覆盖，不要让使用者误以为测过。
- **不要为填格子降低歧义/残缺标准**——坏题的危害大于空格子。

### 7.2 难度分布

参考难度配比 **简单 40% / 中等 40% / 困难 20%**（口径来自 `refer/evaluate/evaluate-Agent/01` 号笔记的 Golden Dataset 建议）。Stage 3 的分桶天然提供难度信号：锚点题≈简单，spread 题≈中等，全低分保留的硬题≈困难。

### 7.3 五类 Coverage 对照

定稿前按 Golden Dataset 五类覆盖（口径来自 `06` 号笔记）过一遍：

| 覆盖维度 | 本场景检查点 |
|---|---|
| **Business** | 10+ 细分领域是否都有存活样本（即 §7.1 矩阵） |
| **User** | 不同用户口吻/身份的 query 是否都有（正式 vs 口语、专家 vs 小白） |
| **Difficulty** | §7.2 的 40/40/20 |
| **Risk** | 安全类、拒答边界类 query 是否保留（这类题往往 Stage 2 分数不高，但按影响而非分数决定去留） |
| **Regression** | 本批暂无历史失败 case；上线使用后把翻车题回灌进来 |

### 7.4 模板组终选

Stage 0 只给模板组打了标签，去留在这里定夺——此时每条实例已经有了质量分（Stage 2）和 spread（Stage 3），**每个 `template_id` 最多保留 2–3 条，按三级排序键择优**：

1. **spread 高者优先**——同模板下能拉开模型差距的实例最稀缺；
2. spread 相同看 **质量分**；
3. 仍相同看 **格子稀缺度**——落在语言 × 领域矩阵稀缺格子里的实例优先（顺手为 §7.1 补位）。

同模板落选的实例标 `drop_reason = template_cap`，进淘汰台账。如果某模板组的全部实例 spread 都为 0（模板本身太简单，所有模型都答对），整组只按锚点集规则处理，不占核心集名额。

### 7.5 Metadata 与版本管理

每条入选 query 落表，最小字段集：

```text
case_id | query | language | domain | difficulty | source(协作方批次)
| template_id(非模板则空) | quality_score(0-7) | spread
| bucket(core/anchor/hard/backfill) | status(active/dropped)
| drop_reason | dataset_version
```

**集合定版为 `v1.0` 并锁定**。此后每次增删都升版本号——否则两次评估的分数差异无法归因（是模型变了还是题变了）。judge prompt、judge 模型、rubric 的版本一并记录。

---

## 8. Judge 质量保障

Stage 2 和 Stage 3 的全部结论都建立在 judge 打分之上。**Judge 分数不是真值，是一台带系统性偏差的测量仪器**——仪器不校准，后面所有筛选都是在精确地执行错误。

### 8.1 四类偏见与对冲

（偏见分类口径来自 `refer/evaluate/evaluate-Agent/05` 号笔记）

| 偏见 | 表现 | 对本流程的具体威胁 | 对冲手段 |
|---|---|---|---|
| **Verbosity Bias** | 把"写得长"误判为"质量高" | Stage 3 中长回答模型被系统性高估，spread 失真 | rubric 中写明"简洁正确不扣分"；附录 B 显式要求不奖励长度 |
| **Position Bias** | 对比时偏向先展示的选项 | 开放题 Pairwise 结果受顺序摆布 | §6.3 的 Swap：交换顺序跑两次，不一致记平局 |
| **Self-Preference Bias** | 偏好同厂商风格的回答 | 若 judge 与某候选模型同源，该模型分数虚高 | judge 与候选模型错开厂商；无法错开时用双 judge 交叉 |
| **Lenience Bias** | 缺惩罚机制时普遍给高分 | 分数挤在 4–5 分，spread 全面塌缩，区分性计算失效 | rubric 写明扣分规则；先跑 CoT 证据再给分；校准集里掺已知烂答案测试 |

其中 **Lenience Bias 对本流程杀伤最大**：其他偏见扭曲的是"谁高谁低"，它直接摧毁"拉不拉得开"这个核心信号。上线打分前先做一个 lenience test——往校准集里掺 5–10 条人工确认的明显低质量回答，judge 若给不出有区分度的低分和明确扣分理由，先修 rubric 再开工。

### 8.2 人工校准流程

分两步走（两份笔记口径不同，分别标注）：

1. **迭代期（20 条基线）**：抽 20 条真实样本，PM 按 rubric 亲自打分 → judge 打同一批 → 逐条对比分数与理由 → 分歧大时**先改 rubric、再改 judge prompt，最后才换 judge 模型**（顺序来自 `04` 号笔记：分歧的根源通常是 rubric 用了"专业、自然"这类不可观察的形容词，而不是 judge 不行）。循环到双方判断基本对齐。
2. **验收期（100 条抽检，>80% 一致性）**：正式跑全量前，随机抽 100 条由人工与 judge 双打分，人机一致性 >80% 才放行（口径来自 `05` 号笔记；`04` 号笔记明确拒绝给统一阈值，80% 应理解为该视频作者的实践建议，团队应按自己的评分尺度和错误成本调整，而非铁律）。
3. **全量运行中持续抽检 20%**（口径来自 `LLM_evaluation_framework.md` Step 3），重点抽两类：分数极端的、语言为小语种的。

### 8.3 多语言特别项

- **Judge 在小语种上的能力本身会衰减**——它可能读不懂 query 却装作读懂了。对策：非英语 query 的人工抽检比例翻倍（40%）；抽检人须懂该语言，找不到人的语言在交付说明里降级标注为"低置信"。
- **警惕"语言 → 分数"的系统相关**：若某语言的 query 质量分或回答分整体显著偏低，先做归因实验——把该语言 10 条 query 人工翻译成英文重打分，分数回升则是 judge 语言能力问题，不是数据质量问题，该语言的阈值需单独校准。
- **rubric 保持语言无关**：评"是否给出可执行步骤"而不是评"中文表达是否地道"，除非语言地道性本身就是被评能力。

### 8.4 成本粗算

调用量估算公式（N=清洗后 query 数，M=模型数，P=通过 Stage 2 的比例）：

```text
Stage 1 改写检测:  2 × N
Stage 2 质量打分:  1 × N
Stage 3 独立打分:  M × P × N
开放题 Pairwise:   2 × M(M-1)/2 × N_open
校准与抽检:        ~0.25 × 上述总量
```

以 N=1500、M=4、P=60% 计，总调用约 1.2–1.5 万次，每次平均 1–2k tokens——**总量在千万 token 级**，用主流强模型做 judge 是几十美元量级的开销。结论：这个规模不值得为省钱换弱 judge，**judge 降级省下的钱远小于筛错数据的返工成本**。

---

## 9. 常见误区与深层陷阱

前面各 Stage 是"怎么做对"，这一节是"怎么不做错"——每一条都是这类筛选项目里真实高发的系统性错误。

**误区一：路灯效应——"好打分"挤掉"有代表性"。** 客观题、封闭题天然容易通过各道闸门，开放生成类 query 在 Stage 2/3 的存活率会系统性偏低。如果线上真实流量四成是开放生成，而终集里只剩 5%，这套 eval 测的就不是你的产品。对策：Stage 4 配比时对照真实流量分布（拿不到就对照协作方交付时的领域配比），开放题占比塌陷时用 §6.3 的 Pairwise 通道回捞，而不是接受塌陷。

**误区二：把区分性当静态属性。** 今天 spread=3 的黄金题，模型迭代半年后可能人人满分。区分性是"当前这代模型"的快照，不是题的固有性质。对策：metadata 里记录本次打分用的全部模型版本；每次参评模型换代，对核心集重算一次 spread，把新塌缩为全对的题移入锚点集——**核心集萎缩是正常代谢，不是质量事故**。

**误区三：把淘汰率当 KPI。** "筛掉 60%"听起来很严格，但淘汰率高可能只说明规则错了（比如把某小语种整体误杀，见 §8.3）。反过来协作方也可能拿"通过率"考核自己。对策：淘汰台账按"原因 × 语言 × 领域"三维统计，任何一个格子的淘汰率显著偏离全局均值，先审规则再定结论。

**误区四：分流错误比打分错误更危险。** 一条封闭题被 judge 打错 1 分，影响一条数据；一类开放题被错误地套上封闭题 rubric 打分（比如把合理的追问行为判为"未完成任务"），影响一整类数据，且方向一致、难以被抽检发现。对策：人工抽检时不只核对分数，**必须核对"这条题用的评分方式对不对"**；抽检样本按 bucket 分层抽，不做简单随机。

**误区五：默认协作方数据分布是中立的。** 交付数据可能带着协作方自己的生产偏好：某几个模板灌量、避开难做的语言、用机器翻译扩语言覆盖（表现为小语种 query 有明显翻译腔）。对策：Stage 0 的模板检测和语言检测结果单独成表；如果筛选标准会回传给协作方，**保留一部分判据不公开**（如人工抽检的裁决标准），否则下一批交付会"应试化"——针对公开判据优化，而不是针对质量优化。

**误区六：把这次筛选当成一次性项目。** 筛出的集合会老化：业务领域会变、模型会换代、参考答案会过期。按 `06` 号笔记的定位，**dataset 是需要持续运营的产品资产**——本文的 metadata、版本管理、淘汰台账设计都是为"下一批"服务的：下批数据到来时，Stage 0–4 原样复跑，新旧集合按版本合并。

---

## 10. 验收与交付

### 10.1 定稿 checklist

发布 `v1.0` 前逐项确认：

- [ ] 每条入选 query 的 metadata 字段完整（§7.5），无 `status` 为空的记录
- [ ] 语言 × 领域矩阵无未声明的空格子；backfill 与低置信语言已标注
- [ ] 难度分布在 40/40/20 的 ±10pp 以内，或偏离已在说明中解释
- [ ] 全低分桶的每条题都有人工裁决记录（硬题保留 or 坏题淘汰，不存在悬而未决）
- [ ] judge 校准记录完整：20 条迭代记录、100 条验收一致率、lenience test 结果
- [ ] 淘汰台账可复算：每条被淘汰 query 有原因标签，各阶段淘汰数相加等于总淘汰数
- [ ] 版本锁定：dataset / judge prompt / judge 模型 / rubric 四个版本号已记录

### 10.2 给协作方的质量反馈报告

淘汰台账不是内部废料，整理成反馈报告是高价值交付物，建议结构：

1. **总览**：交付量 → 各阶段存活量的漏斗图，最终入选率
2. **淘汰原因分布**：Top 原因排序（近重复、歧义类型 1–7、低质量分、无区分），各附 2–3 条脱敏示例
3. **语言 × 领域质量热力图**：哪些格子质量高、哪些格子问题集中
4. **可执行改进建议**：下批交付的具体要求（如"多轮对话请附完整上下文"、"同一模板不超过 3 条"、"附上 query 的原始语言标注"）
5. **不公开项说明**：声明部分裁决判据不随报告公开（防应试化，见 §9 误区五）

---

# 附录 A：Query 质量标注 Prompt（7 判据）

英文 prompt、query 保持原语言。低成本模型即可执行（判据是 yes/no 判断，不需要顶级推理）。

```text
You are a data annotator curating evaluation queries for LLM benchmarking.
Assess the USER QUERY below against 7 binary criteria. For each criterion,
answer true only if the query clearly satisfies it.

1. specificity: Does the query ask for a specific, well-defined output?
2. domain_knowledge: Does it test knowledge in one or more specific domains?
3. complexity: Does it have multiple components, variables, or levels of depth?
4. problem_solving: Does it require active problem-solving — analyzing the
   problem and systematically devising a solution — rather than recall?
5. creativity: Does it require a creative approach or solution?
6. technical_accuracy: Does the expected answer demand a high degree of
   technical accuracy and correctness, such that errors are objectively
   identifiable?
7. real_world: Does it correspond to a realistic real-world use case?

Rules:
- Judge the QUERY itself, not any imagined answer to it.
- The query may be in any language. Do not penalize non-English queries.
- If the query is ambiguous, truncated, or references unavailable material
  (attachments, prior turns), set "defective" to true and explain in "notes".

USER QUERY:
{{query}}

Output strict JSON only, no markdown:
{
  "language": "<ISO 639-1 code>",
  "specificity": true/false,
  "domain_knowledge": true/false,
  "complexity": true/false,
  "problem_solving": true/false,
  "creativity": true/false,
  "technical_accuracy": true/false,
  "real_world": true/false,
  "score": <integer 0-7, count of true values>,
  "defective": true/false,
  "notes": "<one sentence, only if defective or borderline>"
}
```

`defective=true` 的 query 回流 Stage 1 人工裁决队列——annotator 顺手兜住漏网的残缺题。

---

# 附录 B：回答质量打分 Prompt（区分性评估用）

结构改造自 `.claude/skills/evaluate-llm/resources/judge_prompt.md`（保留 rubric_checks / score / failure_mode 三件套，增加 language 字段与反 verbosity 条款）。**用比候选模型更强的模型执行；一次只评一个回答；prompt 中不出现模型名。**

```text
You are a strict evaluator of AI responses. Score ONE candidate response
against the rubric for the given query. You will see only this one response;
do not assume anything about other candidates.

Principles:
- Judge ONLY against the rubric items. No style preferences.
- Do NOT reward length. A concise, correct answer scores no lower than a
  long one. Padding, repetition, and unrequested content earn no credit.
- Evaluate in the language of the query. Do not penalize the response for
  being in the query's language.
- Cite concrete evidence from the response for every PASS/FAIL before scoring.

QUERY:
{{query}}

RUBRIC:
{{rubric}}

CANDIDATE RESPONSE:
{{response}}

Score anchors:
5 = satisfies all rubric items; deployable as-is
4 = satisfies the core rubric; minor flaws that do not affect usability
3 = partially satisfies; needs human correction
2 = fails most rubric items; major defects
1 = barely touches the task
0 = entirely off-task

Output strict JSON only, no markdown:
{
  "language": "<ISO 639-1 code>",
  "rubric_checks": [
    {"item": "...", "status": "PASS|FAIL", "evidence": "..."}
  ],
  "score": <integer 0-5>,
  "failure_mode": "none|hallucination|refusal|format_error|incomplete|off_topic|misunderstood_task|other",
  "summary": "<one sentence>"
}
```

`misunderstood_task` 是相对原模板新增的枚举值：多个模型在同一 query 上触发它 → 回流 §4.1 的歧义裁决（理解方向分歧信号）。

每条 query 的 rubric 从哪来：封闭题直接写参考答案；约束开放题由强模型起草"必须项 + 禁止项"再人工过目（2k 量级不必每条手写，抽检 20% 即可）。

---

# 附录 C：阈值与分桶速查

所有数字集中一处，含出处与调整空间：

| 参数 | 默认值 | 出处 / 调整说明 |
|---|---|---|
| 近重复判定 | 余弦 ≥0.92 | 经验值；0.85–0.92 灰区人工扫 |
| 同模板保留上限 | 终选 2–3 条（Stage 0 仅超大组粗剪至 10 条） | 择优键：spread → 质量分 → 格子稀缺度（§7.4） |
| 质量分入选线 | ≥5（0–7 分制） | Arena-Hard 用 ≥6（20 万挑 500 的口径）；看分布后在 4–6 间调 |
| 区分性入核心集 | spread ≥2（0–5 分制） | 本文口径；M≥5 个模型时可改用分数标准差 ≥1 |
| 锚点集抽取比例 | 全高分题的 10–15% | 经验值 |
| 难度配比 | 40/40/20 | `01` 号笔记 Golden Dataset 建议 |
| 校准迭代集 | 20 条 | `04` 号笔记（明确拒绝配固定通过阈值） |
| 校准验收集 | 100 条、人机一致 >80% | `05` 号笔记（作者标注为实践建议非铁律） |
| 运行抽检比例 | 20%；小语种 40% | framework.md Step 3；小语种加倍为本文口径 |
| Pairwise 一致性 | Swap 两次一致才计入 | `05` 号笔记方法 3 |

| 分数形态（0–5 制） | 桶 | 处置 |
|---|---|---|
| spread ≥2 | core | 入核心集 |
| min ≥4 | anchor | 抽 10–15% 留锚点，余淘汰 |
| max ≤2 | 人工裁决 | 硬题→hard 保留；坏题→淘汰 |
| spread =1 | 弱区分 | 稀缺格子保留，充裕格子淘汰 |

---

# 附录 D：三条 query 的全流程走查

**D.1 被歧义闸门拦下**

> query（中文，电商领域）："根据上面的表格，帮我分析一下哪个渠道的转化率最高"

Stage 0 通过（非重复、完整、无 PII）。Stage 1 命中歧义清单 #2（引用不可见材料——表格不在数据里）。改写一致性测试佐证：两次改写分别虚构了不同的表格内容，意图不可恢复。**处置**：淘汰，`drop_reason = ambiguous_missing_context`。进反馈报告示例池：提示协作方交付时须附引用材料。

**D.2 进核心集**

> query（德语，法务领域）："Entwirf eine DSGVO-Auftragsverarbeitungsklausel für einen SaaS-Anbieter, der EU-Nutzerlogs in US-Rechenzentren speichert, max. 200 Wörter."（为在美国数据中心存储欧盟用户日志的 SaaS 供应商起草一条 GDPR 数据处理条款，不超过 200 词）

Stage 1 通过（自包含、无歧义、无时效问题）。Stage 2 得 6 分（specificity ✓ / domain_knowledge ✓ / complexity ✓ / problem_solving ✓ / creativity ✗ / technical_accuracy ✓ / real_world ✓）。Stage 3：rubric 定为"必须涉及第三国传输机制 / 必须是条款文体 / ≤200 词 / 不得虚构法条编号"，4 个模型独立打分得 [5, 4, 2, 2]，spread=3。**处置**：入核心集，`bucket = core`，`difficulty = hard`（低分模型的 failure_mode 均为 hallucination——虚构法条编号，这本身就是有价值的失败模式记录）。

**D.3 全低分桶的人工裁决**

> query（斯瓦希里语，医疗领域）：询问两种药物联用的相互作用与剂量调整。

Stage 1、2 通过（8 分制下得 5 分）。Stage 3 四个模型得 [2, 1, 1, 0]，全低分，进人工裁决。裁决按两步：① 题目完好性——query 自包含、医学上是真问题，非坏题；② judge 可靠性——按 §8.3 把 query 人工译为英文重跑，分数仍低，排除 judge 语言衰减。**处置**：确认是真硬题（小语种 × 专业领域叠加），`bucket = hard` 保留；同时因属医疗高风险，按 §7.3 Risk 覆盖加标 `risk = medical`，人工复核其 rubric 的安全红线项（是否要求"建议就医"声明）。

三条走查覆盖了三种典型命运：**坏题在花钱前被拦住，好题带着失败模式记录入集，疑难题经双重裁决后正名**。

---

# 参考来源

- LMSYS，[From Live Data to High-Quality Benchmarks: The Arena-Hard Pipeline](https://www.lmsys.org/blog/2024-04-19-arena-hard/)（7 判据、≥6 阈值、separability 87% vs MT-Bench 22%）
- Li et al., [From Crowdsourced Data to High-Quality Benchmarks: Arena-Hard and BenchBuilder Pipeline](https://arxiv.org/abs/2406.11939)（arXiv 2406.11939）
- 本项目 `docs/LLM_evaluation_framework.md` §4 Step 3（自建 eval set：50–200 条、抽检 20%）
- 本项目 `refer/evaluate/evaluate-Agent/` 系列笔记：`01`（Golden Dataset 规模与 40/40/20 难度配比）、`03`（Rubric = Dimensions + Scales + Descriptions；Observable / Discriminative / Actionable）、`04`（Judge 校准流程）、`05`（四类偏见与五种修正）、`06`（五类 Coverage 与 Dataset 治理）
- 本项目 skill：`.claude/skills/evaluate-llm/`（附录 B 的模板基底）

