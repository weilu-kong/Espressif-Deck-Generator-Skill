---
name: espressif-deck-generator
description: 生成、重构、排版和交付 Espressif 风格的 HTML/Web 演示文稿。适用于产品技术介绍、客户提案、Webinar、Lightning Talk、展会说明、技术更新和方案架构 Deck。优先采用结构化 deck.yaml/deck.json + 固定 Renderer + Validator，核验产品事实并输出 HTML、standalone HTML、PDF；需要时再生成讲稿、逐页解析和来源清单。
---

# Espressif Deck Generator V2

本 Skill 用于制作稳定、可复用、可验证的 Espressif 风格 Web Deck。核心原则：**Content is generative. Layout is deterministic. Facts are verified. Output is validated.**

## 1. 先判断任务

当用户要求生成、重构或改版 Espressif/乐鑫风格演示文稿时使用本 Skill。默认目标是 HTML/Web Deck；不要把本 Skill 描述成完整 PPTX 引擎，除非当前项目另有 PPTX 工具链。

开始前确定：
- 语言：日文 / 中文 / 英文；
- 受众：客户技术人员 / 决策层 / 开发者 / 内部；
- 时长：Lightning Talk / 标准汇报 / Webinar；
- 重点产品或方案；
- delivery mode：`quick` / `standard` / `full`，默认 `standard`。

## 2. 标准工作流

1. 理解 brief 与受众。
2. 对芯片、SDK、协议版本、功耗、TX power、内存等时效性技术事实进行核验。
3. 先做 storyboard，再选择 slide archetype。
4. 优先生成 `deck.yaml` 或 `deck.json`，不要直接手写整套页面 CSS。
5. 运行 `scripts/render_deck.py` 生成 HTML。
6. 运行 `scripts/validate_deck.py`；严重错误必须修复后再交付。
7. 按 delivery mode 输出 standalone HTML / PDF / contact sheet / source manifest 等。

## 3. Hard Requirements

以下规则优先级最高：
- 不得杜撰技术规格或把旧示例当作当前事实。
- 产品事实优先核对 Espressif 官方产品页、Datasheet、TRM、Programming Guide、官方 GitHub/SDK 文档。
- Preliminary 产品必须明确标注资料状态或 revision。
- 不得用其他芯片/模组/开发板图片冒充目标产品。
- 不得把 AI 概念图静默当成官方产品图。
- 不允许破图、关键元素零尺寸、严重 console error。
- 不允许正文或关键元素越过 slide safe area；最终必须跑 validator。
- 正文不得为了塞内容而缩成投影不可读的小字；优先删减、拆页或换 archetype。
- 同类对比必须保持一致视觉形式：芯片对芯片、模组对模组、开发板对开发板。
- 不要在最终 HTML 上堆积大量一次性 inline CSS 来“补洞”；优先修改 deck spec、component 或 theme。

## 4. Default Design

默认采用：
- 1920×1080 logical canvas，16:9，整体等比缩放；
- Espressif dark visual system + 克制红色 accent；
- 瑞士网格与清晰的标题层级；
- 视觉优先，复杂关系用原生 HTML/CSS 架构图或流程图；
- 硬件展示框紧凑，大图优先，避免无意义留白；
- 页面外层保持通透，不给整页加厚重大外框；
- 文案像资深 FAE / 系统架构师：具体、客观、工程导向，不用空泛营销话术。

详细设计 Token 和历史经验见 `references/design-system.md`。

## 5. Optional Enhancements

以下不是硬性要求，只有在内容和现场环境合适时使用：
- ASCII / 光效动态背景；
- `B` 键动态/静态切换；
- 特殊转场；
- 逐页演讲稿；
- 深度技术解析与 Q&A；
- 大量动画。

动效绝不能优先于信息可读性和稳定性。

## 6. Structured Deck First

优先把内容写入结构化 Deck Spec：
- Schema：`schemas/deck.schema.json`
- 示例：`examples/lightning-talk.yaml`、`examples/technical-webinar.yaml`
- Renderer：`scripts/render_deck.py`

推荐命令：
```bash
python3 scripts/render_deck.py examples/lightning-talk.yaml -o output/deck.html
```
如果环境缺少 PyYAML：
```bash
uv run --with pyyaml python scripts/render_deck.py examples/lightning-talk.yaml -o output/deck.html
```

Renderer 负责尺寸、CSS、字体层级、grid、card、图片 fit、Logo/brand mark、页码、导航和缩放。Agent 主要负责内容、故事线、slide type 与 visual intent。

## 7. Slide Archetypes

优先从现有 archetype 中选，不要每页重新发明布局：
- `cover`
- `section`
- `product_compare`
- `product_detail`
- `spec_table`
- `architecture`
- `image_focus`
- `three_column`
- `ending`

