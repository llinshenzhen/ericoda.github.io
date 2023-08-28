---
title: BLE超低功耗ULP的实现原理
date: 2019-09-25 15:47:50
tags: ble
---

# BLE超低功耗ULP的实现原理

ble用得不少，也知道ble相对classic bluetooth更省电，那具体是怎么做到省电的呢？

<!--more-->

## ble

### 超低功耗ULP（Ultra Low Power）
> 非常少的广播信道数；标准蓝牙一共有32个信道，而BLE只有3个信道

- BLE搜索设备的时间大大缩短；BLE扫描其他设备只需要0.6ms~1.2ms，而标准蓝牙搜索其他设备要22.5ms
- BLE定位其它无线设备所需的功耗要比标准蓝牙技术低10至20倍
- 蓝牙低能耗技术的广告信道是经过慎重选择的，可以避免与Wi-Fi发生冲突
- 连接成功后，蓝牙低能耗技术就会切换到37个数据信道之一
![](https://www.crifan.com/files/doc/docbook/bluetooth_intro/release/htmls/images/ble_standard_bluetooth_wifi_channels.jpg)
- 尽可能的降低无线开启的时间，1Mbps的原始数据带宽——更大的带宽允许在更短的时间内发送更多的信息。举例来说，具有250kbps带宽的另一种无线技术发送相同信息需要开启的时间要长8倍（消耗更多电池能量）

> 更加“宽松的”射频参数和发送很短的数据包

- 通过这两种方式限制峰值功耗
- 更低调制指数还有两个好处，即提高覆盖范围和增强健壮性
- 蓝牙低能耗技术使用非常短的数据包——这能使硅片保持在低温状态，低能耗收发器不需要较耗能的再次校准和闭环架构。

> 可变连接时间间隔

- 蓝牙低能耗技术采用可变连接时间间隔，这个间隔根据具体应用可以设置为几毫秒到几秒不等；因为BLE技术采用非常快速的连接方式，因此平时可以处于“非连接”状态（节省能源）；此时链路两端相互间只是知晓对方，只有在必要时才开启链路，然后在尽可能短的时间内关闭链路


# BLE蓝牙协议栈架构
看到一个对协议栈有趣解释：

![](https://www.crifan.com/files/doc/docbook/bluetooth_intro/release/htmls/images/ble_protocol_arch_example_of_manufacture.jpg)

BLE中所有profile和应用都建构在GAP或GATT之上。

每一层的含义如下：

- PHY层==工作车间
	
	1Mbps自适应跳频GFSK（高斯频移键控），运行在免证的2.4GHz

- LL层==RF控制器==控制室
	
	控制设备处于准备（standby）、广播、监听/扫描 （scan）、初始化、连接，这五种状态中一种。
	
	五种状态切换描述为：未连接时，设备广播信息（向周围邻居讲“我来了”），另外一个设备一直监听或按需扫描（看看有没有街坊邻居家常里短可聊，打招呼“哈，你来啦”），
	
	两个设备连接初始化（搬几把椅子到院子），设备连接上了（开聊）。
	
	发起聊天的设备为主设备，接受聊天的设备为从设备，同一次聊天只能有一个意见领袖，即主设备和从设备不能切换。

- HCI层==接口层==通信部
	
	向上为主机提供软件应用程序接口（API），对外为外部硬件控制接口，可以通过串口、SPI、USB来实现设备控制

- L2CAP层==物流部
	
	行李打包和拆封处，提供数据封装服务

- SM层==保卫处
	
	提供配对和密匙分发，实现安全连接和数据交换

- ATT层==库房
	
	负责数据检索

- GATT层==出纳/库房前台

	出纳负责处理向上与应用打交道，而库房前台负责向下把检索任务子进程交给ATT库房去做，
	其关键工作是把为检索工作提供合适的profile结构，而profile由检索关键词（characteristics）组成。

- GAP层==秘书处
	
	对上级，提供应用程序接口
	对下级，管理各级职能部门，尤其是指示LL层控制室五种状态切换，指导保卫处做好机要工作
	
	
	[参考链接1](https://www.crifan.com/files/doc/docbook/bluetooth_intro/release/htmls/ble_proto_arch.html)
	
	[参考链接2](https://www.crifan.com/files/doc/docbook/bluetooth_intro/release/htmls/ble_ultra_low_power.html)
