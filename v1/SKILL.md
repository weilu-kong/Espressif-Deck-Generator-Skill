---
name: espressif-deck-generator
description: 当用户要求生成、制作、重构、排版或全案交付乐鑫风格的演示文稿（Espressif Web Deck / HTML 幻灯片）时触发。严格遵循历次实战调优沉淀的高精度设计系统、字号梯队、硬件紧凑展示框、图解优先（Native 流程图卡片）、中日文半角空格排版、通透无外框视觉、Humanizer 原厂严谨文风与真实 Datasheet/生态套件核查标准，交付包含交互网页、自包含单文件发布版、1080p PDF、逐页深度技术解析与结构化演讲原稿的全套工程化成果。
---

# Espressif Deck Generator 生产级实战规范指南

本规范基于真实业务场景（从早期演示版到高精度投屏版 `latest_progress.html`，以及客户 Webinar / Lightning Talk 全案交付经验）历经多轮现场视效调优、实机投屏检验与讲者演讲节奏实测沉淀而成。

当用户需要制作或交付乐鑫风格的介绍资料时，你交付的不应仅仅是一个简单的 HTML 页面，而是一套**兼具视觉震撼、技术严谨、自包含防破图分发、高保真 1080p PDF 导出、精准控时演说稿以及深度技术拆解手册的完整工程化全套交付体系**。

---

## 一、Espressif 演示项目完整工程构成体系 (Standard Project Blueprint)

一个标准的乐鑫演示项目仓库，由以下核心文件矩阵构成：

```
<project-root>/
├── latest_progress.html            # ① 核心交互式演示网页 (1080p 纯 16:9 画布 / 动效引擎 / ESC 索引矩阵)
├── latest_progress_standalone.html # ② 独立自包含单文件分发版 (全图片 Base64 内联，零外部依赖，防丢图)
├── export_pdf.py                   # ③ 1080p 标准高清 PDF 自动化导出套件 (基于 Playwright + Chrome 无头渲染)
├── <Presentation_Name>_1080p.pdf   # ④ 工业级 1080p PDF 演示文档 (1920x1080 精准输出，供离线投屏与归档)
├── speech_script_ja.md             # ⑤ 结构化演讲原稿与时间控制方案 (含时间配分表、秒级时间戳、翻页标记)
├── slides_explanation_zh.md        # ⑥ 逐页技术深度拆解与 Q&A 应对指南 (设计意图、Datasheet 硬指标、Q&A 预案)
├── assets/                         # ⑦ 官方矢量 Logo (logo-espressif-white.svg / red-black.svg) 与 motion.min.js
└── images/                         # ⑧ 高分辨率透明底实物芯片、模组与开发板特写图 (PNG / JPG)
```

### 各文件核心定位与标准生成时序
1. **第一步（需求与大纲分析）**：明确受众（技术开发者、客户决策层、生态伙伴）、演讲时长限制（如 5 分钟 LT 或 30 分钟 Webinar）与核心重点芯片/方案。
2. **第二步（构建交互网页 `latest_progress.html`）**：采用规范语义 DOM、Carbon 色彩 Token、严格字号阶梯与紧凑硬件展示框。
3. **第三步（打包自包含发布版 `*_standalone.html`）**：调用内联工具将所有 SVG/PNG/JPG 转为 Base64，确保脱离本地目录后分发绝不破图。
4. **第四步（自动化导出 1080p PDF）**：运行 `export_pdf.py`，经无头 Chrome 渲染抓取并自动消除 UI 控件，输出纯净 1080p PDF。
5. **第五步（编写深度技术解析手册 `slides_explanation_zh.md`）**：逐页标注技术硬指标的官方 Datasheet/TRM 依据、技术亮点与潜在高频 Q&A 应对策略。
6. **第六步（编写严格控时的演讲原稿 `speech_script_ja.md`）**：严格换算字数与语速，设立时间配分表与正文秒级时间戳，标注翻页时机。

---

## 二、历次实战调优沉淀的 10 大黄金法则 (The 10 Golden Rules)

在生成任何幻灯片代码与配套交付物时，必须严格执行以下十大准则：

### 1. 硬件展示框严禁留白膨胀，必须“收紧容器 + 大图突出 + 格式对齐”
* **历史痛点**：此前在展示模组或开发板照片时，容器经常被误加上 `flex: 1`，导致灰色背景框上下过度拉伸，留出大量空旷的无效灰色空白；而内部的核心芯片照片却被挤压成 80px~100px 的微缩图；此外，左右对比时一侧放概念芯片图、另一侧放实物开发板，造成视觉严重不对称与层级混乱。
* **强制标准**：
  * **严禁展示框使用 `flex: 1`**：外层展示框必须根据内容自适应收紧（紧凑高度），禁止盲目膨胀。
  * **照片尺寸放大 200% 以上**：
    * 单个模组照片（如 `S31-WROOM-1`、`C5-MINI-1`）：高度设为 **`140px ~ 180px`**。
    * 开发板/整机套件特写（如 `ESP32-S31-Korvo-1`, `ESP32-C5-DevKitC-1`）：高度设为 **`190px ~ 240px`**。
    * 照片必须具备：`width: auto; object-fit: contain; filter: drop-shadow(0 14px 28px rgba(0,0,0,0.85));`。
  * **展示格式必须严格对齐**：对比多个芯片或方案时，视觉形式必须保持对称统一。芯片对应芯片，开发板对应官方评估板，严禁概念抽象图与实物板混搭。
  * **容器样式规范**：
    `padding: 1.2vh 1.2vw; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.16); min-height: 180px; display: flex; align-items: center; justify-content: space-around; gap: 1vw; margin-top: 0.6vh;`
  * **去除上下脱节**：消除上半部分文字与下半部分展示框之间过大的空白间距（上边距控制在 `0.6vh ~ 1vh`），使整个卡片内容充实、信息连贯。

### 2. 严格管控字号梯队，彻底杜绝“微型小字”
* **历史痛点**：模组尺寸、Flash/PSRAM 容量、接口数量等信息容易被写成 9px~11px 的超小字体，在会议室投影仪或大屏演讲时后排观众完全无法看清。
* **强制标准**：
  * **主标题（H1）**：`font-size: min(5.6vw, 9.2vh);`（封面）/ `min(7vw, 12vh);`（封底）。
  * **单页大标题（H2）**：`font-size: min(3.6vw, 5.8vh); white-space: nowrap;`。
  * **卡片标题（H3）**：`font-size: max(18px, 1.25vw);`。
  * **正文（Body）**：`max(14px, 0.95vw)` 至 `max(15px, 1.05vw)`。
  * **二级参数/规格说明（Specs/Dimensions/Flash/Notes）**：**必须保持比正文仅小一号**，统一定义为 **`max(12.5px, 0.82vw)` 至 `max(13.5px, 0.9vw)`**。**绝对禁止出现低于 12px 的文本**！
  * **型号大标题（MPN）**：`max(15px, 1.05vw)`，加粗 `font-weight: 700; font-family: var(--mono);`。
  * **标签与元数据（Tag/Kicker/Meta）**：`max(11px, 0.72vw)` 至 `max(12px, 0.78vw)`。

