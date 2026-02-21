# Gemini API Token Usage 文档

## 官方文档参考
- https://ai.google.dev/gemini-api/docs/tokens
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/GenerateContentResponse

## Token 数据结构

当调用 `client.models.generate_content()` 后，响应对象包含 `usage_metadata` 属性：

```python
response = client.models.generate_content(model="gemini-3-pro-preview", contents=prompt)
print(response.usage_metadata)
# 输出示例: prompt_token_count: 11, candidates_token_count: 73, total_token_count: 84
```

### 字段说明

| 字段 | 属性名 | 说明 |
|------|--------|------|
| Input Tokens | `prompt_token_count` | 输入token数量（包含文本、图片、视频等） |
| Output Tokens | `candidates_token_count` | 输出token数量（不包含思考token） |
| Thinking Tokens | `thoughts_token_count` | 思考token数量（如果模型有思考能力） |
| Total Tokens | `total_token_count` | 总token数量 = input + output + thoughts |

## 运行日志格式

每次运行后，会在 `memory/token_usage.log` 中追加一行：

```
2026-02-21 10:30:00 UTC | Input: 1500 | Output: 300 | Total: 1800
```

## 计费说明

- 100 tokens ≈ 60-80 个英文单词
- 1 token ≈ 4 个字符
- 费用按 input + output tokens 计算

## 定价 (每1M tokens, USD)

### 当前使用模型: gemini-3-pro-preview

| 类型 | 价格 (USD) |
|------|-----------|
| Input | $2.00 |
| Output | $12.00 |

### 其他模型参考

| 模型 | Input | Output |
|------|-------|--------|
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 |
| Gemini 2.5 Flash | $0.30 | $2.50 |
| Gemini 2.5 Pro | $1.25 | $10.00 |
| Gemini 3 Pro Preview | $2.00 | $12.00 |
| Gemini 3 Flash Preview | $0.50 | $3.00 |
