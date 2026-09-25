# Slide Archetypes

## `cover`
用途：开场。字段：`title`, `subtitle`, `eyebrow`, `presenter`, `company`, `date`, `theme`。
默认视觉：大标题、少信息、高留白，可启用背景光效。

## `section`
用途：章节切换。字段：`title`, `subtitle`, `eyebrow`。
不要放复杂列表。

## `product_compare`
用途：2–3 个产品并列。字段：`products[]`，每个 product 可含 `name`, `badge`, `positioning`, `highlights[]`, `applications[]`, `image`, `specs{}`。
规则：视觉证据必须同类；推荐 2 列或 3 列，不要 4 列塞满。

## `product_detail`
用途：单一产品重点。字段与 product 相同，可增加 `hero_stat`, `notes`。
适合突出定位、关键工程价值和大图。

## `spec_table`
用途：规格横向比较。字段：`columns[]`, `rows[]`。
规则：表格不是 Datasheet 搬运；只保留决策相关字段。列过多时拆页。

## `architecture`
用途：流程、系统架构、协议协同。字段：`nodes[]`, `connections[]`, `groups[]`。
节点字段：`id`, `label`, `detail`, `tone`。连接字段：`from`, `to`, `label`。
Renderer 当前以稳健的顺序 pipeline / grouped-node 表达为主；复杂自由拓扑可在项目层扩展。

## `image_focus`
用途：开发板、模组、产品照片、现场图。字段：`image`, `caption`, `fit`, `bullets[]`。
图片是页面主角，文字应少。

## `three_column`
用途：三个支柱、三个方案、三个步骤、三个生态组件。字段：`columns[]`，每列含 `title`, `body`, `bullets[]`, `icon`。

## `ending`
用途：总结 / Thank you / CTA。字段：`title`, `subtitle`, `contact`, `qr_image`。
保持简洁，不在结尾继续塞技术参数。

## Choosing an archetype
- 一张页面只回答一个核心问题。
- 两个产品 → `product_compare`。
- 单产品价值 → `product_detail`。
- 多指标横向判断 → `spec_table`。
- 谁连接谁、数据怎么走 → `architecture`。
- 图比文字更重要 → `image_focus`。
- 三个并列概念 → `three_column`。