### 3. 技术内容架构标准：4 段式价值闭环
任何芯片、硬件产品或框架的介绍卡片，不得只罗列干瘪的参数名词，必须严格按照以下结构组织：
1. **顶部分类标签 + 协议概览**：如 `<span class="tag accent">AI MULTI-PROTOCOL</span>` + `Wi-Fi 6 · BT Classic / BLE 5.4 · 802.15.4`。
2. **产品名称与一句话定位**：如 `ESP32-S31`，320 MHz 双核 RISC-V + 128-bit SIMD 的边缘 AI・语音・HMI 特化主控。
3. **おすすめポイント (Key Highlights)**：2~3 点带粗体标题的硬核工程优势（痛点解决，而非空泛宣传）。
4. **主な用途 (Primary Applications)**：清晰指明落地产品形态（如智能音箱、会议音频、穿戴设备、工业网关）。
5. **硬件紧凑展示框**：大图 + 封装/天线型号 + 内存规格 + 引脚数。

### 4. 语气规范与 Humanizer 严选文风（拒绝 AI 假大空与中式生硬直译）
* **核心基调**：必须以乐鑫一线资深 FAE / 系统架构师的专业、严谨、客观、务实语气书写，杜绝销售式空话。
* **杜绝中式技术文档生硬直译**：中日文互译时严禁使用生硬的中文词汇直接当做日文：
  * ❌ `下発` $\to$ ✔️ `配信` / `送信` / `設定・配信`
  * ❌ `配網` $\to$ ✔️ `コミッショニング`（Commissioning）
  * ❌ `単核` $\to$ ✔️ `シングルコア`
  * ❌ `上位機` $\to$ ✔️ `ホストコントローラ` / `ホスト PC`
* **剔除 AI 虚夸词与绝对化口吻**（“完全”泛滥是典型 AI 特征）：
  * ❌ `完全克服` $\to$ ✔️ `大幅に低減`
  * ❌ `完全同一` $\to$ ✔️ `同等の`
  * ❌ `完全監査ログ` $\to$ ✔️ `詳細な監査ログ`
  * ❌ `完全オフライン自律駆動` $\to$ ✔️ `オフライン自律駆動`
  * ❌ `SoC 内蔵 RTC で完全照合` $\to$ ✔️ `SoC 内蔵 RTC のみで自律照合`
* **聚焦工程痛点与客户价值**：以「〜を実現」「〜に対応」「〜をサポート」「〜に最適」为主，聚焦解决客户实际工程痛点（如 5 GHz 回避电波干扰、DC-DC 超低接收电流达成数年电池续航、M5Stack 模块化免焊接快速搭建样机验证），严禁空洞的宣讲式口号。

### 5. 排版与半角空格规范（中日文与西文/数字混排）
* **强制半角空格**：在日文/中文技术文档中，汉字/假名与英文字母、阿拉伯数字之间**必须插入半角空格**（如 `Matter 1.6`、`Apple Home Key`、`< 0.5 秒`、`ESP32-C5`、`2.4 / 5 GHz`、`2026 年 6 月`、`1 チップ`、`4 MB PSRAM`）。这是衡量专业度和排版品质的硬指标。
* **行尾断词与防孤字（Orphan Prevention）**：列表项与正文必须进行字数调优与排版检查，严禁换行后只留下两三个字的孤字脱节悬挂，必须自然铺满或整齐成行。
* **封面规范分行**：演讲人信息必须逐行独立分行，保证视觉呼吸感（公司名、职务与姓名、发表时间）。

### 6. 图解优先法则：复杂逻辑严禁纯文字堆砌，强制采用高对比矢量流程图
* **痛点反思**：“通篇文字、照片很少、缺乏图解心智”是低质技术汇报的通病。幻灯片核心目的是沟通与展示，必须“图解优先（Visual First）”。
* **强制图解场景**：双协议协同（如 Matter 远端管理 + Aliro 门前即时认证）、多阶段鉴权状态机（5 步鉴权）、事件联动流水线、软硬件交互拓扑，**绝对禁止只写干瘪文字列表**，必须配以直观清晰的架构图/流程图。
* **图解实现优先级与技术规范**：
  1. **首选 Native HTML/CSS 流程卡片**：在当前幻灯片体系中，原生 HTML/CSS 卡片（利用 Flex/Grid、圆圈数字标号、下行箭头分隔符、语义化色系边框如 blue/accent/green、13px~15px 可读字号）具有最高清晰度，在任何高分屏/投影仪下都不会模糊失真，文字绝不挤压重叠，与暗黑主题完全融合。
  2. **Mermaid 规范**：若使用 Mermaid，必须预留充分的容器宽度与高度，并显式设置全局 themeVariables 和字号（`fontSize: 13px` 以上），严禁节点文字过小、引线交叉错乱或重叠压线。
* **官方高清透明图片检索**：不得局限于本地旧图，必须主动从乐鑫官方文档中心（`docs.espressif.com`）、官方组件库、SDK 官方仓库（ESP-IDF、ESP-Matter、ESP-Aliro 等）中搜索并下载高质量透明底实物/渲染图，保存在本地 `images/` 并规范引用。严禁缩小成看不清细节的微缩图。

### 7. 视觉通透性与画布外框准则（拒绝压抑的“画地为牢”外框）
* **拒绝整页大外框**：严禁在每页幻灯片最外层套用大边框（“把每一页都框住，视觉效果很差，像画地为牢”）。
* **通透的暗黑空间感**：画布整体应保持现代、通透、大气的暗黑/瑞士网格空间感。边框仅允许作为内部独立功能卡片或对比模块的微弱分隔（如 `border: 1px solid rgba(255,255,255,0.14)`），外层仅保留顶部极简 Chrome 条和底部页码。

### 8. 动态/静态双模视效与流光背景规范
* **氛围流光背景**：封面、封底及关键页面必须配置沉浸式光效（如动态 ASCII 点阵流光场 `ascii-bg` 或呼吸渐变光晕），提升质感与惊艳度。
* **B 键快捷切换**：交互系统必须内置键盘事件监听，支持按快捷键 `B` 快速在“动态模式 / 静止模式”之间切换，以适应现场低算力设备、投影仪或投屏录制的性能与稳定性需求。

### 9. 硬件信息精准度与生态套件区分法则
* **最新官方开发板直出**：芯片一旦正式推出官方开发板（如 ESP32-C5-DevKitC-1 已有板），**严禁继续使用前代/其他芯片（如 C6）作为占位或借代**，必须直接以最新官方评估板呈现。
* **官方 DevKit 与生态套件（M5Stack 等）明确区分定位**：
  * **原厂官方 DevKit**：用于芯片级/模组级先行开发、射频指标评估、底层驱动调试。
  * **第三方生态套件**（如 M5Stack Controller、M5Stack NFC Unit、M5Stack Nano H2 / NanoC6）：用于免焊接、桌面即插即用的客户快速 PoC 演示、高管汇报及即日功能闭环体验。

