# Obsidian 插件配置指南

> 配置日期：2026-04-28

## 已完成预置

以下配置已写入 `.obsidian/` 目录，但你仍需在 Obsidian 内完成插件启用：

### 1. Templater（模板引擎）

**设置路径**：Obsidian 设置 →  Templater

| 配置项 | 值 |
|--------|-----|
| Template folder | `04_Workflows` |
| Trigger | `Ctrl+e` |

**验证**：按 `Ctrl+e` 应弹出模板选择器。

### 2. Obsidian Git

**设置路径**：Obsidian 设置 →  Obsidian Git

| 配置项 | 值 |
|--------|-----|
| Auto backup interval | 30 分钟 |
| Commit message | `vault backup: {{date}}` |
| Auto push | ❌ 建议先手动推送 |

**首次配置 Git 远程**（在 Obsidian 终端或 PowerShell）：

```bash
cd D:\obsidianfile
git remote add origin <你的GitHub仓库URL>
git branch -M main
git push -u origin main
```

### 3. Dataview

无需特别配置，直接在任意笔记使用查询语法：

````markdown
```dataview
TABLE file.ctime as 创建时间, tags
FROM "02_Silicon"
WHERE type = "datasheet"
SORT file.ctime DESC
```
````

### 4. Calendar

安装后左侧栏会出现日历图标，点击日期可查看当天笔记。

---

## 快速上手流程

```
1. 打开 D:\obsidianfile 仓库
2. 设置 → 社区插件 → 开启
3. 设置 → Templater → 确认模板目录为 04_Workflows
4. 设置 → Obsidian Git → 配置仓库
5. Ctrl+e → 选择模板 → 新建笔记
```
