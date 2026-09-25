# Espressif Deck Design System

## Intent

保持现代、工程化、通透的 Espressif 技术演示风格。重点不是装饰，而是远距离可读、对比清楚、硬件视觉突出。

## Logical canvas
- 1920×1080 logical pixels，16:9。
- `.deck-stage` 固定逻辑尺寸，JavaScript 根据 viewport 统一 scale。
- 推荐 safe area：左右 92 px，上 78 px，下 72 px；标题和页码另有固定区域。

## Core colors
- `--bg: #090b10`
- `--bg-soft: #11151d`
- `--panel: rgba(255,255,255,.055)`
- `--panel-strong: rgba(255,255,255,.085)`
- `--line: rgba(255,255,255,.15)`
- `--text: #f7f8fb`
- `--muted: rgba(247,248,251,.68)`
- `--accent: #e73536`
- `--accent-bright: #ff5a5c`
- `--success: #61d29b`
- `--blue: #6db7ff`

颜色可由项目主题覆盖，但同一 Deck 内需保持一致。

## Typography
以投影可读性为基准，不为了塞内容无底线缩字。
- Cover hero：78–112 px 视标题长度自动选择。
- Slide title：54–68 px。
- Section title：72–96 px。
- Card title：26–32 px。
- Body：22–26 px。
- Secondary/spec：18–21 px。
- Meta/caption：16–18 px；除法律性/来源性脚注外不要低于 16 px。

优先通过删减、拆页、改 layout 解决内容过多。

## Spacing
- 主内容左右安全边距约 92 px。
- 标题和正文间 18–30 px。
- 卡片 gap 22–34 px。
- 卡片 padding 24–32 px。
- 同一组件使用一致 spacing token，不要每页手写随机 margin。

## Cards
- 卡片只作为内部信息分组，不给整页套“大相框”。
- 推荐：半透明背景 + 1 px 低对比线 + 14–22 px radius。
- 多列对比卡片应等高或视觉基线一致。

## Hardware visual cards
历史问题：容器膨胀、硬件图过小、不同形态混搭。

规则：
- 容器根据内容收紧，不给硬件展示区使用无意义的 `flex:1`。
- 模组主图建议实际显示高 150–210 px。
- 开发板/整机建议 190–280 px。
- `object-fit: contain`，保留完整轮廓。
- 图片可使用克制的 drop shadow 增强暗背景辨识度。
- 多产品对比使用同类视觉证据：module vs module / board vs board。

## Visual-first diagrams
以下内容优先图解：
- 设备到云的数据链路；
- 双协议协同；
- 状态机；
- 认证/commissioning 流程；
- Host + connectivity companion；
- Edge AI pipeline。

优先使用 HTML/CSS 原生 node + connector，以获得清晰文本。Mermaid 适合较复杂图，但必须控制字号和节点数量。

## Motion
动效是 optional enhancement。
- 动效不得影响截图/PDF 稳定性。
- `body.motion-off` 时必须可完全停止背景动画和 transition。
- PDF 导出前由脚本自动关闭 transition/animation。

## Dense slides
如果一页需要：
- 3 个以上大段文字；
- 5 列以上复杂表格；
- 4 个以上硬件大图；
优先拆页，不要继续压缩字号。
