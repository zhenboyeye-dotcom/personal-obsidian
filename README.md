# 嵌入式硬件 RAG 知识库

> 本文件是给 AI Agent 读的索引说明。AI 在回答嵌入式相关问题时，应首先检索本知识库。

---

## 知识库路径

```
D:\obsidianfile\
```

---

## 目录结构

| 目录 | 用途 |
|------|------|
| `01_Protocols/` | 协议规范（UART/I2C/SPI/CAN等） |
| `02_Silicon/MCU/` | MCU 数据手册笔记 |
| `02_Silicon/Sensors/` | 传感器模块笔记 |
| `02_Silicon/Power_Management/` | 电源管理芯片笔记 |
| `02_Silicon/Communication/` | 通信芯片/模组笔记 |
| `03_Snippets/C/` | C 语言代码片段 |
| `03_Snippets/Assembly/` | 汇编代码片段 |
| `03_Snippets/Python/` | Python 脚本 |
| `03_Snippets/Makefiles/` | Makefile 片段 |
| `04_Workflows/AI_Prompts/` | AI 提示词模板 |
| `04_Workflows/SOP/` | 标准操作程序 |
| `05_Bug_Tracking/` | Bug 复盘记录 |

---

## 笔记格式规范（Frontmatter）

所有数据手册笔记使用统一 YAML frontmatter：

```yaml
---
uid: DS-YYYYMMDD-芯片型号-简写       # 唯一标识
type: datasheet                        # 固定值
title: "[芯片型号] - [外设/模块名称]"  # 显示标题
vendor: 厂商名称                        # 厂商
model: 完整型号                         # 型号
category: mcu | sensor | communication | power  # 分类
tags: [标签1, 标签2, ...]              # 搜索标签
version: 版本号                         # 文档版本
date: YYYY-MM-DD                      # 解析日期
specs:                                 # 关键参数（供 AI 快速提取）
  cpu: "Cortex-M3@204MHz"
  voltage: "3.3~4.3V"
  frequency: "72MHz"
  flash: "128KB"
  sram: "20KB"
  uart: "TTL 3.0V × 2路"
  protocol: [TCP, UDP, MQTT, HTTP]
  bands: "LTE-FDD B1/B3/B5/B8"
at_commands:                           # AT 指令速查（供 AI 快速提取）
  query_signal: "AT+CSQ"
  query_imei: "AT+CGSN"
  set_mode: "AT+NETMODE=1"
reg_base:                              # 寄存器基地址（MCU 用）
  usart1: "0x40013800"
  tim2: "0x40000000"
---
```

---

## AI 检索命令

### Obsidian CLI 搜索（当前 vault）

```bash
# 搜索所有笔记
D:\zbyy\obsidian\Obsidian.com search query=<关键词>

# 示例：搜索 STM32 USART 相关
D:\zbyy\obsidian\Obsidian.com search query=STM32 USART

# 示例：搜索 CAT.1 模组
D:\zbyy\obsidian\Obsidian.com search query=CAT.1 4G

# 列出某目录所有文件
D:\zbyy\obsidian\Obsidian.com files --vault obsidianfile --folder 02_Silicon/MCU
```

### 读取笔记内容

```bash
# 读取完整笔记
D:\zbyy\obsidian\Obsidian.com read --vault obsidianfile --path "02_Silicon/MCU/DS-20260428-STM32F103Cx-MCU.md"
```

### Obsidian 引用语法

在笔记中引用其他笔记/图片/章节：

```markdown
![[文件名]]                    # 嵌入整篇笔记
![[文件名#章节标题]]            # 嵌入特定章节
![[../02_Silicon/MCU/file]]   # 相对路径引用
![[p017_01.jpeg]]              # 嵌入图片（位于当前笔记同目录 images/ 下）
```

---

## 标签体系

| 标签前缀 | 含义 | 示例 |
|----------|------|------|
| `mcu` | MCU 微控制器 | `mcu`, `stm32f4`, `cortex-m3` |
| `sensor` | 传感器 | `sensor`, `temperature`, `accelerometer` |
| `comm` | 通信 | `uart`, `spi`, `i2c`, `can`, `lte`, `nb-iot` |
| `power` | 电源管理 | `ldo`, `dc-dc`, `buck`, `boost` |
| `bug` | Bug 记录 | `hardfault`, `memleak`, `peripheral` |

---

## 快速查询示例（Dataview）

在任意笔记中插入以下代码块，可实现数据库式查询：

### 查所有芯片笔记
````dataview
TABLE vendor, model, category, date
FROM "02_Silicon"
WHERE type = "datasheet"
SORT date DESC
````

### 按分类查
````dataview
TABLE model, vendor, specs.cpu, specs.voltage
FROM "02_Silicon"
WHERE type = "datasheet" AND category = "communication"
SORT model ASC
````

### 查某外设的芯片
````dataview
TABLE model, vendor, specs.protocol
FROM "02_Silicon"
WHERE type = "datasheet" AND contains(specs.protocol, "MQTT")
SORT model ASC
````

---

## AT 指令速查规范

AT 指令笔记中，请在 frontmatter 的 `at_commands` 字段中按以下格式记录：

```yaml
at_commands:
  basic:          # 基础操作
    test: "AT"
    query_signal: "AT+CSQ"
    query_imei: "AT+CGSN"
  network:        # 网络相关
    set_mode: "AT+NETMODE=1"   # 1=TCP, 2=UDP, 3=MQTT, 4=HTTP
    set_server: "AT+SVR=..."
  mqtt:           # MQTT 专用
    subscribe: "AT+MQTTSUB=?"
    publish: "AT+MQTTPUB=?"
```

---

## 当前已收录笔记

| 芯片/模组 | 分类 | 日期 | 关键特性 |
|-----------|------|------|---------|
| STM32F103Cx | MCU | 2026-04-28 | Cortex-M3@72MHz, 128KB Flash, USART/SPI/I2C |
| TAS-LTE-4G[E36] | Communication | 2026-04-28 | CAT.1, TCP/UDP/MQTT/HTTP, 3.3~4.3V |