### 10. 官方 MCP 与 Datasheet 硬核事实校验
涉及芯片参数、SDK 版本特性时，严禁脑补，必须核对官方文档：
* **ESP32-H4**：发射功率范围是 `-24 ~ +6 dBm`（官方限制最大 +6 dBm 以换取超低电流，绝不可写成 +20 dBm；+20 dBm 是 H2/H21）。
* **ESP32-H21**：最大卖点是引入片上高效率开关型 DC-DC，RX 接收电流降至 **8.2 mA**。
* **ESP32-S31**：320 MHz 双核 RISC-V + 128-bit SIMD 扩展，经典蓝牙 (BR/EDR) 重磅回归 + BLE 5.4 + Wi-Fi 6。
* **ESP32-C5**：2.4 GHz + 5 GHz 双频 Wi-Fi 6 (802.11ax)。
* **Fast Reflash (IDF 6.1)**：基于 4 KB 扇区差分对比，日常代码修改烧录由 10~15 秒缩短至 1~2 秒。

---

## 三、常用页面母版原型代码 (Slide Archetypes)

直接复制以下母版结构并填充内容，即可保证生成效果达到调优后的最优水准。

### Archetype 1: 瑞士网格封面 (Cover Slide)
适合作为演讲开篇，搭载 ASCII 动态点阵呼吸场与严谨的演讲人分行布局。

```html
<section class="slide accent" data-layout="SWISS-COVER-ASCII" data-animate="hero">
  <div class="brand-logo"><img src="assets/logo-espressif-white.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--accent); color: var(--accent-on);">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min">
      <div class="l"><span style="color: rgba(255,255,255,0.78);">LIGHTNING TALK · 2026</span></div>
      <div class="r"><span style="color: rgba(255,255,255,0.78);">01 / 08</span></div>
    </div>
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
      <span class="kicker no-line" style="margin-bottom: 2.2vh; color: rgba(255,255,255,0.85); font-size: max(15px, 1.05vw); letter-spacing: 0.16em;">
        LATEST TECH UPDATES 2026
      </span>
      <h1 class="h-hero-zh" style="color: #fff; font-size: min(5.6vw, 9.2vh); font-weight: 300; line-height: 1.18; letter-spacing: -0.015em; white-space: nowrap;">
        Espressif Systems<br>製品アップデートと最新動向
      </h1>
      <div style="margin-top: 4.2vh; display: flex; flex-direction: column; align-items: center; gap: 0.8vh; color: rgba(255,255,255,0.92); font-family: var(--mono); font-size: max(18px, 1.25vw); letter-spacing: 0.08em;">
        <div>楽鑫ジャパン株式会社</div>
        <div style="font-size: max(16px, 1.1vw); opacity: 0.88;">Field Application Engineer 孔 維魯</div>
        <div style="font-size: max(16px, 1.1vw); opacity: 0.88;">2026 年 9 月</div>
      </div>
    </div>
  </div>
</section>
```

---

### Archetype 2: 双旗舰硬件对比页 (Dual Hardware Slide)
核心模式：左右两栏紧凑卡片，包含清晰的推荐要点、应用领域及下方 200% 放大的紧凑模组展示框。

