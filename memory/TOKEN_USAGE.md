# Gemini API Token Usage 文档

## 官方文档参考
- https://ai.google.dev/gemini-api/docs/tokens
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/GenerateContentResponse

## Token 数据结构

当调用 `client.models.generate_content()` 后，响应对象包含 `usage_metadata` 属性：

### 字段说明

| 字段 | 属性名 | 说明 |
|------|--------|------|
| Input Tokens | `prompt_token_count` | 输入token数量（包含文本、图片、视频等） |
| Output Tokens | `candidates_token_count` | 输出token数量（不包含思考token） |
| Thinking Tokens | `thoughts_token_count` | 思考token数量（如果模型有思考能力） |
| Total Tokens | `total_token_count` | 总token数量 = input + output + thoughts |

**重要：Output 包含 thinking tokens**（官方文档明确）

## 运行日志格式

每次运行后，会在 `memory/token_usage.log` 中追加一行：

```
2026-02-21 10:30:00 UTC | Input: 1500 | Output: 300 | Total: 1800 | Cost: $0.0040
```

### 计费公式
- `Output = Total - Input`（因为 total = input + output）
- `Cost = (Input/1M * $2.00) + (Output/1M * $12.00)`

## 定价 (每1M tokens, USD)

### 当前使用模型: gemini-3-pro-preview

| 类型 | 价格 (USD) |
|------|-----------|
| Input | $2.00 |
| Output | $12.00 |
