# 参数配置标准格式（input_schema）

`input_schema` 是 shareable skill 参数配置的唯一标准存储位，格式为 json/jsonb。

## 标准结构

```json
{
  "zh": {
    "<param_name>": {
      "type": "input | select | multiple",
      "label": "中文标签",
      "default": "默认值",
      "options": [
        { "label": "显示名", "value": "actual_value" }
      ],
      "description": "中文描述",
      "required": true
    }
  },
  "en": {
    "<param_name>": {
      "type": "input | select | multiple",
      "label": "English Label",
      "default": "default value",
      "options": [
        { "label": "Display Name", "value": "actual_value" }
      ],
      "description": "English description",
      "required": true
    }
  }
}
```

## 必填字段

每个参数必须包含以下 6 个字段：

- `type`
- `label`
- `default`
- `options`
- `description`
- `required`

## type 规则

- `input`：文本或数字输入；`options` 必须是 `[]`
- `select`：单选下拉；`default` 必须是 `options[].value` 中的一个值
- `multiple`：多选组件；`default` 必须是数组，且每个值都必须存在于 `options[].value`

## 强校验规则

- 顶层必须同时有 `zh` 和 `en`
- `zh` 和 `en` 的参数 key 必须完全一致
- `zh/en` 的 `type` / `default` / `required` 必须一致
- `zh/en` 的 `options[].value` 必须一致；`label` 可以不同
- `required` 必须是 boolean，不能是字符串
- `options` 不能为空字段；`input` 类型也必须显式填 `[]`
- `options[]` 每项必须包含 `label` 和 `value`
- `value` 是实际传给后端的值，`label` 只是展示文案

## 旧格式迁移

- `string` 且无 `enum` → `input`
- `string` 且有 `enum` → `select`
- `number` / `integer` → `input`
- `array` → `multiple`
- 原 required 数组中存在 → `required: true`
- 原 required 数组中不存在 → `required: false`
