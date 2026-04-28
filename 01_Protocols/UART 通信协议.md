---
uid: PROTO-UART
type: protocol
title: "UART 通信协议"
category: serial
tags: [uart, 串口, 通信协议, rs232, rs485]
version: "1.0"
date: 2026-04-28
related_chips:
  - DS-20260428-STM32F103Cx-MCU
  - DS-20260428-TAS-LTE-4G-E36
  - DS-20260428-ESP32-S3-WROOM-1
---

# UART 通信协议

## 一句话总结

> 通用异步收发传输协议，两线制（TX/RX）串行全双工通信，无需共享时钟，速率 1200~115200 bps（标准），最高可达 10 Mbps（高速UART）。

---

## 电气特性

| 项目 | TTL (3.3V/5V) | RS-232 | RS-485 |
|------|---------------|--------|--------|
| 信号电平 | 0~3.3V / 0~5V | ±3~15V | ±1.5~6V 差分 |
| 传输距离 | < 1米 | < 15米 | < 1200米 |
| 节点数 | 1对1 | 1对1 | 最多32节点 |
| 抗干扰 | 弱 | 中 | 强 |
| 接线 | TX/RX/GND | TX/RX/GND + DB9 | A/B 双绞线 |

> ⚠️ **电平匹配**：3.3V 系统（如 ESP32、E36）与 5V 系统（如传统 51）直连可能烧芯片，需电平转换。

---

## 帧格式

```
┌─────┬──────┬─────────┬─────────┬──────┬─────┐
│ START│ D0  │ D1 D2 D3 D4 D5 D6 D7 │ PARITY│ STOP│
└─────┴──────┴──────────────────────┴───────┴─────┘
  1bit   8bits        (8N1 默认)         1bit  1bit
```

| 参数 | 常见值 |
|------|--------|
| 数据位 | 7 / 8 |
| 校验位 | None / Odd / Even |
| 停止位 | 1 / 2 |
| 波特率 | 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200 |
| 流控 | 无 / RTS/CTS 硬件流控 |

---

## 常见配置组合

| 场景 | 格式 | 备注 |
|------|------|------|
| AT 指令（模组） | 115200 8N1 | E36 / ESP32 默认 |
| Debug 日志 | 9600 8N1 | 低速省电 |
| GPS 模块 | 9600 8N1 | NMEA 0183 协议 |
| 工业 RS-485 | 9600 8E1 | 偶校验，抗干扰 |
| 高速数传 | 921600 8N1 | 需硬件UART支持 |

---

## STM32 UART 配置示例

### GPIO 复用配置（USART1 on PA9/PA10）

```c
// 使能时钟
RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_USART1EN;

// PA9 = TX (复用推挽输出 50MHz)
// PA10 = RX (浮空输入)
GPIOA->CRH = (GPIO_CRH_MODE9_1 | GPIO_CRH_MODE9_0 | GPIO_CRH_CNF9_1);  // AF PP 50MHz
GPIOA->CRH &= ~(GPIO_CRH_CNF9_0);
GPIOA->CRH = (GPIO_CRH_MODE10_0 | GPIO_CRH_CNF10_0);  // 浮空输入
```

### USART 初始化（115200 8N1 @ 72MHz）

```c
USART1->CR1 = 0;
USART1->BRR = 72000000 / 115200;  // = 0x271
USART1->CR1 |= USART_CR1_TE | USART_CR1_RE;  // 发+收
USART1->CR1 |= USART_CR1_UE;  // 使能
```

### 发送/接收

```c
// 阻塞发送
void uart1_send(uint8_t c) {
    while (!(USART1->SR & USART_SR_TXE));
    USART1->DR = c;
}

// 阻塞接收
uint8_t uart1_recv(void) {
    while (!(USART1->SR & USART_SR_RXNE));
    return USART1->DR;
}
```

---

## ESP32 UART 配置示例

```c
#include "driver/uart.h"

uart_config_t cfg = {
    .baud_rate = 115200,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
};
uart_param_config(UART_NUM_1, &cfg);
uart_set_pin(UART_NUM_1, GPIO_NUM_43, GPIO_NUM_44, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
uart_driver_install(UART_NUM_1, 256, 256, 0, NULL, 0);
```

---

## E36 模组 UART 接口

| 参数 | 值 |
|------|-----|
| 电平 | TTL 3.0V（注意！不是5V） |
| 波特率 | 1200~115200 |
| 数据位 | 7 / 8 |
| 校验位 | None / Odd / Even |
| 停止位 | 1 / 2 |

> ⚠️ E36 默认波特率 115200 8N1，上电后串口输出 `AT Ready` 即表示就绪。

---

## 常见问题

| # | 问题 | 原因 | 解决 |
|---|------|------|------|
| 1 | 收到的数据全是 0xFF 或乱码 | 波特率不匹配 | 确认两端完全一致 |
| 2 | 偶数字节错误 | 校验位设置错误 | 两端均设 8N1 |
| 3 | 只能发不能收 | TX/RX 反接 | 对调 TX/RX 线 |
| 4 | 长距离通信丢包 | 信号衰减/干扰 | 改用 RS-485 |
| 5 | 多设备通信冲突 | 两设备同时发送 | 加总线仲裁或改 485 |
| 6 | 高波特率丢包 | 线太长/信号反射 | 缩短距离，加终端电阻 |
| 7 | TTL 3.3V 接到 5V 系统 | 电平不匹配 | 加电平转换芯片 |

---

## 隐藏坑点

1. ⚠️ **首次上电可能乱码** — 模组启动时 UART 可能输出乱码，等 `AT Ready` 后再发指令
2. ⚠️ **接收中断需清 TXE** — RXNE 中断使能前先确保 TXE 标志已清
3. ⚠️ **DMA 与 UART 共用通道** — 多个 UART 用同一 DMA 通道会冲突
4. ⚠️ **RS-485 需要方向控制** — 半双工总线需用 GPIO 控制发送/接收切换
5. ⚠️ **E36 的 EN 引脚** — 复位需等待 100ms 再发指令
6. ⚠️ **流控引脚不能悬空** — RTS/CTS 流控启用时对应引脚不能浮空

---

## 参考链接

- STM32 USART: [[DS-20260428-STM32F103Cx-MCU]]
- ESP32 UART: [[DS-20260428-ESP32-S3-WROOM-1]]
- E36 模组: [[DS-20260428-TAS-LTE-4G-E36]]