```html
<section class="slide dark">
  <div class="brand-logo"><img src="assets/logo-espressif-white.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--ink); color: var(--paper);">
    <div class="chrome-min">
      <div class="l">LATEST HARDWARE · S &amp; C SERIES</div>
      <div class="r">03 / 08</div>
    </div>
    <div class="frame col" style="padding-top: 1vh; flex: 1; display: flex; flex-direction: column;">
      <div>
        <h2 class="h-xl-zh" style="font-size: min(3.6vw, 5.8vh); line-height: 1.15; white-space: nowrap;">
          最新 SoC: ESP32-S31 &amp; ESP32-C5
        </h2>
        <p class="body-sm" style="margin-top: 0.3vh; color: rgba(255,255,255,0.7); font-size: max(13.5px, 0.9vw);">
          AI 音声・HMI ディスプレイ向け高性能 SoC と、2.4/5 GHz デュアルバンド Wi-Fi 6 SoC
        </p>
      </div>

      <div class="grid-2-6-6" style="margin-top: 1.2vh; gap: 1.8vw; align-items: start;">
        <!-- 左卡片 (S31) -->
        <div class="col" style="border: 1px solid rgba(255,255,255,0.18); padding: 1.8vh 1.5vw; border-radius: 10px; display: flex; flex-direction: column; gap: 1vh; background: rgba(255,255,255,0.02);">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="tag accent" style="font-size: max(11px, 0.72vw);">AI MULTI-PROTOCOL</span>
              <span class="t-meta" style="color: rgba(255,255,255,0.65); font-size: max(12px, 0.78vw);">Wi-Fi 6 · BT Classic / BLE 5.4 · 802.15.4</span>
            </div>
            <h3 class="h-md" style="font-size: max(18px, 1.25vw); margin-top: 0.4vh;">ESP32-S31</h3>
            <p style="font-size: max(13px, 0.85vw); color: rgba(255,255,255,0.75); margin-top: 0.2vh;">
              320 MHz デュアル RISC-V + 128-bit SIMD によるエッジ AI・音声・HMI 特化 SoC
            </p>
          </div>

          <!-- おすすめポイント & 主な用途 -->
          <div style="display: flex; flex-direction: column; gap: 0.6vh; font-size: max(13.5px, 0.9vw); line-height: 1.5; color: rgba(255,255,255,0.9);">
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">おすすめポイント:</span>
              <ul style="padding-left: 1.2em; margin-top: 0.2vh;">
                <li><strong>エッジ AI 演算:</strong> 128-bit SIMD 搭載、音声対話・軽量画像認識の演算を高速化</li>
                <li><strong>マルチメディア:</strong> DVP カメラ、RGB LCD、JPEG、2D 描画 PPA 統合</li>
                <li><strong>通信 &amp; クラシック BT:</strong> クラシック Bluetooth (BR/EDR) 再対応 + BLE 5.4、GbE</li>
              </ul>
            </div>
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">主な用途:</span>
              音声対話端末、高精細 HMI、スマートスピーカー・通話機器
            </div>
          </div>

          <!-- 紧凑模组展示框 (无 flex:1，大图突出) -->
          <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.16); border-radius: 8px; padding: 1.2vh 1.2vw; display: flex; align-items: center; justify-content: space-around; gap: 1vw; margin-top: 0.6vh; min-height: 180px;">
            <div style="display: flex; align-items: center; gap: 1vw;">
              <img src="images/ESP32-S31-WROOM-1.png" style="height: 145px; width: auto; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));" alt="ESP32-S31-WROOM-1">
              <div>
                <div class="t-meta" style="color: rgba(255,255,255,0.6); font-size: max(11px, 0.74vw);">汎用 (PCB)</div>
                <div style="font-family: var(--mono); font-size: max(15px, 1.05vw); font-weight: 700; color: #fff;">S31-WROOM-1</div>
                <div style="font-size: max(12.5px, 0.82vw); color: rgba(255,255,255,0.85); line-height: 1.35; margin-top: 2px;">
                  25.5 × 18.0 mm<br>Flash 8~32MB · PSRAM 16MB
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右卡片 (C5) -->
        <div class="col" style="border: 1px solid rgba(255,255,255,0.18); padding: 1.8vh 1.5vw; border-radius: 10px; display: flex; flex-direction: column; gap: 1vh; background: rgba(255,255,255,0.02);">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="tag" style="background: rgba(255,255,255,0.15); color: #fff; font-size: max(11px, 0.72vw);">DUAL-BAND WI-FI 6</span>
              <span class="t-meta" style="color: rgba(255,255,255,0.65); font-size: max(12px, 0.78vw);">2.4/5 GHz Wi-Fi 6 · BLE 5.3 · 802.15.4</span>
            </div>
            <h3 class="h-md" style="font-size: max(18px, 1.25vw); margin-top: 0.4vh;">ESP32-C5</h3>
            <p style="font-size: max(13px, 0.85vw); color: rgba(255,255,255,0.75); margin-top: 0.2vh;">
              2.4 GHz &amp; 5 GHz デュアルバンド対応、干渉に強く安定した低遅延通信を実現
            </p>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.6vh; font-size: max(13.5px, 0.9vw); line-height: 1.5; color: rgba(255,255,255,0.9);">
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">おすすめポイント:</span>
              <ul style="padding-left: 1.2em; margin-top: 0.2vh;">
                <li><strong>5 GHz 帯対応:</strong> 混雑の少ない 5 GHz 帯により、医療・産業や密集環境での通信安定性向上</li>
                <li><strong>Wi-Fi 6 特性:</strong> OFDMA・MU-MIMO・TWT（省電力ターゲットウェイクタイム）対応</li>
                <li><strong>マルチプロトコル:</strong> Thread / Zigbee との同時通信によるスマートホーム親機化</li>
              </ul>
            </div>
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">主な用途:</span>
              産業・医療 IoT 機器、家庭用ゲートウェイ・中継器、スマートカメラ
            </div>
          </div>

          <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.16); border-radius: 8px; padding: 1.2vh 1.2vw; display: flex; align-items: center; justify-content: space-around; gap: 1vw; margin-top: 0.6vh; min-height: 180px;">
            <div style="display: flex; align-items: center; gap: 0.8vw;">
              <img src="images/ESP32-C5-WROOM-1.jpg" style="height: 140px; width: auto; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));" alt="ESP32-C5-WROOM-1">
              <div>
                <div class="t-meta" style="color: rgba(255,255,255,0.6); font-size: max(11px, 0.74vw);">標準サイズ</div>
                <div style="font-family: var(--mono); font-size: max(14px, 0.95vw); font-weight: 700; color: #fff;">C5-WROOM-1</div>
                <div style="font-size: max(12px, 0.78vw); color: rgba(255,255,255,0.85); line-height: 1.35; margin-top: 2px;">
                  27.5 × 18.0 mm<br>Flash 4~32MB
                </div>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.8vw;">
              <img src="images/ESP32-C5-MINI-1.png" style="height: 125px; width: auto; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));" alt="ESP32-C5-MINI-1">
              <div>
                <div class="t-meta" style="color: rgba(255,255,255,0.6); font-size: max(11px, 0.74vw);">超小型</div>
                <div style="font-family: var(--mono); font-size: max(14px, 0.95vw); font-weight: 700; color: #fff;">C5-MINI-1</div>
                <div style="font-size: max(12px, 0.78vw); color: rgba(255,255,255,0.85); line-height: 1.35; margin-top: 2px;">
                  21.3 × 15.4 mm<br>Flash 4MB
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### Archetype 3: 多チップ低功耗/规格横向对比表 (Spec Table Slide)
适合对比芯片族谱（如 H2 vs H21 vs H4），采用清晰的数据表格与重点差异高亮。

```html
<section class="slide dark">
  <div class="brand-logo"><img src="assets/logo-espressif-white.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--ink); color: var(--paper);">
    <div class="chrome-min">
      <div class="l">LOW POWER &amp; 802.15.4 · H-SERIES</div>
      <div class="r">04 / 08</div>
    </div>
    <div class="frame col" style="padding-top: 0.5vh">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.8vh;">
        <div>
          <div class="t-meta" style="color: var(--accent-bright); font-size: max(11.5px, 0.76vw);">LOW POWER 802.15.4 &amp; BLUETOOTH LE</div>
          <h2 class="h-xl-zh" style="font-size: min(3.6vw, 5.8vh); line-height: 1.15; white-space: nowrap;">
            ESP32-H2 / H21 / H4 比較
          </h2>
        </div>
        <p class="body-sm" style="color: rgba(255,255,255,0.65); font-size: max(12.5px, 0.82vw); text-align: right;">
          長寿命バッテリー駆動 IoT 機器に向けた超低消費電力ワイヤレス SoC
        </p>
      </div>

      <!-- 参数对比表 (字号受严格保障，保持清晰可见) -->
      <div style="overflow-x: auto; margin-top: 0.6vh;">
        <table style="width: 100%; border-collapse: collapse; font-size: max(13px, 0.86vw); text-align: left;">
          <thead>
            <tr style="border-bottom: 2px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.7); font-family: var(--mono); font-size: max(12px, 0.78vw);">
              <th style="padding: 1.2vh 1vw;">型番</th>
              <th style="padding: 1.2vh 1vw;">CPU / メモリ</th>
              <th style="padding: 1.2vh 1vw;">送信出力 (TX)</th>
              <th style="padding: 1.2vh 1vw;">受信電流 (RX)</th>
              <th style="padding: 1.2vh 1vw;">スリープ電流</th>
              <th style="padding: 1.2vh 1vw;">電源回路</th>
              <th style="padding: 1.2vh 1vw;">主なターゲット</th>
            </tr>
          </thead>
          <tbody style="line-height: 1.5;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
              <td style="padding: 1.2vh 1vw; font-weight: 700; font-family: var(--mono); color: #fff;">ESP32-H2</td>
              <td style="padding: 1.2vh 1vw;">96MHz 単核 RISC-V<br>320KB SRAM</td>
              <td style="padding: 1.2vh 1vw;"><span class="mark" style="color: #fff; background: rgba(230,0,18,0.3); padding: 2px 6px; border-radius: 4px;">最大 20 dBm</span></td>
              <td style="padding: 1.2vh 1vw;">~24 mA (BLE)<br>~25 mA (15.4)</td>
              <td style="padding: 1.2vh 1vw;">Deep-Sleep: 7 µA<br>Light-Sleep: 25 µA</td>
              <td style="padding: 1.2vh 1vw;">内部 LDO</td>
              <td style="padding: 1.2vh 1vw; color: rgba(255,255,255,0.8);">常時給電ルーター、長距離通信ノード</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.03);">
              <td style="padding: 1.2vh 1vw; font-weight: 700; font-family: var(--mono); color: var(--accent-bright);">ESP32-H21</td>
              <td style="padding: 1.2vh 1vw;">96MHz 単核 RISC-V<br>320KB SRAM</td>
              <td style="padding: 1.2vh 1vw;"><span class="mark" style="color: #fff; background: rgba(230,0,18,0.3); padding: 2px 6px; border-radius: 4px;">最大 20 dBm</span></td>
              <td style="padding: 1.2vh 1vw; font-weight: 600; color: var(--accent-bright);">約 8.2 mA (65% 削減)</td>
              <td style="padding: 1.2vh 1vw;">Deep-Sleep: 5 µA<br>Light-Sleep: 9 µA</td>
              <td style="padding: 1.2vh 1vw; font-weight: 600;">高効率オンチップ DC-DC</td>
              <td style="padding: 1.2vh 1vw; color: rgba(255,255,255,0.8);">電池駆動スマートメーター、長距離センサー</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
              <td style="padding: 1.2vh 1vw; font-weight: 700; font-family: var(--mono); color: #4ade80;">ESP32-H4</td>
              <td style="padding: 1.2vh 1vw;">96MHz デュアル RISC-V<br>384KB SRAM + 2MB PSRAM</td>
              <td style="padding: 1.2vh 1vw;">-24 ~ +6 dBm<br>(最大 6 dBm @ 12.2mA)</td>
              <td style="padding: 1.2vh 1vw; font-weight: 600; color: #4ade80;">約 8.8 mA (BLE)<br>約 8.9 mA (15.4)</td>
              <td style="padding: 1.2vh 1vw;">Deep-Sleep: 5 µA<br>Light-Sleep: 12 µA</td>
              <td style="padding: 1.2vh 1vw; font-weight: 600;">高効率オンチップ DC-DC</td>
              <td style="padding: 1.2vh 1vw; color: rgba(255,255,255,0.8);">ウェアラブル、リモコン、LE Audio 音声機器</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>
