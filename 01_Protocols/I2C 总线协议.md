---
uid: PROTO-I2C
type: protocol
title: "I2C 总线协议"
category: serial
tags: [i2c, iic, 串行总线, 双线, 传感器]
version: "1.0"
date: 2026-04-28
related_chips:
  - DS-20260428-STM32F103Cx-MCU
  - DS-20260428-ESP32-S3-WROOM-1
---

# I2C 总线协议

## 一句话总结

> 两线制同步串行总线（SCL + SDA），支持多主机多从设备，标准速率 100kHz，快速模式 400kHz，高速模式 3.4MHz，适合板内芯片/传感器之间的中短距离通信。

---

## 电气特性

| 项目 | 参数 |
|------|------|
| 信号线 | SCL（时钟）、SDA（数据）|
| 上拉电阻 | 4.7kΩ（5V）/ 2.2kΩ~10kΩ（3.3V）|
| 总线电容 | < 400pF（否则需总线缓冲器）|
| 传输距离 | 通常 < 1米（板内通信）|
| 拓扑 | 多主机多从设备，仲裁机制 |

---

## 速度等级

| 模式 | 速率 | 备注 |
|------|------|------|
| 标准 | 100 kbit/s | 最常用 |
| 快速 | 400 kbit/s | 多数传感器支持 |
| 快速+ | 1 Mbit/s | 需较好硬件 |
| 高速 | 3.4 Mbit/s | 需专用PHY |

---

## 帧格式

### START + 地址 + 读写 + ACK

```
  S   [7bit addr] [R/W] [A]  [8bit reg] [A]  [8bit data] [A]   P
────┬───────────────────────┬────┬────────────┬────┬───────────┬────
    │                       │    │            │    │           │
 SCL┴───────────────────────┴────┴────────────┴────┴───────────┴────
```

| 符号 | 含义 |
|------|------|
| S | START condition (SDA 拉低) |
| P | STOP condition (SCL 高时 SDA 升高) |
| A | ACK (从设备拉低 SDA) |
| N | NACK (从设备释放 SDA) |
| R/W | 0=写, 1=读 |

---

## 地址格式

```
  [7bit 设备地址]  [R/W]
  ────────────────  ───
  高位            低位
```

> ⚠️ I2C 地址是 7bit，不是 8bit！常见误区是把 8bit 写地址（包括读写位）当成 7bit 地址。

### 常见 I2C 地址换算

| 7bit 地址 | 写地址 (8bit) | 读地址 (8bit) |
|-----------|---------------|---------------|
| 0x27 | 0x4E | 0x4F |
| 0x3C | 0x78 | 0x79 |
| 0x68 | 0xD0 | 0xD1 |
| 0x76 | 0xEC | 0xED |

---

## STM32 I2C 配置示例

### I2C1 引脚（PB6=SCL, PB7=SDA）

```c
// 使能时钟
RCC->APB1ENR |= RCC_APB1ENR_I2C1EN;
RCC->APB2ENR |= RCC_APB2ENR_IOPBEN;

// PB6=复用开漏, PB7=复用开漏
GPIOA->CRL = (GPIO_CRL_MODE6 | GPIO_CRL_CNF6_1);  // 开漏输出
GPIOA->CRL &= ~(GPIO_CRL_CNF6_0);
GPIOA->CRL = (GPIO_CRL_MODE7 | GPIO_CRL_CNF7_1);
GPIOA->CRL &= ~(GPIO_CRL_CNF7_0);
```

### I2C 初始化（100kHz @ 36MHz APB1）

```c
I2C1->CR1 = I2C_CR1_SWRST;  // 复位
I2C1->CR1 = 0;

I2C1->CR2 = 36;  // APB1 = 36MHz
I2C1->CCR = 180;  // 100kHz = 36MHz / (2 * 180)
I2C1->TRISE = 37;  // 1000ns + 1 = 37

I2C1->CR1 |= I2C_CR1_PE;  // 使能
```

