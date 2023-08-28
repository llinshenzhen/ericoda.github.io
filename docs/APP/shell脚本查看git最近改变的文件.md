---
title: shell脚本查看git最近改变的文件
date: 2019-11-21 16:12:53
tags: other
---

最近在做安卓平板适配，由于项目是由另外一个团队的同事在开发，我只针对layout做出横竖屏适配即可。但由于他们每天提交大量代码，我也不知道他们修改了哪些layout文件。所以我就需要查看git日志，通过时间来判断是否需要作出调整，一个个看文件是不可能的，所以就写了个脚本。其中的核心命令就是`git log --after="2019-11-11" xxx.xml`个命令，能查看某个文件在指定日期之后有没有提交。

shell的判断有个坑，就是要这个命令输出的结如果有符合条件的是字符串类型，如果没有就是data类型，我开始以为是数组，所以用长度去判断，一直都是4，原来不是。

```
#!/bin/bash

currentpath=$PWD

folderpath=/Users/doubll/workspace/eufySecurity-Android/android/BatteryCam/app/src/main/res/layout

cd $folderpath

files=$(ls $folderpath)

for filename in $files
do
time="2019-11-11"
result=$(git log --after=$time $filename)
echo $result|grep [a-zA-Z]>/dev/null
if [ $? -eq 0 ];then
echo $filename
echo "${filename}" >> changed_files.txt
fi
done

cd $currentpath
```
