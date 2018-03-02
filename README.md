# flask框架电影网站
### flask优点
- 冗余度小
- 扩展丰富
- 自由组合各种插件
- 性能优越

### 本项目
微电影网站
前台+后台管理

### flask框架知识
- 整型，浮点型，路径型，字符串型正则表达式路由转化器
- post与get请求，上传文件，cookie获取与响应，404处理
- 模板自定义转义，定义过滤器，定义全局上下文处理器，Jinjia2语法，包含，继承，定义宏
- 使用flask-wtf定义表单模型，字段类型，字段验证，视图处理表单，模板使用表单
- 使用flask-sqlachemy定义数据库模型
- 使用蓝图优化项目结构，实现前后台业务逻辑
- flask的部署方法，安装编译nginx服务，安装编译python3.6服务，安装MySQL服务以及通过nginx反向代理对视频流媒体限制下载速率，限制单个IP能发起的播放链接数
- 微内核+扩展插件:werkzug工具箱，pymysql数据库驱动，sqlalchemy数据库orm，wtforms表单验证工具，jinjia2模板引擎，flask-script命令行脚本，functools定义高阶函数

### 视频技术
- jwplayer播放器插件
- 视频限速限IP访问
- flv,mp4视频格式支持
- nginx点播实现

### 课程结构：11章，6部分
#### 一，课程介绍
- 整体开发流程
- flask简介
- 课程知识点

#### 二，环境与工具
- 安装包，virtualenv,pycharm,pip
- centOSB，python3，MySQL，HTML5，flask，NGINX

#### 三，项目优化与模型
- 蓝图Blueprint
- flask sqlalchemy
- mysql 

#### 四，前台搭建
- 前后台HTML页面
- jinjia2
- 静态文件，404处理

#### 五，后端开发
- flask sqlalchemy结合MySQL
- flask数据分页查询，路由装饰器定义，模板中变量调用登录会话机制，上传文件
- flask wtforms表单验证，flask自定义应用上下文，自定义权限装饰器对管理系统进行基于角色权限的访问控制
- flask的多表关联查询，关键字模糊查询

#### 六，网站部署
- 在centos服务器上搭建nginx+mysql+python环境
- 使用nginx反向代理多端口多进程部署微电影网站
- 配制nginx流媒体访问限制参数

### 网站组成
前台：
- 会员登录注册
- 会员中心
- 电影播放
- 电影评论
- 电影收藏
后台：
- 管理员登录
- 修改密码
- 标签管理
- 电影管理
- 预告管理
- 会员管理
- 评论管理
- 收藏管理
- 角色管理
- 权限管理
- 管理员管理
- 日志管理

### web开发实例：
- 果壳flask
- 知乎tornado
- 豆瓣Quixote

### 环境搭建
1. 操作系统:mac os
2. python3.6:https://www.python.org/
3. mysql5.6
4. virtualenv
5. pycharm

### pycharm 创建新项目flask-movie
#### 安装flask
- 在terminal虚拟环境中安装flask:
pip3 install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com flask
- 或者在pycharm的preferences里面的Project Interpreter点击加号搜索flask,然后点击install package

### 目录，蓝图
blueprint

### 数据模型
前台模型：

- 会员表user
- 会员登录日志userlog
- 标签表tag
- 电影表movie
- 上映预告preview
- 评论comment
- 电影收藏moviecol
后台模型：
- 权限表auth
- 角色表role
- 管理员表admin
- 管理员登录日志adminlog
- 操作日志oplog

### 安装flask-sqlalchemy
pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask-sqlalchemy

### 安装pymysql
在pycharm的preferences里面的Project Interpreter点击加号搜索PyMySQL,然后点击install package
### mysql登录
mysql -uroot -p123456




















 