```

---

### Archetype 4: 框架 + 官方硬件套件展示页 (Framework & DevKit Slide)
展示高阶算法框架与官方硬件板（200px~240px 大图特写），彻底消除多余空隙。

```html
<section class="slide dark">
  <div class="brand-logo"><img src="assets/logo-espressif-white.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--ink); color: var(--paper);">
    <div class="chrome-min">
      <div class="l">FRAMEWORKS · MULTIMEDIA &amp; EDGE AI</div>
      <div class="r">05 / 08</div>
    </div>
    <div class="frame col" style="padding-top: 1vh; flex: 1; display: flex; flex-direction: column;">
      <div>
        <h2 class="h-xl-zh" style="font-size: min(3.6vw, 5.8vh); line-height: 1.15; white-space: nowrap;">
          次世代マルチメディア &amp; Edge AI 開発フレームワーク
        </h2>
        <p class="body-sm" style="margin-top: 0.3vh; color: rgba(255,255,255,0.7); font-size: max(13.5px, 0.9vw);">
          ESP-GMF（音声・音響処理）と ESP-VISION（軽量エッジビジョン）
        </p>
      </div>

      <div class="grid-2-6-6" style="margin-top: 1.2vh; gap: 1.8vw; align-items: start;">
        <!-- GMF 卡片 -->
        <div class="col" style="border: 1px solid rgba(255,255,255,0.18); padding: 1.8vh 1.5vw; border-radius: 10px; display: flex; flex-direction: column; gap: 1vh; background: rgba(255,255,255,0.02);">
          <div>
            <span class="tag accent" style="font-size: max(11px, 0.72vw);">AUDIO FRAMEWORK</span>
            <h3 class="h-md" style="font-size: max(18px, 1.25vw); margin-top: 0.4vh;">ESP-GMF (General Multimedia Framework)</h3>
            <p style="font-size: max(13px, 0.85vw); color: rgba(255,255,255,0.75); margin-top: 0.2vh;">
              超軽量パイプライン型マルチメディアフレームワーク（最小 RAM 約 7 KB）
            </p>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.6vh; font-size: max(13.5px, 0.9vw); line-height: 1.5; color: rgba(255,255,255,0.9);">
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">実現できること:</span>
              <ul style="padding-left: 1.2em; margin-top: 0.2vh;">
                <li><strong>高音質化アルゴリズム:</strong> ALC (自動レベル制御)、DRC (ダイナミックレンジ圧縮)、EQ</li>
                <li><strong>双方向通話・音声対話:</strong> AEC (音響エコーキャンセラ)、3D 音響効果</li>
              </ul>
            </div>
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">適したプロジェクト:</span>
              スマートスピーカー、遠隔会議マイク、IP インターホン
            </div>
          </div>

          <!-- 开发板展示框 (230px 大图特写) -->
          <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.16); border-radius: 8px; padding: 1.2vh 1.2vw; display: flex; align-items: center; justify-content: center; gap: 1.5vw; margin-top: 0.6vh; min-height: 180px;">
            <img src="images/esp32-s31-korvo-1.png" style="height: 230px; width: auto; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));" alt="ESP32-S31-Korvo-1">
            <div>
              <div class="t-meta" style="color: rgba(255,255,255,0.6); font-size: max(11px, 0.74vw);">公式評価ボード</div>
              <div style="font-family: var(--mono); font-size: max(15px, 1.05vw); font-weight: 700; color: #fff;">ESP32-S31-Korvo-1</div>
              <div style="font-size: max(12.5px, 0.82vw); color: rgba(255,255,255,0.85); line-height: 1.35; margin-top: 2px;">
                デュアルマイク + Codec 搭載<br>S31-WROOM-3 (PSRAM 16MB)
              </div>
            </div>
          </div>
        </div>

        <!-- VISION 卡片 (结构相同，高度严谨对齐) -->
        <div class="col" style="border: 1px solid rgba(255,255,255,0.18); padding: 1.8vh 1.5vw; border-radius: 10px; display: flex; flex-direction: column; gap: 1vh; background: rgba(255,255,255,0.02);">
          <div>
            <span class="tag accent" style="font-size: max(11px, 0.72vw);">VISION &amp; EDGE AI</span>
            <h3 class="h-md" style="font-size: max(18px, 1.25vw); margin-top: 0.4vh;">ESP-VISION Framework</h3>
            <p style="font-size: max(13px, 0.85vw); color: rgba(255,255,255,0.75); margin-top: 0.2vh;">
              MicroPython / Web IDE による低コードかつ迅速なビジョン AI 開発基盤
            </p>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.6vh; font-size: max(13.5px, 0.9vw); line-height: 1.5; color: rgba(255,255,255,0.9);">
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">実現できること:</span>
              <ul style="padding-left: 1.2em; margin-top: 0.2vh;">
                <li><strong>映像パイプライン:</strong> MIPI-CSI 入力、カラー追従、バーコード/QR 認識、H.264 配信</li>
                <li><strong>エッジ AI 推論 (ESP-DL):</strong> YOLO 物体検出、顔認識、骨格検出、クラウド VLM 連携</li>
              </ul>
            </div>
            <div>
              <span style="color: var(--accent-bright); font-weight: 600;">適したプロジェクト:</span>
              スマートカメラ、小型産業用ビジョンセンサー、入退室ゲート
            </div>
          </div>

          <!-- 开发板展示框 (230px 大图特写) -->
          <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.16); border-radius: 8px; padding: 1.2vh 1.2vw; display: flex; align-items: center; justify-content: center; gap: 1.5vw; margin-top: 0.6vh; min-height: 180px;">
            <img src="images/esp32_p4_eye_front.png" style="height: 230px; width: auto; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.6));" alt="ESP32-P4-EYE">
            <div>
              <div class="t-meta" style="color: rgba(255,255,255,0.6); font-size: max(11px, 0.74vw);">公式評価ボード</div>
              <div style="font-family: var(--mono); font-size: max(15px, 1.05vw); font-weight: 700; color: #fff;">ESP32-P4X-EYE</div>
              <div style="font-size: max(12.5px, 0.82vw); color: rgba(255,255,255,0.85); line-height: 1.35; margin-top: 2px;">
                400MHz デュアル RISC-V<br>Flash 16MB · PSRAM 32MB · MIPI
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### Archetype 5: AI 开发者服务与 MCP 矩阵 (AI Ecosystem Slide)
浅色底、三列网格展示官方 MCP 生态体系，条理清晰、层次分明。

