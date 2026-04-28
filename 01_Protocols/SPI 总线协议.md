---
uid: PROTO-SPI
type: protocol
title: "SPI 总线协议"
category: serial
tags: [spi, 串行外设接口, 全双工, 高速]
version: "1.0"
date: 2026-04-28
related_chips:
  - DS-20260428-STM32F103Cx-MCU
  - DS-20260428-ESP32-S3-WROOM-1
---

# SPI 总线协议

## 一句话总结

> 串行外设接口，4线制（SCK/MOSI/MISO/SS）同步全双工通信，无地址概念，靠片选线选从机，速率可达数十 MHz，适合 Flash、显示屏、传感器等高速场景。

---

## 电气特性

| 项目 | 参数 |
|------|------|
| 信号线 | SCK（时钟）、MOSI（主出从入）、MISO（从出主入）、SS（片选）|
| 拓扑 | 1 主 n 从，片选线管理 |
| 传输距离 | 通常 < 30cm（板内通信）|
| 速率 | 100 kHz ~ 数十 MHz（依硬件）|
| 方向 | 全双工 |

---

## 四种模式（CPOL + CPHA）

| 模式 | CPOL | CPHA | SCK 空闲 | 采样沿 |
|------|------|------|-----------|--------|
| 0 | 0 | 0 | 低电平 | 第一个边沿（上升沿）|
| 1 | 0 | 1 | 低电平 | 第二个边沿（下降沿）|
| 2 | 1 | 0 | 高电平 | 第一个边沿（下降沿）|
| 3 | 1 | 1 | 高电平 | 第二个边沿（上升沿）|

```
Mode 0 (CPOL=0, CPHA=0):    Mode 3 (CPOL=1, CPHA=1):
    SCK ─┐  ┌──  SCK ─┐  ┌──
         └──┘         └──┘
    MOSI ──────────────────
    MISO ──────────────────
         ↑ 采样            ↓ 采样
```

> ⚠️ **两个参数必须匹配**：主从设备 SPI 模式必须完全一致，常见错误是主机设了 Mode 0 但从机是 Mode 1。

---

## 数据位序与宽度

| 参数 | 常见值 |
|------|--------|
| 位宽 | 8 bit / 16 bit |
| 位序 | MSB First（默认）/ LSB First |
| 时钟分频 | 2/4/8/16/32/64/128/256 |

---

## STM32 SPI 配置示例

### SPI1 引脚（PA5=SCK, PA6=MISO, PA7=MOSI）

```c
// 使能时钟
RCC->APB2ENR |= RCC_APB2ENR_SPI1EN;
RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;

// PA5=复用推挽, PA6/PA7=复用推挽
GPIOA->CRL = (GPIO_CRL_MODE5 | GPIO_CRL_CNF5_1);  // SCK AF PP
GPIOA->CRL &= ~(GPIO_CRL_CNF5_0);
GPIOA->CRL = (GPIO_CRL_MODE6 | GPIO_CRL_CNF6_1);  // MISO AF PP
GPIOA->CRL &= ~(GPIO_CRL_CNF6_0);
GPIOA->CRL = (GPIO_CRL_MODE7 | GPIO_CRL_CNF7_1);  // MOSI AF PP
GPIOA->CRL &= ~(GPIO_CRL_CNF7_0);
```

### SPI1 初始化（Mode 3, 8MHz）

```c
SPI1->CR1 = 0;
SPI1->CR1 |= SPI_CR1_MSTR;  // 主模式
SPI1->CR1 |= SPI_CR1_SPE;   // 使能

// 或者更完整配置：
SPI1->CR1 = SPI_CR1_MSTR   // 主模式
          | SPI_CR1_BR_1;   // f_PCLK/8 = 9MHz
SPI1->CR1 |= SPI_CR1_CPHA;  // 第二个边沿采样 (Mode 3)
SPI1->CR1 |= SPI_CR1_CPOL;  // SCK 高空闲
SPI1->CR2 |= SPI_CR2_SSOE;  // SS 输出使能
SPI1->CR1 |= SPI_CR1_SPE;   // 使能
```

### 发送/接收

