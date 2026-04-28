# 嵌入式硬件 RAG 知识库

基于 Obsidian + Git 的本地优先知识管理系统，专为嵌入式硬件工程师设计。

## 目录结构

```
├── 01_Protocols/          # 协议规范（UART/I2C/SPI/CAN等）
├── 02_Silicon/             # 芯片与外设
│   ├── MCU/               # 微控制器数据手册与笔记
│   ├── Sensors/           # 传感器模块
│   ├── Power_Management/  # 电源管理芯片
│   └── Communication/     # 通信芯片
├── 03_Snippets/           # 代码片段库（C/汇编/Python/Makefile）
├── 04_Workflows/          # AI提示词与SOP
│   ├── AI_Prompts/        # 大模型提示词模板
│   ├── SOP/               # 标准操作程序
│   └── Hooks/             # Obsidian 钩子脚本
├── 05_Bug_Tracking/       # 疑难杂症复盘记录
│   ├── HardFaults/        # 硬故障分析
│   ├── Memory_Leaks/       # 内存泄漏记录
│   └── Peripheral_Errors/  # 外设异常记录
```

## 使用说明

### 模板使用
- **数据手册解析**：`Ctrl+P` → 输入 `Datasheet` → 选择模板
- **Bug 复盘报告**：`Ctrl+P` → 输入 `Bug` → 选择模板

### 目录说明
| 目录 | 用途 |
|------|------|
| `01_Protocols` | 存储协议规范笔记（UART/I2C/SPI/CAN等） |
| `02_Silicon` | 芯片选型参考、外设驱动笔记、数据手册摘要 |
| `03_Snippets` | 可复用的代码片段，按语言分类 |
| `04_Workflows` | AI 提示词模板、SOP 流程文档 |
| `05_Bug_Tracking` | 每次疑难 Bug 的复盘记录 |

### Git 同步
```bash
git init
git remote add origin <your-repo-url>
git add .
git commit -m "chore: init embedded RAG knowledge base"
git push -u origin main
```
