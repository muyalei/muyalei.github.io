---
layout: default
author: muyalei
title: superset使用ldap认证
date: 2019-09-19
tags:
    - superset
---


### 一、前言

superset的ldap认证设置这块儿，官方给出的指导文档有限，网上搜出来的配置方式也是五花八样，我本地实际测试后，都没能成功（没能成功的很大一部分原因是对我公司的ldap服务器配置没查证，默认ldap服务器配置是标准的来处理了）


### 二、安装superset

***1、anaconda安装。***</p >
略。

***2、使用pip工具安装。***</p >
整理自***[https://www.cnblogs.com/lovely-lisk/p/11411785.html](https://www.cnblogs.com/lovely-lisk/p/11411785.html)***</p >
防止链接页面丢失，主要过程整理如下：</p >
pip下载的依赖会按照其脚本找相应的版本，可能处于某些插件没有指定版本被下载了不兼容的版本的缘故，这里在此命令基础安装完成后对几个包的版本进行替换：</p >
1是pandas： pip install pandas==0.23.4</p >
2是flask-jwt-extended：pip install flask-jwt-extended==3.10.0</p >
3是flask-appbuilder：pip install flask-appbuilder==1.12.1 #基础思想就是改版本直到红字消失,可能每个人的环境会有不同，记住这是方法和思路</p >
4是SQLAlchemy：pip install sqlalchemy==1.2.18</p >

初始化superset：</p >
```
#一些基本设定
python fabmanager create-admin --app superset  

#初始化数据库
python superset db upgrade  

#载入样例
python superset load_examples  

#初始化role and power
python superset init 

#启动服务-p是设置端口，默认8088
python superset runserver -p 3000 -d
```
注：安装的superset版本是0.28.0

### 三、修改superset/config.py文件
 
(1)引入AUTH_LDAP，在`from flask_appbuilder.security.manager import AUTH_DB,AUTH_LDAP`中加上AUTH_LDAP</p >
(2)将`AUTH_TYPE = AUTH_DB`改成`AUTH_TYPE = AUTH_LDAP`</p >
(3)增加下列配置信息：
```
AUTH_USER_REGISTRATION = True
AUTH_LDAP_SERVER = 'ldap://ip:port' #也可以是'域名:端口'
AUTH_LDAP_SEARCH = 'ou=xx,dc=xx,dc=xx' #问运维
AUTH_LDAP_UID_FIELD = 'cn' #ldap服务不了解，我试了其他字段，只能用'cn'查
AUTH_LDAP_BIND_USER = "xxx" #问运维
AUTH_LDAP_BIND_PASSWORD = 'xxxx' #问运维
```

### 四、superset配置ldap认证的源码分析

相关代码主要是在flask_appbuilder/security/views.py、flask_appbuilder/security/manager.py下，在superset/config.py中配置登录认证方式是ldap认证后，views.py中的login函数处理来自localhost:3000/login/的登录请求，代码如下：
```
class AuthLDAPView(AuthView):
394     login_template = 'appbuilder/general/security/login_ldap.html'
395 
396     @expose('/login/', methods=['GET', 'POST'])
397     def login(self):
398         if g.user is not None and g.user.is_authenticated:
399             return redirect(self.appbuilder.get_url_for_index)
400         form = LoginForm_db()
401         if form.validate_on_submit():
402             user = self.appbuilder.sm.auth_user_ldap(form.username.data, form.password.data)
403             if not user:
404                 flash(as_unicode(self.invalid_login_message), 'warning')
405                 return redirect(self.appbuilder.get_url_for_login)
406             login_user(user, remember=False)
407             return redirect(self.appbuilder.get_url_for_index)
408         return self.render_template(self.login_template,
409                                title=self.title,
410                                form=form,
411                                appbuilder=self.appbuilder)
```
在这个函数中调用了auth_user_ldap函数完成ldap认证过程，auth_user_ldap函数的代码如下：
```
    def _search_ldap(self, ldap, con, username):
        """
            Searches LDAP for user, assumes ldap_search is set.

            :param ldap: The ldap module reference
            :param con: The ldap connection
            :param username: username to match with auth_ldap_uid_field
            :return: ldap object array
        """
        if self.auth_ldap_append_domain: #superset/config.py中没有配置参数AUTH_LDAP_APPEND_DOMAIN,跳过这行继续向下执行
            username = username + '@' + self.auth_ldap_append_domain
        filter_str = "%s=%s" % (self.auth_ldap_uid_field, username) #这里就是为什么要在superset/config.py中增加参数 AUTH_LDAP_UID_FIELD = 'cn'，因为superset与ldap服务器通讯，验证用户名时用到了
        user = con.search_s(self.auth_ldap_search,
                            ldap.SCOPE_SUBTREE,
                            filter_str,
                            [self.auth_ldap_firstname_field,
                             self.auth_ldap_lastname_field,
                             self.auth_ldap_email_field
                            ]) #这句是调用了python-ldap的search_s方法，向ldap服务器查询用户信息，filter_str后面的三个参数是用来指定要查询的字段，可以不管
        if user:
            if not user[0][0]: #如果一切顺利，user[0][0]应该是类似[('CN=小风,OU=多多少啊,OU=huxxx,DC=hxxx,DC=com', {'mail': [b'mru@xxx.com']})]这样的信息
                return None
        return user

    def _bind_ldap(self, ldap, con, username, password):
        """
            Private to bind/Authenticate a user.
            If AUTH_LDAP_BIND_USER exists then it will bind first with it,
            next will search the LDAP server using the username with UID
            and try to bind to it (OpenLDAP).
            If AUTH_LDAP_BIND_USER does not exit, will bind with username/password
        """
        try:
            indirect_user = self.auth_ldap_bind_user #读取superset/config.py文件中的参数AUTH_LDAP_BIND_USER
            if indirect_user:
                indirect_password = self.auth_ldap_bind_password #读取参数AUTH_LDAP_BIND_PASSWORD
                log.debug("LDAP indirect bind with: {0}".format(indirect_user))
                con.bind_s(indirect_user, indirect_password) #绑定
                log.debug("LDAP BIND indirect OK")
                user = self._search_ldap(ldap, con, username) #跳到_search_ldap函数，查询用户信息
                if user:
                    log.debug("LDAP got User {0}".format(user))
                    # username = DN from search
                    username = user[0][0]
                else:
                    return False
            log.debug("LDAP bind with: {0} {1}".format(username, "XXXXXX"))
            if self.auth_ldap_username_format: 
                username = self.auth_ldap_username_format % username
            if self.auth_ldap_append_domain:
                username = username + '@' + self.auth_ldap_append_domain #这两个参数，superset/config.py中都没设置，跳过向下执行
            con.bind_s(username, password)
            log.debug("LDAP bind OK: {0}".format(username))
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

    def auth_user_ldap(self, username, password):
        """
            Method for authenticating user, auth LDAP style.
            depends on ldap module that is not mandatory requirement
            for F.A.B.

            :param username:
                The username
            :param password:
                The password
        """
        if username is None or username == "": #登录用户名为空时返回None
            return None
        user = self.find_user(username=username) #find_user函数总是返回None
        if user is not None and (not user.is_active): #user为None，这一行判读不成立，继续向下执行
            return None
        else:
            try:
                import ldap #superset是通过flask_appbuilder做的ldap登录认证，flask_appbuilder做ldap认证使用的是python-ldap模块，一个比较古老的模块，跟ldap3不一样
            except:
                raise Exception("No ldap library for python.")
            try:
                if self.auth_ldap_allow_self_signed: #auth_ldap_allow_self_signed函数是去superset/config.py文件读参数AUTH_LDAP_ALLOW_SELF_SIGNED，没有设置这个参数，所以这一行不成立，继续向下执行
                    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
                con = ldap.initialize(self.auth_ldap_server) 
                con.set_option(ldap.OPT_REFERRALS, 0) #这两行都是使用python的python-ldap模块连接ldap服务器
                if self.auth_ldap_use_tls: #如果ldap服务器做了TLS，superset/config.py文件中需要增加配置信息`AUTH_LDAP_USE_TLS = True`
                    try: 
                        con.start_tls_s()
                    except Exception:
                        log.info(LOGMSG_ERR_SEC_AUTH_LDAP_TLS.format(self.auth_ldap_server))
                        return None
                # Authenticate user
                if not self._bind_ldap(ldap, con, username, password): #跳到_bind_ldap函数，做绑定动作，如果用户认证成功，后面的语句跳过，继续向下执行
                    if user:
                        self.update_user_auth_stat(user, False)
                    log.info(LOGMSG_WAR_SEC_LOGIN_FAILED.format(username))
                    return None
                # If user does not exist on the DB and not self user registration, go away
                if not user and not self.auth_user_registration:  
                    return None
                # User does not exist, create one if self registration.
                elif not user and self.auth_user_registration: #这里是为什么superset/config.py中增加参数AUTH_USER_REGISTRATION = True
                    new_user = self._search_ldap(ldap, con, username) #new_user是根据用户输入的名字在ldap服务器查询到的用户信息
                    if not new_user:
                        log.warning(LOGMSG_WAR_SEC_NOLDAP_OBJ.format(username))
                        return None
                    ldap_user_info = new_user[0][1]
                    if self.auth_user_registration and user is None:
                        user = self.add_user(
                            username=username,
                            first_name=self.ldap_extract(ldap_user_info, self.auth_ldap_firstname_field, username),
                            last_name=self.ldap_extract(ldap_user_info, self.auth_ldap_lastname_field, username),
                            email=self.ldap_extract(ldap_user_info, self.auth_ldap_email_field, username + '@email.notfound'),
                            role=self.find_role(self.auth_user_registration_role)
                        )

                self.update_user_auth_stat(user)
                return user

            except ldap.LDAPError as e:
                if type(e.message) == dict and 'desc' in e.message:
                    log.error(LOGMSG_ERR_SEC_AUTH_LDAP.format(e.message['desc']))
                    return None
                else:
                    log.error(e)
                    return None
```












