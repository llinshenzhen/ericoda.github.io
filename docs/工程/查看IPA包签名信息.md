---
title: 查看IPA包签名信息
date: 2019-10-17 16:13:07
tags: iOS
---

#### 业务需要获得ipa包做一些MFi的测试，记性不好，记录一下操作步骤。

- 首先通过configurator下载安装包，如果手机中没有，则需要先安装一次，第二次安装的时候会出现弹窗，此时进入路径找到IPA包。
`~/Library/Group Containers/K36BKF7T3D.group.com.apple.configurator/Library/Caches/Assets/TemporaryItems/MobileApps/`

- 解压IPA安装包，如果弹出损坏报错，则输入`sudo spctl --master-disable`

- 一直找到对应app下的二进制文件，使用命令 `codesign -d -vv XXX`

#### 以spotify为例，结果如下：

```
Identifier=com.spotify.client
Format=app bundle with Mach-O universal (armv7 arm64)
CodeDirectory v=20500 size=762910 flags=0x0(none) hashes=11915+7 location=embedded
Signature size=4390
Authority=Apple iPhone OS Application Signing
Authority=Apple iPhone Certification Authority
Authority=Apple Root CA
Info.plist entries=62
TeamIdentifier=2FNC3A47ZF
Sealed Resources version=2 rules=14 files=731
Internal requirements count=1 size=100
```