### I2C 读写时序

```c
// 发送 START
I2C1->CR1 |= I2C_CR1_START;
while (!(I2C1->SR1 & I2C_SR1_SB));

// 发送地址 (7bit + 写)
I2C1->DR = (addr << 1) | 0;
while (!(I2C1->SR1 & I2C_SR1_ADDR));

// 发送寄存器地址
I2C1->DR = reg;
while (!(I2C1->SR1 & I2C_SR1_TXE));

// 发送数据
I2C1->DR = data;
while (!(I2C1->SR1 & I2C_SR1_TXE) && !(I2C1->SR1 & I2C_SR1_BTF));

// 发送 STOP
I2C1->CR1 |= I2C_CR1_STOP;
```

---

## ESP32 I2C 配置示例

```c
#include "driver/i2c.h"

i2c_config_t cfg = {
    .mode = I2C_MODE_MASTER,
    .sda_io_num = GPIO_NUM_21,
    .scl_io_num = GPIO_NUM_22,
    .sda_pullup_en = GPIO_PULLUP_ENABLE,
    .scl_pullup_en = GPIO_PULLUP_ENABLE,
    .master.clk_speed = 400000,
};
i2c_param_config(I2C_NUM_0, &cfg);
i2c_driver_install(I2C_NUM_0, cfg.mode, 0, 0, 0);

// 写寄存器
i2c_cmd_handle_t cmd = i2c_cmd_link_create();
i2c_master_start(cmd);
i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
i2c_master_write_byte(cmd, reg, true);
i2c_master_write_byte(cmd, data, true);
i2c_master_stop(cmd);
i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_PERIOD_MS);
i2c_cmd_link_delete(cmd);
```

---

## 常见传感器地址参考

| 传感器 | 7bit 地址 |
|--------|-----------|
| MPU6050 (陀螺仪) | 0x68 / 0x69 |
| BMP280 (气压) | 0x76 / 0x77 |
| AHT10 (温湿度) | 0x38 |
| SSD1306 (OLED) | 0x3C / 0x3D |
| BH1750 (光强) | 0x23 / 0x5C |
| ADS1115 (ADC) | 0x48~0x4B |
| INA219 (电流) | 0x40~0x41 |

---

## 常见问题

| # | 问题 | 原因 | 解决 |
|---|------|------|------|
| 1 | 总线一直忙 | SDA 被从机拉低 | 发送 9 个 SCL 脉冲释放 |
| 2 | 无 ACK | 地址错误/从机不响应 | 确认 7bit 地址和上拉 |
| 3 | 读数据全 0xFF | 未发送 restart | 读操作需 restart 再发读地址 |
| 4 | 时钟拉伸 | 从机延展 SCL | 正常现象，增加超时检测 |
| 5 | 多设备通信冲突 | 两设备同时发 | I2C 仲裁机制自动处理 |
| 6 | 高速模式失败 | 总线电容太大 | 降低速率或加缓冲器 |

---

## 隐藏坑点

1. ⚠️ **地址左移 1 位** — 7bit 地址写入 DR 时需左移一位，再加 R/W 位
2. ⚠️ **SDA/SCL 上拉不能省** — I2C 开漏输出，无上拉总线无法工作
3. ⚠️ **重启后 I2C 可能死锁** — 从机异常拉低 SDA 导致，可软件复位 I2C 总线
4. ⚠️ **APB1 频率影响 I2C 时序** — STM32 的 APB1 最大 36MHz，需查表计算 CCR
5. ⚠️ **多字节读取需 restart** — 读多个字节时，末字节前需发送 NACK 再 STOP
6. ⚠️ **总线电容限制速率** — 每增加 10cm 线长可能需减小上拉电阻（但不能太小否则灌电流过大）

---

## 参考链接

- STM32 I2C: [[DS-20260428-STM32F103Cx-MCU]]
- ESP32 I2C: [[DS-20260428-ESP32-S3-WROOM-1]]