```c
// 发送一个字节
uint8_t spi1_tx(uint8_t data) {
    SPI1->DR = data;
    while (!(SPI1->SR & SPI_SR_TXE));  // 等待发送完成
    while (SPI1->SR & SPI_SR_BSY);    // 等待总线空闲
    return SPI1->DR;
}

// 全双工收发
uint8_t spi1_transfer(uint8_t data) {
    SPI1->DR = data;
    while (!(SPI1->SR & SPI_SR_RXNE));
    return SPI1->DR;
}
```

---

## ESP32 SPI 配置示例

```c
#include "driver/spi_master.h"

spi_device_handle_t spi;
spi_bus_config_t buscfg = {
    .mosi_io_num = GPIO_NUM_23,
    .miso_io_num = GPIO_NUM_19,
    .sclk_io_num = GPIO_NUM_18,
    .quadwp_io_num = -1,
    .quadhd_io_num = -1,
};
spi_device_interface_config_t devcfg = {
    .clock_speed_hz = 10 * 1000 * 1000,  // 10 MHz
    .mode = 0,  // CPOL=0, CPHA=0
    .spics_io_num = GPIO_NUM_5,  // CS
    .queue_size = 1,
};
spi_bus_initialize(HSPI_HOST, &buscfg, 1, 0);
spi_bus_add_device(HSPI_HOST, &devcfg, &spi);

// 传输
spi_transaction_t t = {
    .length = 8,  // bits
    .tx_buffer = &tx_data,
    .rx_buffer = &rx_data,
};
spi_device_transmit(spi, &t);
```

---

## 常用外设模式参考

| 外设 | 模式 | 速率 | 备注 |
|------|------|------|------|
| W25Qxx Flash | Mode 0 / 3 | up to 133MHz | 通常 Mode 0 |
| SD Card | Mode 0 | up to 25MHz | SPI 模式 |
| ST7789 LCD | Mode 3 | up to 65MHz | 16-bit RGB |
| nRF24L01 | Mode 0 | 2MHz | 无线收发 |
| ADS1256 | Mode 1 | 7.68MHz | 24-bit ADC |
| ESP32 PSRAM | QSPI | 80MHz | 8-bit 并行 |

---

## 多从设备连接

```
        SS1 ──┐
              ├─── SS2 ──┐
                    └─── SS3
  MOSI ──────────────────────────────
  MISO ──────────────────────────────
  SCK  ──────────────────────────────
```

每个从设备需要独立的 SS 片选线，主机通过 GPIO 控制选择当前通信的从设备。

---

## 常见问题

| # | 问题 | 原因 | 解决 |
|---|------|------|------|
| 1 | 数据错乱 | 主从不匹配（模式/位序/速率）| 确认 CPOL/CPHA 和时钟分频 |
| 2 | MISO 一直高 | 从机未使能或 SS 未拉低 | 确认片选时序 |
| 3 | 只发不收 | 全双工需交替读写 | 同时写入 DR 触发 SCK |
| 4 | 高速通信失败 | 线太长/信号完整性 | 减小速率，加驱动或用并行 |
| 5 | 多从机冲突 | 两从机同时拉 MISO | 从机 MISO 需三态，需上拉 |

---

## 隐藏坑点

1. ⚠️ **Mode 0 还是 Mode 3 傻傻分不清** — 购买模组前确认模式，写代码时对着手册设
2. ⚠️ **SS 片选时序** — 有些从机要求在 SCK 第一个边沿前 SS 就已拉低，且保持整个帧
3. ⚠️ **发送后必须读 DR** — 未读取的数据会覆盖下一帧，尤其在多字节传输时
4. ⚠️ **BSY 标志需等待** — 判断传输完成的可靠方式是检查 BSY，不是 TXE
5. ⚠️ **从机 SPI 时钟源** — STM32 作为从机时，需要外部提供 SCK，不能自己生时钟
6. ⚠️ **MOSI/MISO 交叉连接** — 主机 MOSI 接从机 MOSI（不是 MISO）！

---

## 参考链接

- STM32 SPI: [[DS-20260428-STM32F103Cx-MCU]]
- ESP32 SPI/PSRAM: [[DS-20260428-ESP32-S3-WROOM-1]]
