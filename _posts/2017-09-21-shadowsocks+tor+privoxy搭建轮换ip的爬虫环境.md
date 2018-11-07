***本人原创，转载请注明出处***

1、前置代理
(1)前提:tor在大陆被GFW封杀，网桥、meek等方式已经不能连接到tor网络，需要前置代理服务器(海外，可以连接tor网络的服务器),选择shadowsocks
(2)shadowsocks分服务器端与客户端两部分，有海外vps时可以自行搭建服务器端，在下述网址找到免费可用代理：
    https://unwire.hk/2017/08/16/shadowsocks-windows-macos/software/
	https://www.namaho.org/ssweb/user/info
(3)linux上安装shadowsocks客户端:
    ①pip install shadowsocks
	②在任意目录下新建文件shadowsocks.json,内容如下:
	{
		"server":"my_server_ip",
		"server_port":my_server_port,
		"local_address": "127.0.0.1",
		"local_port":1080,
		"password":"my_password",
		"timeout":300,
		"method":"rc4-md5"     ##加密方式
	}
	③sslocal -c shadowsocks.json，启动shadowsocks
	 或者执行命令，sslocal -s server_ip -p server_port  -l 1080 -k password -t 600 -m aes-256-cfb
2、tor
	(1)yum install tor 
	(2)修改tor配置文件 /etc/tor/torrc，修改/添加如下语句:
	    SOCKSPort 9050 				               #监听本地连接  
		SOCKSPort 0.0.0.0:9150 		               #监听所有连接,socks5协议
	   为tor配置前置代理，在文件末尾添加如下语句：
	    Socks5Proxy 127.0.0.1:1080                 #使tor的流量走1080端口，通过shadowsocks，由不封杀tor的海外服务器连接到tor网络       
	(3)打开管理端口,控制切换出口ip
	   ①tor --hash-password mypassword             #生成管理密码,以 16: 开头的一段字符串
	   ②编辑 /etc/tor/torrc,修改/添加如下语句：
       	    ControlPort  9051                          #管理端口是9051
		    HashedControlPassword  16:xx..xx           #此处密码即是上面生成的16:开头的字符串
			CookieAuthentication 1                     #开启cookie认证
	   ③linux下python环境中切换tor网络出口ip:
	        os.system("""(echo authenticate '"mypassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
	(4)systemctl start tor ,开启tor服务
3、privoxy
	(1)yum install privoxy 
	(2)修改/etc/privoxy/config,如下:
	   修改 listen-address 0.0.0.0:8118            #使privoxy监听所有网络连接
	   添加 forward-socks5 / localhost:9050 .      #将流量转向socks5协议的tor端口9050,一定不要丢掉最后的点 . ，
												   #这个点表示没有http设置,去掉将报错。
4、验证
    (1)ipinfo.io、ifconfig.me这两个网址可以显示本机的公网ip；
	   torify、torsocks可以使请求走tor网络；
	(2)实例：
       curl ifconfig.me 或 curl ipinfo.io                     #显示本机公网ip
	   torify curl ifconfig.me 或 torify curl ifconfig.me     #显示经过tor网络后本机公网ip
6、注意
   (1)设置requests的proxies参数, proxies={'http':'ip:port'}或proxies={'https':'ip:port'}，与设置正常的http协议代理一样；
   socks5协议代理使用 proxies={'http':'socks5://user:password@ip:port'}或proxies={'https':'socks5://user:password@ip:port'}
   (2)通过9051与tor通信方式:
      ①直接通过操作系统控制tor切换线路:
	   windows下           telnet ip port => authenticate  "password(必须带双引号)"  =>  signal newnym  =>  quit
       linux下python环境   os.system("""(echo authenticate '"mypassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
	  ②通过python的stem模块与tor交互
	   stem官方文档   https://stem.torproject.org/index.html
	   pip install stem
	   from stem import Signal
	   from stem.control import Controller
	   with Controller.from_port(address='ip',port=yourport) as controller:        #ip地址需要加引号,端口不需要
	       controller.authenticate(password="password")                            #验证密码必须加双引号,加密计算前的密码
		   controller.signal(Signal.NEWNYM)                                        
		   controller.close()
	(3)编辑/etc/tor/torrc,排除部分节点,避开蜜罐
	   #指定进入节点国家
       #EntryNodes
       #指定出节点国家
	   #ExitNodes
	   #排除入节点国家
	   ExcludeNodes {cn},{hk},{mo},{kp},{ir},{sy},{pk},{cu},{vn}
	   #排除出节点国家
	   ExcludeExitNodes {cn},{hk},{mo},{kp},{ir},{sy},{pk},{cu},{vn}
	   #强制使用指定节点，如果不设置strictnode 1，TOR 客户端首先也会规避ExcludeNodes列出的这些国家。但如果 TOR 客户端
	    找不到可用的线路，就会去尝试位于排除列表中的节点。如果设置了 strictnode 1，即使 TOR 客户端找不到可用的线路，也不会去尝试这些国家的节点。
       strictnodes 1
	(4)tor配置文件torrc编辑汇总:
       SOCKSPort 9050                    
	   SOCKSPort 0.0.0.0:9150
	   
	   SOCKS5Proxy 127.0.0.1:1080
	   
	   ControlPort 0.0.0.0:9051
	   CookieAuthentication 1
	   HashedControlPassword 16:8F4EADB49B5425B06072283EB3D76368010B547E379FB59D3680333218
	   
	   ExcludeNodes {cn},{hk},{mo},{kp},{ir},{sy},{pk},{cu},{vn}  
	   ExcludeExitNodes {cn},{hk},{mo},{kp},{ir},{sy},{pk},{cu},{vn}
	   strictnodes 1	
6、异常处理
    错误信息:”Job for tor.service failed because the control process exited with error code. See "systemctl status tor.service" and "journalctl -xe" for details.“
    原因:(1)安装的tor是老版本,systemctl启动tor时存在bug,需要改/lib/systemd/system/tor.service文件:
	        ReadOnlyDirectories=/
			ReadWriteDirectories=/var/lib/tor
			ReadWriteDirectories=/var/log/tor
		 (2)编辑配置文件/etc/torrc出现拼写错误。
   
   
   
   
