---
layout: default
author: muyalei
date: 2019-01-16
title: shell script笔记
tag:
   - linux相关
---


循环的理解：

- while..do..done 当条件满足的时候，就执行do后面跟的循环语句。如：
```
while [ "${yn}" != "yes" -a "${yn}" != "YES" ] 
do
	read -p "Please input yes/YES to stop this program: " yn done
echo "OK! you input the correct answer."
```

- until..do..done 直到条件满足才会跳出循环，否则一只执行do后面跟的循环语句。如：
```
until [ "${yn}" == "yes" -o "${yn}" == "YES" ] 
do
	read -p "Please input yes/YES to stop this program: " yn done
echo "OK! you input the correct answer."
```