```html
<section class="slide light">
  <div class="brand-logo"><img src="assets/logo-espressif-red-black.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--paper); color: var(--ink);">
    <div class="chrome-min">
      <div class="l">AI DEVELOPER SERVICES · OFFICIAL MCP ECOSYSTEM</div>
      <div class="r">06 / 08</div>
    </div>
    <div class="frame col" style="padding-top: 1.6vh; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <h2 class="h-xl-zh" style="font-size: min(3.6vw, 6vh); line-height: 1.2; white-space: nowrap;">
          公式 AI 開発者サービスと MCP エコシステム
        </h2>
        <p class="body-sm" style="margin-top: 0.6vh; color: var(--text-secondary); font-size: max(14px, 0.95vw);">
          Claude Code、Windsurf、Cursor、VS Code などの最新 AI 開発環境と Espressif 開発リソースを直結
        </p>
      </div>

      <div class="frame grid-12" style="gap: 1.5vw; flex: 1; align-items: stretch; margin-top: 1.5vh;">
        <!-- Column 1: Docs MCP -->
        <div class="span-4 col" style="border: 1px solid var(--border-subtle); padding: 2vh 1.5vw; border-radius: 8px; background: var(--grey-1); justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="tag" style="background: #e0e0e0; color: #333; font-size: max(11px, 0.72vw);">DOCUMENTATION</span>
              <span class="t-meta" style="color: var(--text-helper); font-size: max(11px, 0.72vw);">Web / RAG</span>
            </div>
            <h3 class="h-md" style="font-size: max(18px, 1.2vw); margin-top: 1vh; line-height: 1.3;">chat.espressif.com &amp;<br>Docs MCP</h3>
            <p class="body-sm" style="font-size: max(13px, 0.86vw); color: var(--text-secondary); margin-top: 0.8vh; line-height: 1.5;">
              公式データシート、TRM、プログラミングガイド全量をインデックス化した専用 AI チャットボット。
            </p>
          </div>
          <div style="background: #fff; border: 1px solid var(--border-subtle); border-radius: 6px; padding: 1.2vh 1vw; font-size: max(12.5px, 0.82vw); line-height: 1.45; color: var(--text-secondary);">
            <strong style="color: var(--ink);">利用シーン:</strong> 「ESP32-S31 のクラシック Bluetooth 対応状況は？」などの技術仕様を即座に回答。
          </div>
        </div>

        <!-- Column 2: Cloud MCP Services -->
        <div class="span-4 col" style="border: 1px solid var(--border-subtle); padding: 2vh 1.5vw; border-radius: 8px; background: var(--grey-1); justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="tag accent" style="font-size: max(11px, 0.72vw);">CLOUD MCP</span>
              <span class="t-meta" style="color: var(--accent); font-weight: 600; font-size: max(11px, 0.72vw);">mcp.espressif.com</span>
            </div>
            <h3 class="h-md" style="font-size: max(18px, 1.2vw); margin-top: 1vh; line-height: 1.3;">リモート MCP サービス群</h3>
            <p class="body-sm" style="font-size: max(13px, 0.86vw); color: var(--text-secondary); margin-top: 0.8vh; line-height: 1.5;">
              IDE から直接呼び出せる樂鑫公式のクラウド MCP サーバー群。
            </p>
          </div>
          <div style="background: #fff; border: 1px solid var(--border-subtle); border-radius: 6px; padding: 1.2vh 1vw; font-size: max(12.5px, 0.82vw); line-height: 1.45; color: var(--text-secondary);">
            <strong style="color: var(--ink);">主なサービス:</strong>
            <ul style="padding-left: 1.2em; margin-top: 0.4vh;">
              <li><strong>Component Registry:</strong> 公式コンポーネントの検索と依存関係自動解決</li>
              <li><strong>Engineering MCP:</strong> ハードウェア設計レビュー・選型支援</li>
            </ul>
          </div>
        </div>

        <!-- Column 3: Local stdio MCP -->
        <div class="span-4 col" style="border: 1px solid var(--border-subtle); padding: 2vh 1.5vw; border-radius: 8px; background: var(--grey-1); justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="tag" style="background: var(--ink); color: #fff; font-size: max(11px, 0.72vw);">LOCAL TOOLCHAIN</span>
              <span class="t-meta" style="color: var(--text-helper); font-size: max(11px, 0.72vw);">ESP-IDF 6.0+</span>
            </div>
            <h3 class="h-md" style="font-size: max(18px, 1.2vw); margin-top: 1vh; line-height: 1.3;">idf.py mcp-server</h3>
            <p class="body-sm" style="font-size: max(13px, 0.86vw); color: var(--text-secondary); margin-top: 0.8vh; line-height: 1.5;">
              ESP-IDF 公式ツールチェーンに統合されたローカル stdio MCP サーバー。
            </p>
          </div>
          <div style="background: #fff; border: 1px solid var(--border-subtle); border-radius: 6px; padding: 1.2vh 1vw; font-size: max(12.5px, 0.82vw); line-height: 1.45; color: var(--text-secondary);">
            <strong style="color: var(--ink);">自律開発支援:</strong> AI エージェントが接続デバイスを認識し、<code>build</code> や <code>flash</code> を直接実行。ビルドエラーの自己修復を実現。
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### Archetype 6: 极简致谢封底 (Ending Slide)
醒目、大气的红底闭幕页，带 ASCII 点阵呼吸场。

```html
<section class="slide accent" data-animate="hero">
  <div class="brand-logo"><img src="assets/logo-espressif-white.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--accent); color: var(--accent-on);">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min">
      <div class="l"><span style="color: rgba(255,255,255,0.78);">LIGHTNING TALK · SUMMARY</span></div>
      <div class="r"><span style="color: rgba(255,255,255,0.78);">08 / 08</span></div>
    </div>
    <div class="frame col" style="justify-content: center; align-items: center; text-align: center; height: 100%;">
      <h1 class="h-hero-zh" style="color: #fff; font-size: min(7vw, 12vh); line-height: 1.2; letter-spacing: -0.02em; white-space: nowrap;">
        ご清聴<br>ありがとうございました
      </h1>
      <p class="body" style="margin-top: 3vh; color: rgba(255,255,255,0.88); font-size: max(16px, 1.15vw); letter-spacing: 0.05em;">
        SoC ハードウェア · ESP-IDF · エッジ AI · 公式 MCP エコシステム
      </p>
    </div>
  </div>
