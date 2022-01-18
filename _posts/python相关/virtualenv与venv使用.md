---
layout: default
author: muyalei
title: virtualenv与venv
date: 2021-09-14
tags:
	- python相关
---


**整理自：[https://blog.csdn.net/yezhenquan123/article/details/79313110](https://blog.csdn.net/yezhenquan123/article/details/79313110)**


### virtualenv

Python2 和 Python3 均支持的方式

**安装**
```
pip install virtualenv
```

**创建项目**
```
cd my_project_folder
virtualenv my_project
```

**指定python版本**
```
virtualenv -p /usr/bin/python2.7 my_project
或者在环境变量配置中加入
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7
```

**激活虚拟环境**
```
(Linux) source my_project/bin/activate
(Windows) my_project\Scripts\activate
```

**退出环境**
```
(Linux) my_project/bin/deactivate
(Windows) my_project\Scripts\deactivate.bat
```

**virtualenv 常用命令选项**
```
virtualenv [OPTIONS] DEST_DIR

Options:
–version　　　　　显示版本信息。
-h, –help　　　　　显示帮助信息。
-v, –verbose　　　增加后台输出的信息。
-q, –quiet　　　　控制后台输出的信息。
-p PYTHON_EXE, –python=PYTHON_EXE　　
　　　　　　　　　指定 Python 解释器
–clear　　　　　　清除虚拟环境中依赖库，初始化环境。
–system-site-packages
　　　　　　　　　使用当前 Python 主体上已安装的程序库。
–always-copy　　　一概不使用 符号链接，直接复制文件。
–no-setuptools　　Do not install setuptools in the new virtualenv.
–no-pip　　　　　Do not install pip in the new virtualenv.
–no-wheel　　　　Do not install wheel in the new virtualenv.
```

#### virtualenv 相关扩展

**virtualenvwrapper**

virtualenv 的扩展包，能方便的管理 virtualenv

**安装**

环境变量 WORKON_HOME 指定虚拟环境位置
```
(Linux)
pip install virtualenvwrapper
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
(Windows)
pip install virtualenvwrapper-win
WORKON_HOME 默认值是 %USERPROFILE%Envs
```

**基本用法**

创建虚拟环境
```
mkvirtualenv myenv
```

切换到虚拟环境
```
workon myenv
```

虚拟环境和项目分开
```
mkproject my_project
```
虚拟环境在 WORKON_HOME 中，项目在 PROJECT_HOME 中

退出虚拟环境
```
deactivate
```

删除虚拟环境
```
rmvirtualenv myenv
```

**其它用法**
```
lsvirtualenv 列举所有的环境。
cdvirtualenv [subdir] 导航到当前激活的虚拟环境的目录中
cdsitepackages [subdir] 和上面的类似，但是是直接进入到 site-packages 目录中
lssitepackages 显示 site-packages 目录中的内容
showvirtualenv [env] 显示指定环境的详情
cpvirtualenv [source] [dest] 复制一份虚拟环境
allvirtualenv 对当前虚拟环境执行统一的命令
add2virtualenv [dir] [dir] 把指定的目录加入当前使用的环境的path中，这常使用
于在多个project里面同时使用一个较大的库的情况
toggleglobalsitepackages -q 控制当前的环境是否使用全局的sitepackages目录
```

**virtualenv-burrito**

相当于 virtualenv + virtualenvwrapper ，不过只支持 python 2

**autoenv**

当进入到一个包含 .env 的目录，autoenv 会自动激活该环境
```
pip install autoenv
```

### venv

Python3 支持的方式，原名又 pyvenv，python 3.6 已弃用

**创建虚拟环境**
```
python3 -m venv /path/to/new/virtual/environment
```

**命令帮助**
```
python3 -m venv -h

usage: venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear]
            [--upgrade] [--without-pip] [--prompt PROMPT]
            ENV_DIR [ENV_DIR ...]
Creates virtual Python environments in one or more target directories.
positional arguments:
  ENV_DIR              A directory to create the environment in.
optional arguments:
  -h, --help              帮助信息
  --system-site-packages  给虚拟环境访问系统 site-packages 目录的权限
  --symlinks              当系统默认不是符号链接的方式时，尝试使用符号链接而不是复制。
  --copies                尝试使用复制而不是符号链接，即使符号链接是平台默认的方式。
  --clear                 在虚拟环境创建之前，删除已存在的虚拟环境目录。
  --upgrade               使用当前 python，升级虚拟环境目录。
  --without-pip           跳过pip的升级或安装
  --prompt PROMPT         为该环境提供一个提示前缀

Once an environment has been created, you may wish to activate it, e.g. by
sourcing an activate script in its bin directory.
```

**不同平台激活虚拟环境方法**

Platform|Shell|激活虚拟环境命令
---|:--:|---:
Posix|bash/zsh|$ source /bin/activate
|fish|$ . /bin/activate.fish
|csh/tcsh|$ source /bin/activate.csh
Windows|cmd.exe|C:> \Scripts\activate.bat
|PowerShell|PS C:> \Scripts\Activate.ps1