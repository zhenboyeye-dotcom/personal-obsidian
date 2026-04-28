# Dataview 快速查询手册

> 基于 Obsidian Dataview 插件，支持在任意笔记中嵌入数据库式查询。

---

## 1. 所有芯片笔记（按时间排序）

````dataview
TABLE file.ctime as 创建时间, title, tags
FROM "02_Silicon"
WHERE type = "datasheet"
SORT file.ctime DESC
````

---

## 2. 按芯片系列分类

````dataview
TABLE title as 芯片, file.ctime as 日期
FROM "02_Silicon"
WHERE type = "datasheet"
GROUP BY tags[1]
SORT rows.file.ctime DESC
````

---

## 3. 按外设类型查询

````dataview
TABLE title as 芯片, tags[2] as 外设类型
FROM "02_Silicon"
WHERE type = "datasheet" AND contains(tags, "uart")
SORT title ASC
````

> 查找所有含 UART 外设的芯片笔记。把 `uart` 换成 `spi` / `i2c` / `adc` / `can` 可查其他外设。

---

## 4. Bug 追踪（按严重度排序）

````dataview
TABLE severity as 级别, title as 问题描述, platform as 平台, status as 状态
FROM "05_Bug_Tracking"
WHERE severity
SORT 
  CASE 
    WHEN severity = "P0" THEN 1
    WHEN severity = "P1" THEN 2
    WHEN severity = "P2" THEN 3
    ELSE 4
  END ASC
````

---

## 5. 未解决的 Bug

````dataview
TABLE severity as 级别, title as 问题描述, platform as 平台, 发现时间
FROM "05_Bug_Tracking"
WHERE status = "open"
SORT file.ctime DESC
````

---

## 6. 代码片段库（按语言分类）

````dataview
TABLE file.ctime as 日期, file.name as 文件
FROM "03_Snippets"
WHERE file.extension = "md"
SORT file.folder ASC
````

---

## 7. 使用说明

1. 在 Obsidian 中新建任意笔记
2. 切换为 **实时预览模式**（Live Preview）
3. 粘贴上方任意查询代码块
4. Dataview 会自动渲染结果

> **提示**：查询结果为只读，不可编辑。如需修改，定位到对应笔记直接编辑。