</section>
```

---

### Archetype 7: 协议协同与高对比度流程图页 (Coordination Architecture & Native Pipeline)
适合展示双层协议协同机制（如 Matter 远端管理 + Aliro 门前即时认证）以及 5 步鉴权处理流水线。采用 Native HTML/CSS 流程卡片，高对比度、清晰度 100% 受控、字号绝对不糊不挤。

```html
<section class="slide dark">
  <div class="brand-logo"><img src="assets/logo-espressif-white.svg" alt="Espressif"></div>
  <div class="canvas-card" style="background: var(--ink); color: var(--paper);">
    <div class="chrome-min">
      <div class="l">STANDARDS ARCHITECTURE · MATTER &amp; ALIRO</div>
      <div class="r">02 / 07</div>
    </div>
    <div class="frame col" style="padding-top: 0.5vh; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <h2 class="h-xl-zh" style="font-size: min(3.0vw, 5.0vh); line-height: 1.15; white-space: nowrap;">
          ESP-Matter と ESP-Aliro の役割と協調関係
        </h2>
        <p class="body-sm" style="margin-top: 0.3vh; color: rgba(255,255,255,0.72); font-size: max(13px, 0.88vw);">
          「広域管理・クラウド同期の Matter」と「ドア前近接・即時デジタル鍵認証の Aliro」が 1 チップ上で協調動作
        </p>
      </div>

      <div class="grid-2-6-6" style="margin-top: 1.2vh; gap: 1.8vw; align-items: stretch; flex: 1; min-height: 0;">
        <!-- 左栏: 双协议特性卡片 -->
        <div class="col" style="display: flex; flex-direction: column; gap: 1.4vh; justify-content: stretch;">
          <div style="border: 1px solid rgba(56,189,248,0.3); padding: 1.8vh 1.5vw; border-radius: 10px; background: linear-gradient(135deg, rgba(56,189,248,0.06) 0%, rgba(16,28,48,0.4) 100%); flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="tag blue">REMOTE &amp; ECOSYSTEM PLANE</span>
                <span class="t-meta" style="color: #38bdf8;">Wi-Fi 6 / Thread</span>
              </div>
              <h3 class="h-md" style="font-size: max(18px, 1.25vw); margin-top: 0.6vh; color: #fff;">ESP-Matter（広域管理・状態同期）</h3>
            </div>
            <ul style="padding-left: 1.2em; font-size: max(13.8px, 0.9vw); line-height: 1.65; color: rgba(255,255,255,0.9); display: flex; flex-direction: column; gap: 0.6vh; margin-top: 1vh;">
              <li><strong>最新仕様:</strong> <strong>Matter 1.6 (2026 年 6 月策定)</strong> にネイティブ対応</li>
              <li><strong>エコシステム統合:</strong> Apple Home、Google Home と直接連携</li>
              <li><strong>広域遠隔操作:</strong> 外出先からの施解錠、施錠状態監視、セキュア OTA</li>
              <li><strong>ユーザー権限管理:</strong> PIN コードやアクセススケジュールの配信・同期</li>
            </ul>
            <div style="margin-top: 1vh; border: 1px solid rgba(56,189,248,0.25); background: rgba(56,189,248,0.08); border-radius: 6px; padding: 0.8vh 1vw; font-size: max(12px, 0.78vw); color: rgba(255,255,255,0.85);">
              外出先スマホやスマートスピーカーから暗号化通信で合鍵・権限ルールを一括管理
            </div>
          </div>
        </div>

        <!-- 右栏: 原生 Native HTML/CSS 流程管道 -->
        <div class="arch-container" style="display: flex; flex-direction: column; justify-content: space-between; gap: 0.8vh; border: 1px solid rgba(255,255,255,0.18); border-radius: 10px; padding: 1.5vh 1.4vw; background: rgba(255,255,255,0.02);">
          <div style="width: 100%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.12); padding-bottom: 0.6vh;">
            <span style="font-family: var(--mono); font-size: max(12.5px, 0.82vw); color: var(--accent-bright); font-weight: 700;">AUTHENTICATION PIPELINE</span>
            <span class="t-meta" style="color: rgba(255,255,255,0.7); font-size: max(12px, 0.78vw);">5 段階 認証・駆動フロー</span>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.6vh; flex: 1; justify-content: space-between; margin-top: 0.6vh;">
            <!-- Pipeline Step 1 -->
            <div style="display: flex; align-items: center; gap: 1vw; padding: 1.2vh 1.2vw; background: rgba(56,189,248,0.06); border: 1px solid rgba(56,189,248,0.3); border-radius: 6px;">
              <div style="background: rgba(56,189,248,0.25); color: #38bdf8; font-family: var(--mono); font-size: 13px; font-weight: 700; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">1</div>
              <div style="flex: 1;">
                <div style="font-size: max(14px, 0.92vw); font-weight: 700; color: #fff;">解錠要求の受信 (Input Capture)</div>
                <div style="font-size: max(12.5px, 0.82vw); color: rgba(255,255,255,0.85); margin-top: 2px;">テンキー暗証番号入力、またはスマホ Wallet / NFC タグかざし</div>
              </div>
            </div>

            <div style="text-align: center; color: #38bdf8; font-size: 13px; line-height: 1;">↓</div>

            <!-- Pipeline Step 2 -->
            <div style="display: flex; align-items: center; gap: 1vw; padding: 1.2vh 1.2vw; background: rgba(244,63,94,0.06); border: 1px solid rgba(244,63,94,0.3); border-radius: 6px;">
              <div style="background: rgba(244,63,94,0.25); color: #f43f5e; font-family: var(--mono); font-size: 13px; font-weight: 700; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">2</div>
              <div style="flex: 1;">
                <div style="font-size: max(14px, 0.92vw); font-weight: 700; color: #fff;">クレデンシャル照合（NVS 暗号鍵検証）</div>
                <div style="font-size: max(12.5px, 0.82vw); color: rgba(255,255,255,0.85); margin-top: 2px;">内蔵フラッシュの暗号鍵テーブルと即時照合。不一致時は一時凍結</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## 四、自包含单文件（Base64 Inlining）发布机制

### 1. 为什么必须产出自包含版本
当网页制作完成后，如果用户需要将其发送给客户、复制到上级目录（如直接放到客户文件夹 `M5Stack/`、`Kaga/` 下）、或通过 AirDrop / 邮件传输，普通的相对路径（`src="images/..."`）极易由于目录层级变动而产生 404 破图。

因此，**全案交付必须同时产出带有 `_standalone.html` 后缀的自包含版本**。

### 2. 内联脚本使用方式
在项目根目录下，直接执行 Skill 内置的内联脚本：