选择规则和字段说明见 `references/slide-archetypes.md`。对应模板位于 `assets/templates/`。

## 8. Product Story

产品介绍推荐采用 5-Layer Product Story：
1. 分类标签 / 协议概览；
2. 产品名称 + 一句话定位；
3. 2–3 个工程价值点；
4. 主要用途；
5. Visual Evidence：官方芯片、模组、开发板或清晰架构图。

硬件图片必须足够大，避免“灰框很大、产品图很小”。

## 9. Fact Checking

详细规则见 `references/fact-checking.md`。特别注意：
- 不把具体产品参数长期硬编码在 Skill 主文件中；
- Matter / BLE / Wi-Fi / SDK 等版本信息在使用时重新核验；
- Fast Reflash 等性能描述使用机制性、条件化表述；除非有可靠 benchmark，否则不要给固定秒数承诺。

## 10. 日文文案

详细规则见 `references/copywriting-ja.md`。
- 自然日语优先，不机械给所有日文与数字/英文之间插空格；
- 技术术语优先行业常用写法；
- 避免中文直译式日语；
- 避免“完全”“革命性”等无依据绝对化表达；
- 用「〜を実現」「〜に対応」「〜をサポート」「〜に最適」等工程表达，但不要机械重复。

## 11. Image Policy

见 `references/image-policy.md`。默认优先级：
1. Espressif 官方产品图 / Datasheet 图；
2. 官方开发板/模组图；
3. 官方生态或合作伙伴公开素材；
4. 清楚标记的 illustration / concept。

所有图片保持比例，避免过度裁剪开发板、芯片和模组。

## 12. Validate Before Delivery

生成 HTML 后运行：
```bash
python3 scripts/validate_deck.py output/deck.html --report output/validation-report.json
```
如需 Playwright：
```bash
uv run --with playwright python scripts/validate_deck.py output/deck.html --report output/validation-report.json
```

必须重点检查：
- broken images；
- console/page errors；
- horizontal/vertical overflow；
- safe-area violations；
- 关键文本字号；
- slide ID；
- page number；
- zero-size important elements。

严重错误时 validator 返回非 0 exit code。

## 13. Delivery Modes

详细见 `references/delivery-modes.md`。

`quick`：HTML。

`standard`（默认）：HTML + standalone HTML + PDF。

`full`：standard + contact sheet + source manifest + speaker script + slide explanation（按任务需要生成）。

不要无条件生成讲稿和长篇解析。

## 14. Standalone HTML

运行：
```bash
python3 scripts/inline_assets.py output/deck.html -o output/deck_standalone.html --strict
```

打包后再次扫描 unresolved local dependencies。只有在本地资源完全内联或明确允许外链时，才称为 standalone。

## 15. PDF

Fidelity PDF：浏览器高分辨率截图后组合成 PDF，重点是视觉一致性，不要称为 vector/lossless PDF。
```bash
python3 scripts/export_pdf.py output/deck.html --mode fidelity -o output/deck_fidelity.pdf
```

Vector PDF：使用 Chromium print-to-PDF，尽量保留 selectable text 和 vector CSS/SVG。
```bash
python3 scripts/export_pdf.py output/deck.html --mode vector -o output/deck_vector.pdf
```

不要硬编码 macOS Chrome 路径；优先 Playwright Chromium，允许 `CHROME_PATH` override。

## 16. Contact Sheet

需要全局视觉复核时：
```bash
python3 scripts/make_contact_sheet.py output/deck.html -o output/deck_contact_sheet.png
```

用它快速判断整套 Deck 的节奏、重复度、图片比例和信息密度。

## 17. 资源读取原则

只在需要时读取 references，避免把所有知识一次塞入上下文：
- 视觉与尺寸：`references/design-system.md`
- 页面类型：`references/slide-archetypes.md`
- 技术核验：`references/fact-checking.md`
- 日文：`references/copywriting-ja.md`
- 图片：`references/image-policy.md`
- 交付：`references/delivery-modes.md`
- 演讲原稿：`references/speaker-script.md`
- 技术解析/Q&A：`references/slide-explanation.md`
- 来源清单模板：`references/source-manifest-template.md`

## 18. Final Preflight

交付前确认：
- [ ] 故事线符合受众和时间；
- [ ] 事实已核验，Preliminary 状态正确；
- [ ] 没有用错误产品图占位；
- [ ] 无明显小字、孤字和不自然换行；
- [ ] 硬件卡片紧凑，图片比例一致；
- [ ] 架构关系不是纯文字堆砌；
- [ ] Validator 无 blocking errors；
- [ ] standalone 无意外本地依赖；
- [ ] PDF 模式与命名准确；
- [ ] 只生成用户需要的交付物。
