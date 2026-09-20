# Agent 质检检测标准模板

模板用于正式标准，不用于承载批次统计或技术解析细节。章节可按算子复杂度裁剪；简单确定性算子不需要为了完整而写成长文。

## 文档头

```markdown
# <维度名称> —— 检测标准

- version: <v0.1>
- status: DRAFT / CALIBRATING / FROZEN / DEPRECATED
- applicable_data: <数据类型与 schema 版本>
- last_calibrated_at: <YYYY-MM-DD>
```

## 一、维度定义

### 1.1 Core question

> <本标准唯一回答的问题，尽量写成一句可判定的问题。>

### 1.2 缺陷命题

```text
当 <前置条件> 成立时，<被检行为> 出现 <直接冲突／缺失／越界>，构成本维度缺陷。
```

### 1.3 为什么影响训练

说明模型会从样本中学到什么错误关系。不要只写“质量不好”或“可能有风险”。

### 1.4 适用范围与明确排除

| 纳入 | 排除并转出到 |
|---|---|
| <当前维度直接检查的内容> | <相邻维度及原因> |

## 二、数据与证据契约

### 2.1 输入字段

列出原始输入、模型输出、环境反馈和必要元数据。旧标签、reason code 和算子 trigger 单列为参考字段。

### 2.2 可见范围

说明判断时允许使用哪些信息、截止到哪个时间点。禁止使用后续信息为当前步骤反向补证。

### 2.3 前置事实

列出进入判定链前需要确定、但本身不构成缺陷的事实。例如 schema 是否存在、内容是否进入上下文、事件是否发生。

## 三、判定结论

根据维度选择并定义结果，不必机械使用同一组枚举。至少区分：

| 语义 | 推荐结果 |
|---|---|
| 缺陷成立 | `DEFECT` / 维度专用错误名 |
| 已检查且未发现缺陷 | `PASS` |
| 当前对象不适用 | `NOT_APPLICABLE` |
| 有候选但证据不足或歧义未解 | `UNCERTAIN` |
| 数据损坏或定位失败 | `INVALID` |

`UNCERTAIN`、`NOT_APPLICABLE` 和 `INVALID` 均不能并入 PASS 或 FAIL。

## 四、判定链

先写总体流程，再展开每一步。

```text
前置门 → 证据抽取／规范化 → 逐项判断 → hard negative 排除 → 结论
```

根据算子原型替换中段：

- 结构校验：schema → normalized value → validator；
- 局部一致性：expected contract ↔ actual contract；
- 状态转移：S0 → event → S1 → action；
- 轨迹模式：events → bounded window → metric → exclusions；
- 声明溯源：claim → evidence requirement → bounded search；
- 信息变换：source ↔ product，以及 dependency → usage。

每一步说明：输入、产出、停止条件和弃权条件。

## 五、缺陷形态

| 形态 | 成立条件 | 必需证据 | Primary type |
|---|---|---|---|
| <名称> | <可复现规则> | <原文、字段或运行结果> | <枚举> |

同一案例可多标签时，说明 primary type 的选择顺序；不要依靠标注员自由发挥。

## 六、Hard negatives 与相邻边界

每个主要缺陷形态至少配置一个最接近的反例：

| 看起来像缺陷但不是 | 为什么不是 | 如何排除 | 转出维度 |
|---|---|---|---|
| <案例形态> | <原因> | <证据> | <如适用> |

额外检查：

- 当前／未来／过去／条件／备选／撤销；
- 操作对象／搜索位置／搜索内容／原因线索；
- 调用发生／执行成功／结果被使用；
- 数据缺失／证据不足／真实缺陷；
- 可修复格式问题／需要过滤的语义错误。

## 七、证据与输出要求

判错至少返回：

```yaml
case_id:
raw_locator:
label:
primary_type:
evidence_under_test:
comparison_evidence:
derived_facts:
rule_applied:
direct_conflict:
hard_negatives_excluded:
adjacent_dimension_check:
confidence_or_abstain_reason:
```

确定性算子还应保留原始 `value`，便于改阈值时不重跑全量。

## 八、严重度与处置

先完成缺陷判定，再讨论后果：

| 命中形态 | 训练影响 | 严重度 | 建议处置 | 处置范围 |
|---|---|---|---|---|

分别说明修复、Mapper、mask step、filter sample、只标记和人工复核的适用条件。处置动作不能反向定义缺陷。

## 九、单位与指标（按需展开）

只有在单位不同或会影响统计时详细填写：

```yaml
sampling_unit:
evidence_unit:
decision_unit:
disposition_unit:
aggregation_unit:
```

指标至少声明分子、分母、抽样来源和不可外推范围。若含弃权，coverage 与 defect rate 并列报告。

## 十、已知风险与待确认

| 风险／问题 | 影响 | 当前处理 | 阻塞冻结？ |
|---|---|---|---|

未验证的新规则标明成熟度，不与已验证规则混写成同一确定语气。

## 十一、校准记录

```yaml
discovery_set:
human_adjudication:
backlabel_summary:
validation_set:
validation_reviewer:
validation_mode: independent_reviewer / blinded_same_reviewer
validation_summary:
known_distribution_gaps:
recalibration_triggers:
```

## 配套文档，不写入标准正文

### 批次分析

- 当前批次规模与分布；
- 命中量、案例和聚集形态；
- 旧标签翻案情况；
- 定向样本的统计限制；
- 下一轮采样建议。

### 技术实现说明

- schema 和字段路径；
- 多种序列化兼容；
- locator 还原；
- normalization 与映射；
- 性能、流式读取和无效记录处理；
- 需要工程方确认的链路事实。

### 校准与验证报告

- 人工分歧；
- 回标差异；
- 独立验证指标；
- 分桶误差；
- 标准版本变化和验证集失效情况。