```bash
python3 ~/.gemini/config/skills/espressif-deck-generator/scripts/inline_assets.py [input.html] [output_standalone.html]
```
脚本会自动扫描所有 `<img>` 标签的本地图片引用，自动将其转为 `data:image/...;base64,...`，生成一个完全脱离图片文件夹也能 100% 正常显示所有图片的独立 HTML。

---

## 五、标准 1080p 高清 PDF 自动化导出套件

### 1. 为什么不能直接用浏览器打印 (Ctrl + P)
乐鑫风格幻灯片采用了横向 Flexbox 滑动容器（`#deck`）、动态 WebGL/Canvas 点阵呼吸场背景以及 entrance 动画。在浏览器普通打印模式下，经常会出现：
* 页面被横向切断、只打印出第 1 页或空白页；
* 动画元素因处于未触发状态而导致透明度为 0；
* 底部导航圆点、ESC 提示条等交互控件混入打印结果。

### 2. 自动化导出命令与工作流
Skill 随附了经过实战检验的高精度导出脚本 `export_pdf.py`。该脚本通过无头 Google Chrome 渲染，固定 1920×1080（2x Retina）分辨率，隐藏所有导航遮罩，逐页等待 Canvas 点阵稳定并强制可见，最后通过 ReportLab 无损合成为 16:9 标准 1080p PDF。

执行导出命令：
```bash
uv run --with playwright --with reportlab --with pillow python ~/.gemini/config/skills/espressif-deck-generator/scripts/export_pdf.py [input.html] [output.pdf]
```

导出的 PDF 满足：
- 每页精准为 `1920 × 1080 pt`；
- 页面无任何边缘毛刺或排版错位；
- 经过 `pdftoppm` 自动验证通过。

---

## 六、结构化演讲原稿与时间控制规约 (`speech_script_ja.md`)

讲者在登台或进行线上 Webinar 时，原稿必须具备极其严谨的节拍控制。每次交付演示文稿时，必须配套生成演讲脚本：

### 1. 语速换算基准
* **日语标准**：**300 ~ 340 字符/分钟**
  * 5 分钟 Lightning Talk：约 **1,450 ~ 1,600 字符**（7 核心页 + 1 结语页，每页约 180~220 字）。
  * 30 分钟 Webinar：约 **9,000 ~ 10,000 字符**。
* **中文标准**：**220 ~ 260 汉字/分钟**。
* **英语标准**：**130 ~ 150 词/分钟**。

### 2. 脚本结构标准规范
演讲脚本必须包含三大模块：
1. **概要信息栏**：登坛时间目标、总字符数（含换算公式）、对象幻灯片版本、登坛人信息。
2. **时间配分表 (Schedule Matrix)**：
   | スライド番号 | タイトル・テーマ | 所要時間目安 | 累積経過時間 |
   | :--- | :--- | :--- | :--- |
   | **P1** | 表紙（自己紹介 & 趣旨説明） | 20 秒 | 00:00 - 00:20 |
   | **P2** | 会社概要 & 製品ポートフォリオ | 35 秒 | 00:20 - 00:55 |
   | ... | ... | ... | ... |
3. **正文演讲台词**：
   * 每个段落必须带上分秒级时间标记：如 `#### [00:55 - 02:10] スライド 3：最新フラグシップ SoC`。
   * 台词以引用块 `>` 呈现，便于阅读与提词。
   * 必须明确标注翻页时机（如 `[スライド切り替え]` 或 `[NEXT SLIDE]`）。
   * 重点词汇加粗（如「**双核 320 MHz RISC-V**」、「**经典蓝牙 BR/EDR 回归**」），提示讲者重音强调。

---

## 七、逐页深度技术解析与 Q&A 应对指南 (`slides_explanation_zh.md`)

为了使讲者、本地 FAE 及销售团队在与客户交流或应对现场 Q&A 时有据可依，必须同时产出深度中文说明手册。

### 1. 必须覆盖的核心要素
针对每一页幻灯片，手册必须提供：
* **展示内容清单**：主标题、核心图表、模组型号。
* **设计意图与主旨**：该页在整体叙事中的承上启下作用。
* **核心事实与数据依据**：
  * 严谨引用官方 Datasheet / TRM 章节与测试表格（例如：引用 `Table 5-10: Deep-sleep Current 5 µA`）。
  * 澄清技术边界（例如：明确指出 H4 的 +6 dBm 限制是为了换取极致低电流，与 H2/H21 的 20 dBm 属于不同的产品定位）。
* **客户交流重点**：提炼客户最关心的收益（如生产烧录时间减少 90%、代码合规与可移植性等）。
* **潜在高频 Q&A 应对策略**：预判客户可能提出的技术疑问，并给出官方依据的明确回答。

---

## 八、全案交付与生成前自检清单 (The 12-Point Pre-flight Checklist)

每次在向用户交付成果前，必须逐项对照检查：
1. [ ] **半角空格排版核对**：中日文文本与数字、英文字母交界处是否全局统一插入了半角空格（如 `Matter 1.6`、`ESP32-C5`、`< 0.5 秒`、`2.4 / 5 GHz`）？
2. [ ] **图解优先核对**：复杂协议协同、状态机流转是否强制采用了高对比 Native HTML/CSS 流程卡片或清晰 Mermaid？是否杜绝了通篇纯文字堆砌？
3. [ ] **图片大小与格式对称**：模组图片高度是否在 `140px~180px` 之间？开发板特写是否在 `190px~240px` 之间？双方对比格式是否对称一致（芯片对芯片、板子对板子）？
4. [ ] **画布通透性（无外框）**：页面最外层是否彻底去除了生硬厚重的外边框？是否保持了开放大气的暗黑空间感？
5. [ ] **展示框留白核对**：硬件展示框是否彻底去除了 `flex: 1`？上下留白是否紧凑收紧（上边距 0.6vh~1vh）？
6. [ ] **字号阶梯核对**：是否有任何文本低于 `max(12.5px, 0.82vw)`？规格参数、尺寸、容量等是否清晰可见？
7. [ ] **Humanizer 语气与用词核对**：是否清除了中式生硬直译（如「下発」$\to$「配信/送信」，「配網」$\to$「コミッショニング」）？是否彻底去除了「完全〜」等 AI 虚夸词？
8. [ ] **硬件时效与生态定位**：新芯片（如 C5）已出官方板时是否直接呈现官方板（杜绝用 C6 占位借代）？是否准确区分了原厂 DevKit 与 M5Stack 等客户快速体验生态套件？
9. [ ] **双模视效与快捷键**：封面/封底是否配备了流光背景？是否支持按 `B` 键随时在动态/静止模式间切换？
10. [ ] **自包含单文件发布版**：是否通过 `inline_assets.py` 生成了 `*_standalone.html` 并验证脱离文件夹后图片 100% 可见？
11. [ ] **1080p PDF 导出**：是否通过 `export_pdf.py` 自动化导出了 1920×1080 的纯净演示文档？
12. [ ] **演讲稿与技术手册配套**：是否配备了按 300~340 字/分严密控时的演讲稿（`speech_script_ja.md`）以及具备 Datasheet 硬核事实核验的白皮书（`slides_explanation_zh.md`）？
